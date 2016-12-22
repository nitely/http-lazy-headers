# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import quality
from ..shared import parameters
from ..shared.values import encodings


def accept_encoding(encoding, quality=None):
    assert (
        encoding == '*' or
        encoding in encodings.ENCODING_VALUES)
    assert (
        quality is None or
        0 <= quality <= 1)

    params = ()

    if quality is not None:
        params = (('q', quality),)

    return encoding, parameters.ParamsCI(params)


class AcceptEncoding(bases.AcceptSomeBase):
    """
    Sent by client.

    Encodings the client accepts or refuses.

    This is one of the few headers where\
    there may be no values.

    If is empty, the user agent does not\
    want any content-coding in response.

    If is present and none is available as\
    response that is acceptable, send a\
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
            (Encodings.gzip, Params({'q': 1})),
            (Encodings.identity, Params({'q': 0.5})),
            ('*', Params({'q': 0.1}))
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.accept-encoding>`_
    """

    name = 'accept-encoding'

    def clean(self, raw_values):
        # Allow empty value
        return tuple(sorted(
            (
                self.clean_value(raw_value)
                for raw_value in raw_values),
            key=quality.quality_sort_key))
