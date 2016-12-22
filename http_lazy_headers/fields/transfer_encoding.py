# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import helpers
from ..shared import parsers
from ..shared import cleaners
from ..shared import constraints
from ..shared import parameters
from ..shared.values import encodings


def transfer_encoding(te):
    assert te in encodings.ENCODING_VALUES

    return te, parameters.Params()


class TransferEncoding(bases.HeaderBase):
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
    codings = frozenset((
        'chunked',
        'compress',
        'deflate',
        'gzip'))

    def values_str(self, values):
        return ', '.join(
            helpers.format_values_with_params(values))

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, raw_value):
        value, raw_params = parsers.from_raw_value_with_params(raw_value)
        constraints.must_be_token(value)
        return (
            value.lower(),
            cleaners.clean_params(raw_params))

    def clean(self, raw_values):
        values = tuple(
            self.clean_value(rv)
            for rv in raw_values)
        constraints.must_not_be_empty(values)
        return values
