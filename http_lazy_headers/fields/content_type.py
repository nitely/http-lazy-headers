# -*- coding: utf-8 -*-

from ..shared.values import media_types
from ..shared import bases
from ..shared import cleaners
from ..shared import helpers


def content_type(
        top_level,
        sub_level,
        charset=None):
    return media_types.media_type(
        top_level, sub_level, charset=charset)


class ContentType(bases.SingleHeaderBase):
    """
    The ``Content-Type`` header field indicates\
    the media type of the associated representation:\
    either the representation enclosed in the\
    message payload or the selected representation,\
    as determined by the message semantics. The\
    indicated media type defines both the data\
    format and how that data is intended to be\
    processed by a recipient, within the scope of\
    the received message semantics, after any\
    content codings indicated by ``Content-Encoding``\
    are decoded.

    Example::

        ContentType([
            content_type(
                MediaType.text,
                MediaType.html,
                charset=Charsets.utf_8)
        ])

        ContentType([
            (
                ('text', 'html'),
                Params({'charset': 'ISO-8859-4'})
            )
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.content-type>`_
    """

    name = 'content-type'

    def values_str(self, values):
        return next(
            helpers.format_values_with_params(
                ('/'.join(mime), params)
                for mime, params in values))

    def clean_value(self, value):
        return cleaners.clean_media_type(value)
