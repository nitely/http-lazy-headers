# -*- coding: utf-8 -*-

from ..shared.generic import quality
from ..shared import bases
from ..shared import parameters
from ..shared.values import encodings
from ..shared.utils import assertions


def accept_encoding(encoding, quality=None):
    assert (
        encoding == '*' or
        encoding in encodings.ENCODING_VALUES)
    assert (
        quality is None or
        0 <= quality <= 1)

    return encoding, quality


class AcceptEncoding(bases.AcceptSomeBase):
    """
    Sent by client.

    Encodings the client accepts or refuses.

    This is one of the few headers where\
    there may be no values.

    If it's empty, the user agent does not\
    want any content-coding in the response.

    If it's present and none is available as\
    an acceptable (quality > 0) response, send a\
    response without any content-coding.

    Example::

        AcceptEncoding([
            accept_encoding(
                Encodings.gzip,
                quality=1),
            accept_encoding(
                Encodings.identity,
                quality=0.5),
            accept_encoding(
                '*',
                quality=0.1)
        ])

        AcceptEncoding([
            (Encodings.gzip, 1),
            (Encodings.identity, 0.5),
            ('*', 0.1)
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.accept-encoding>`_
    """

    name = 'accept-encoding'

    def check_values(self, values):
        for v in values:
            assertions.must_be_tuple_of(v, 2)

            encoding, weight = v

            assertions.must_be_token(encoding)
            assertions.must_be_weight(weight)

    def clean(self, raw_values):
        # Allow empty value
        return tuple(sorted(
            (
                self.clean_value(raw_value)
                for raw_value in raw_values),
            key=quality.weight_sort_key))
