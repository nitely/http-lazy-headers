# -*- coding: utf-8 -*-

from ..shared.values import media_types
from ..shared import bases
from ..shared import cleaners
from ..shared import helpers
from ..shared import quality


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

    def values_str(self, values):
        return ', '.join(
            helpers.format_values_with_params(
                ('/'.join(mime), params)
                for mime, params in values))

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_multi_raw_values(raw_values_collection)

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
