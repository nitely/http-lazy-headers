# -*- coding: utf-8 -*-

from ..shared.generic import formatters
from ..shared.generic import cleaners
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared.utils import assertions
from ..shared import bases
from ..shared import parameters
from ..shared.values import encodings


def transfer_encoding(te):
    assert te in encodings.ENCODING_VALUES

    return te, parameters.Params()


class TransferEncoding(bases.MultiHeaderBase):
    """
    The ``Transfer-Encoding`` header field lists the\
    transfer coding names corresponding to the\
    sequence of transfer codings that have been\
    (or will be) applied to the payload body in\
    order to form the message body.

    Example::

        TransferEncoding([
            transfer_encoding(Encodings.gzip),
            transfer_encoding(Encodings.chunked)
        ])

        TransferEncoding([
            (Encodings.gzip, Params()),
            (Encodings.chunked, Params())
        ])

        TransferEncoding([
            ('gzip', Params()),
            ('chunked', Params())
        ])

        TransferEncoding([
            ('my_encoding', Params({'lvl': 5})
        ])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.transfer-encoding>`_
    """

    name = 'transfer-encoding'

    def check_one(self, value):
        assertions.must_be_tuple_of(value, 2)
        encoding, params = value
        assertions.must_be_token(encoding)
        assertions.must_be_ascii_params(params)

    def to_str(self, values):
        return ', '.join(
            formatters.format_values_with_params(values))

    def clean_one(self, raw_value):
        value, raw_params = parsers.from_raw_value_with_params(raw_value)
        constraints.must_be_token(value)
        return (
            value.lower(),
            cleaners.clean_params(raw_params))
