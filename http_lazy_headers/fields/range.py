# -*- coding: utf-8 -*-

from ..shared.generic import cleaners
from .. import exceptions
from ..shared import bases
from ..shared.utils import assertions
from ..shared.utils import constraints
from ..shared.utils import checkers
from ..shared.values import ranges


def range_bytes(sub_ranges):
    assert sub_ranges
    assert all(
        len(sr) == 2
        for sr in sub_ranges)

    return (
        (ranges.RangesOptions.bytes, tuple(sub_ranges)),)


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
            (Ranges.bytes, ((0, 499),))
        ])

        Range([
            (Ranges.bytes, ((0, 499), (500, 999)))
        ])

        Range([
            ('my_unit', 'my_sub_range')
        ])

    `Ref. <http://httpwg.org/specs/rfc7233.html#header.range>`_
    """

    name = 'range'

    def check_value(self, value):
        assertions.must_be_tuple_of(value, 2)

        unit, unit_range = value

        if unit != ranges.RangesOptions.bytes:
            assertions.must_be_token(unit)
            assertions.must_be_visible_chars(unit_range)
            return

        assertions.must_be_instance_of(unit_range, tuple)
        assertions.assertion(
            all((isinstance(r, tuple) and
                 len(r) == 2 and
                 (r[0] is None or isinstance(r[0], int)) and
                 (r[1] is None or isinstance(r[1], int)))
                for r in unit_range),
            '"{}" received, a tuple of tuples of 2 '
            'ints were expected'.format(unit_range))
        assertions.assertion(
            all(r[0] is not None or
                r[1] is not None
                for r in unit_range),
            '"{}" received, start and/or end '
            'was expected'.format(unit_range))

    def values_str(self, values):
        unit, unit_range = values[0]

        if unit != ranges.RangesOptions.bytes:
            return '{}={}'.format(unit, unit_range)

        return '{}={}'.format(
            unit,
            ','.join(
                '{}-{}'.format(
                    start if start is not None else '',
                    end if end is not None else '')
                for start, end in unit_range))

    def clean_value(self, raw_value):
        try:
            name, raw_range = raw_value.split('=', 1)
        except ValueError:
            raise exceptions.BadRequest(
                'Value must have "name=param" format')

        if name != ranges.RangesOptions.bytes:
            constraints.must_be_token(name)
            constraints.constraint(
                checkers.is_visible_chars(raw_range),
                'Value must contain 1 or '
                'more visible chars')
            return name, raw_range

        # todo: setting.BYTES_RANGES_LIMIT
        ranges_ = tuple(
            cleaners.clean_bytes_range(r)
            for r in raw_range.split(',', 20))

        constraints.constraint(
            all(start is not None or
                end is not None
                for start, end in ranges_),
            'Unbounded range is not allowed, '
            'must have start and/or end')

        return (
            ranges.RangesOptions.bytes,
            ranges_)
