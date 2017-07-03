# -*- coding: utf-8 -*-

from ..shared.generic import formatters
from ..shared.generic import cleaners
from ..shared.generic import quality
from ..shared.generic import preparers
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared.utils import assertions
from ..shared import bases
from ..shared import parameters
from ..shared.values import encodings


def te(encoding, quality=None):
    assert (
        (encoding == TEncodings.trailers and
         quality is None) or
        encoding in encodings.ENCODING_VALUES)
    assert (
        quality is None or
        isinstance(quality, int))
    assert (
        quality is None or
        (isinstance(quality, int) and
         0 <= quality <= 1))

    params = ()

    if quality is not None:
        params = (('q', quality),)

    return encoding, parameters.Params(params)


class TEncodings(encodings.Encodings):

    trailers = 'trailers'


class TE(bases.HeaderBase):
    """
    Sent by client only.

    May be empty.

    The ``TE`` header field in a request\
    indicates what transfer codings, besides\
    chunked, the client is willing to accept\
    in response, and whether or not the client\
    is willing to accept trailer fields in a\
    chunked transfer coding.

    Example::

        TE([
            te(TEncodings.trailers),
            te(TEncodings.deflate, quality=1)
        ])

        TE([
            (TEncodings.trailers, Params()),
            (TEncodings.deflate, Params({'q': 1})),
        ])

        TE([
            ('trailers', Params()),
            ('deflate', Params({'q': 1}))
        ])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.te>`_
    """

    name = 'te'

    def check_one(self, value):
        assertions.must_be_tuple_of(value, 2)
        encoding, params = value
        assertions.must_be_token(encoding)
        assertions.must_be_quality(params)

    def check(self, values):
        for v in values:
            self.check_one(v)

    def to_str(self, values):
        return ', '.join(
            formatters.format_values_with_params(values))

    def prepare_raw(self, raw_values_collection):
        return preparers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, raw_value):
        value, raw_params = parsers.from_raw_value_with_params(raw_value)
        constraints.must_be_token(value)

        return (
            value.lower(),
            cleaners.clean_quality(
                cleaners.clean_params(raw_params)))

    def clean(self, raw_values):
        # Allow empty field
        return tuple(sorted(
            (self.clean_value(raw_value)
             for raw_value in raw_values),
            key=quality.quality_sort_key))
