# -*- coding: utf-8 -*-

from ..shared.generic import cleaners
from ..shared.generic import quality
from ..shared.generic import preparers
from ..shared.utils import assertions
from ..shared import bases
from ..shared.values import media_types
from ..shared.common import media_ranges


def accept(
        top_level,
        sub_level,
        quality=None,
        charset=None):
    return media_types.media_type(
        top_level, sub_level, quality, charset)


class Accept(bases.HeaderBase):
    """
    Sent by client only.

    This is one of the few headers where\
    there may be no values.

    The ``Accept`` header field can be\
    used by user agents to specify response\
    media types that are acceptable. Accept\
    header fields can be used to indicate that\
    the request is specifically limited to a\
    small set of desired types, as in the case\
    of a request for an in-line image.

    Example::

        Accept([
            accept(
                MediaType.text,
                MediaType.html,
                quality=1),
            accept(
                MediaType.text,
                MediaType.star,
                quality=0.5)
        ])

        Accept([
            (('text', 'html'), Params({'q': 1})),
            (('text', '*'), Params({'q': 0.5}))
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.accept>`_
    """

    name = 'accept'

    def check_values(self, values):
        for v in values:
            media_ranges.check_value(v)

            _, params = v

            # There may be a "q" with no value
            # and "charset" with no value, but
            # we don't allow it
            assertions.must_be_quality(params)
            assertions.must_be_token(
                params.get('charset', 'dummy'))
            assertions.assertion(
                all(isinstance(v, str)
                    for p, v in params.items()
                    if not p == 'q'),
                '"{}" received, all params as str '
                'were expected'.format(params))

    def values_str(self, values):
        return ', '.join(
            media_ranges.format_media_ranges(values))

    def prepare_raw_values(self, raw_values_collection):
        return preparers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, value):
        # todo: params may contain only a token (no argument), except q
        value, params = media_ranges.clean_media_type(value)
        return value, cleaners.clean_quality(params)

    def clean(self, raw_values):
        # Allow empty field
        return tuple(sorted(
            (self.clean_value(raw_value)
             for raw_value in raw_values),
            key=quality.quality_mime_sort_key))
