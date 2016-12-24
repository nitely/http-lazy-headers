# -*- coding: utf-8 -*-

from ..shared.generic import formatters
from ..shared.generic import cleaners
from ..shared.generic import quality
from ..shared.generic import preparers
from ..shared.utils import assertions
from ..shared import bases
from ..shared import parameters
from ..shared.values import media_types


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
            (top_level, sub_level), params = v

            assertions.must_be_instance_of(
                top_level, str)
            assertions.must_be_instance_of(
                sub_level, str)
            assertions.must_be_token(top_level)
            assertions.must_be_token(sub_level)
            assertions.must_be_instance_of(
                params, parameters.Params)
            assertions.must_be_quality(
                params.get('q', 1))
            assertions.must_be_token(
                params.get('charset', 'token'))

    def values_str(self, values):
        return ', '.join(
            formatters.format_values_with_params(
                ('/'.join(mime), params)
                for mime, params in values))

    def prepare_raw_values(self, raw_values_collection):
        return preparers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, value):
        # todo: params may contain only a token (no argument), except q
        value, params = cleaners.clean_media_type(value)
        return value, cleaners.clean_quality(params)

    def clean(self, raw_values):
        # Allow empty field
        return tuple(sorted(
            (
                self.clean_value(raw_value)
                for raw_value in raw_values),
            key=quality.quality_mime_sort_key))
