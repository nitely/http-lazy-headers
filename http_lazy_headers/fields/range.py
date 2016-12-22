# -*- coding: utf-8 -*-

from .. import exceptions
from ..shared import bases
from ..shared import cleaners
from ..shared import parameters
from ..shared.values import ranges


def range_bytes(sub_ranges):
    assert sub_ranges
    assert all(
        1 <= len(sr) <= 2
        for sr in sub_ranges)
    assert all(
        all(
            isinstance(r, int)
            for r in sr)
        for sr in sub_ranges)
    assert all(
        sr[0] <= sr[1]
        for sr in sub_ranges
        if len(sr) == 2)

    return parameters.Params((
        (ranges.RangesOptions.bytes, tuple(sub_ranges)),))


class Range(bases.SingleHeaderBase):
    """
    Sent by client only.

    Be aware bytes order is not validated,\
    ignoring or raising an error when the order\
    of bytes is not ascendant or descendant\
    is up to the user.

    The ``Range`` header field on a GET request\
    modifies the method semantics to request transfer\
    of only one or more subranges of the selected\
    representation data, rather than the entire\
    selected representation data.

    Example::

        Range([
            range_bytes([
                (0, 499),
                (500, 999)])
        ])

        Range([
            Params([
                (Ranges.bytes, ((0, 499),))
            ])
        ])

        Range([
            Params([
                (Ranges.bytes, ((0, 499), (500, 999)))
            ])
        ])

        Range([
            Params([
                ('my_unit', 'my_sub_range')
            ])
        ])

    `Ref. <http://httpwg.org/specs/rfc7233.html#header.range>`_
    """

    name = 'range'

    def __init__(
            self,
            values=None,
            raw_values_collection=None):
        super().__init__(values, raw_values_collection)
        assert (
            self._values is None or
            isinstance(self._values[0], parameters.Params))
        assert (
            self._values is None or
            len(self._values[0]) == 1)

    def values_str(self, values):
        params = values[0]

        if ranges.RangesOptions.bytes not in params:
            return '{}={}'.format(
                *next(params.items()))

        return '{}={}'.format(
            ranges.RangesOptions.bytes,
            ', '.join(
                '{}-{}'.format(
                    start if start is not None else '',
                    end if end is not None else '')
                for start, end in params[ranges.RangesOptions.bytes]))

    def clean_value(self, raw_value):
        try:
            name, raw_param_value = raw_value.split('=', 1)
        except ValueError:
            raise exceptions.BadRequest(
                'Value must have "name=param" format')

        if name != ranges.RangesOptions.bytes:
            return cleaners.clean_params((raw_value,))

        # todo: setting.BYTES_RANGES_LIMIT
        return parameters.ParamsCI((
            (ranges.RangesOptions.bytes,
             tuple(
                 cleaners.clean_bytes_range(rp)
                 for rp in raw_param_value.split(',', 20))),))
