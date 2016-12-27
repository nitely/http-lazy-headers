# -*- coding: utf-8 -*-

from ..shared.generic import cleaners
from ..shared.utils import constraints
from .. import exceptions
from ..settings import settings
from ..shared import bases
from ..shared.values import ranges
from ..shared.utils import assertions


def content_range_bytes(
        start=None,
        end=None,
        length=None):
    """
    Shorthand for creating a\
    ContentRange value

    :param unit:
    :param start:
    :param end:
    :param length:
    :return:
    """
    return (
        ranges.RangesOptions.bytes,
        (start, end),
        length,
        None)


def content_range_none():
    return None, None, None, None


def content_range_bytes_unsatisfied(length=None):
    return ranges.RangesOptions.bytes, None, length, None


def content_range_other(unit, chars=''):
    # A SP after other-unit is required
    return unit, None, None, chars


class ContentRange(bases.SingleHeaderBase):
    """
    Sent by server only.

    Be aware, HTTP spec does not define\
    a way to resume uploads (i.e: client side).

    Creating values from the function helpers in\
    this module instead of passing a mystic\
    tuple is advised.

    The "Content-Range" header field is sent\
    in a single part 206 (Partial Content)\
    response to indicate the partial range of\
    the selected representation enclosed as the\
    message payload, sent in each part of a\
    multipart 206 response to indicate the range\
    enclosed within each body part, and sent in\
    416 (Range Not Satisfiable) responses to\
    provide information about the selected\
    representation.

    Example::

        ContentRange([
            ('bytes', (0, 100), 100, None)
        ])
        # content-range: bytes 0-100/100

        ContentRange([
            content_range_bytes(
                start=0,
                end=100,
                length=100)
        ])
        # content-range: bytes 0-100/100

        ContentRange([
            content_range_bytes(
                end=100,
                length=100)
        ])
        # content-range: bytes -100/100

        ContentRange([
            content_range_bytes(
                length=100)
        ])
        # content-range: bytes -/100

        ContentRange([
            content_range_bytes()
        ])
        # content-range: bytes -/*

        ContentRange([
            ('bytes', None, 100, None)  # Unsatisfied
        ])
        # content-range: bytes */100

        ContentRange([
            content_range_bytes_unsatisfied(
                length=100)
        ])
        # content-range: bytes */100

        ContentRange([
            ('my-unit', None, None, '0-100-200-400')
        ])
        # content-range: my-unit 0-100-200-400

        ContentRange([
            content_range_other(
                unit='my-unit',
                chars='0-100-200-400')
        ])
        # content-range: my-unit 0-100-200-400

        ContentRange([
            (None, None, None, None)
        ])
        # content-range: none

        ContentRange([
            content_range_none()
        ])
        # content-range: none

    `Ref. <http://httpwg.org/specs/rfc7233.html#header.content-range>`_
    """

    name = 'content-range'

    def check_value(self, value):
        unit, unit_range, length, chars = value

        if unit is None:
            assertions.assertion(
                all(not v
                    for v in value),
                '"{}" received, a unit was '
                'expected'.format(value))

            return

        if unit != ranges.RangesOptions.bytes:
            assertions.assertion(
                unit_range is None and
                length is None,
                '"{}" received, either unit '
                '\'bytes\' or no range and '
                'no length were expected'
                .format(value))

            return

        # Bytes

        start = None
        end = None

        if unit_range:
            start, end = unit_range

        assertions.assertion(
            start is None or
            isinstance(start, int),
            'Start range must be None or int')
        assertions.assertion(
            end is None or
            isinstance(end, int),
            'End range must be None or int')
        assertions.assertion(
            start is None or
            end is None or
            start <= end,
            '"{}" range received, '
            'start <= end was expected'
            .format(value))

        assertions.assertion(
            length is None or
            isinstance(length, int),
            'Length must be None or int')
        assertions.assertion(
            start is None or
            length is None or
            start <= length,
            '"{}" received, '
            'start <= length was expected'
            .format(value))
        assertions.assertion(
            end is None or
            length is None or
            end <= length,
            '"{}" received, '
            'end <= length was expected'
            .format(value))

    def values_str(self, values):
        unit, range_, length, chars = values[0]

        if not unit:
            return 'none'

        if unit != ranges.RangesOptions.bytes:
            return '{unit} {chars}'.format(
                unit=unit,
                chars=chars)

        if length is None:
            length = '*'

        if range_ is None:
            return '{unit} */{length}'.format(
                unit=unit,
                length=length)

        start, end = range_

        if start is None:
            start = ''

        if end is None:
            end = ''

        return '{unit} {start}-{end}/{length}'.format(
            unit=unit,
            start=start,
            end=end,
            length=length)

    def clean_value(self, raw_value):
        try:
            unit, chars = raw_value.split(' ', 1)
        except ValueError:
            unit = raw_value
            chars = ''

        constraints.must_be_token(unit)
        unit = unit.lower()

        if unit == ranges.RangesOptions.none:
            return content_range_none()

        if unit != ranges.RangesOptions.bytes:
            return content_range_other(unit, chars)

        try:
            range_, length = chars.split('/', 1)
        except ValueError:
            raise exceptions.BadRequest(
                'Expected "start-end/length"')

        if length == '*':
            length = None

        if length is not None:
            length = cleaners.clean_number(
                length,
                max_chars=settings.CONTENT_MAX_CHARS)

        if range_ == '*':
            return content_range_bytes_unsatisfied(length)

        return content_range_bytes(
            *cleaners.clean_bytes_range(range_),
            length=length)
