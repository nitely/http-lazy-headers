# -*- coding: utf-8 -*-

from ..shared.utils import assertions
from ..shared.utils import constraints
from ..shared import bases
from ..shared.values import encodings


class ContentEncoding(bases.TokensHeaderBase):
    """
    The ``Content-Encoding`` header field indicates\
    what content codings have been applied to the\
    representation, beyond those inherent in the media\
    type, and thus what decoding mechanisms have to be\
    applied in order to obtain data in the media type\
    referenced by the Content-Type header field.\
    Content-Encoding is primarily used to allow a\
    representation's data to be compressed without\
    losing the identity of its underlying media type.

    Example::

        ContentEncoding([
            Encodings.gzip,
            Encodings.deflate
        ])

        ContentEncoding([
            'gzip',
            'deflate'
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.content-encoding>`_
    """

    name = 'content-encoding'

    def check_one(self, value):
        assertions.must_be_token(value)
        assertions.assertion(
            value.lower() in encodings.CONTENT_ENCODING_VALUES,
            '"{}" received, a value in {} '
            'was expected'.format(
                value, encodings.CONTENT_ENCODING_VALUES))

    def clean_one(self, raw_value):
        constraints.must_be_token(raw_value)
        raw_value = raw_value.lower()
        constraints.constraint(
            raw_value in encodings.CONTENT_ENCODING_VALUES,
            '{} is not a valid encoding'
            .format(raw_value),
            status=415)
        return raw_value
