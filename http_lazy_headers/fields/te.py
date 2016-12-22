# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import helpers
from ..shared import cleaners
from ..shared import quality
from ..shared import parsers
from ..shared import constraints
from ..shared import parameters
from ..shared.values import encodings


def te(encoding, quality=None):
    assert (
        encoding == TEncodings.trailers or
        encoding in encodings.ENCODING_VALUES)
    assert (
        encoding != TEncodings.trailers or
        quality is None)
    assert (
        quality is None or
        isinstance(quality, int))
    assert (
        quality is None or
        0 <= quality <= 1)

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
    codings = frozenset((
        'chunked',
        'compress',
        'deflate',
        'gzip',
        'trailers'))

    def values_str(self, values):
        # todo: remove the q=1 in trailers (from str values)
        return ', '.join(
            helpers.format_values_with_params(values))

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, raw_value):
        # todo: don't allow params in "trailers"

        value, raw_params = parsers.from_raw_value_with_params(raw_value)
        constraints.must_be_token(value)
        return (
            value.lower(),
            cleaners.clean_quality(
                cleaners.clean_params(raw_params)))

    def clean(self, raw_values):
        # Allow empty field
        return tuple(sorted(
            (
                self.clean_value(raw_value)
                for raw_value in raw_values),
            key=quality.quality_sort_key))

    def first_of(self, values):
        return quality.first_of(self.values(), values)

    def best_of(self, values):
        return quality.best_of(self.values(), values)
