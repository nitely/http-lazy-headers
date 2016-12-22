# -*- coding: utf-8 -*-

import datetime

from .. import exceptions
from . import cleaners
from . import constraints


_DAYS = (
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday')

_WEEK_DAYS = {
    d: n
    for n, d in enumerate(_DAYS)}

_WEEK_DAYS_SHORT = {
    d[:3]: n
    for n, d in enumerate(_DAYS)}

_WEEK_DAYS_SHORT_NUM = {
    v: k
    for k, v in _WEEK_DAYS_SHORT.items()}

_MONTHS = {
    m: n + 1
    for n, m in enumerate((
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'))}

_MONTHS_NUM = {
    v: k
    for k, v in _MONTHS.items()}

_IMF_FIXDATE_LEN = len('Ddd, dd Mmm YYYY HH:MM:SS GMT')

_RFC_850_DATE_MIN_LEN = (
    min(len(d) for d in _DAYS) +
    len(', dd-Mmm-yy hh:mm:ss GMT'))
_RFC_850_DATE_MAX_LEN = (
    max(len(d) for d in _DAYS) +
    len(', dd-Mmm-yy hh:mm:ss GMT'))

_ASCTIME_LEN = len('Ddd Mmm xd hh:mm:ss yyyy')


def _clean_time(raw_time):
    try:
        hh, mm, ss = raw_time.split(':', 2)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected HH:MM:SS format')

    constraints.constraint(
        (len(hh), len(mm), len(ss)) == (2, 2, 2),
        'Expected HH:MM:SS')

    return (
        cleaners.clean_number(hh),
        cleaners.clean_number(mm),
        cleaners.clean_number(ss))


def _to_datetime(week_day, year, month, day, hh, mm, ss):
    try:
        date_time = datetime.datetime(
            year, month, day, hh, mm, ss)
    except ValueError:
        raise exceptions.BadRequest(
            'Bad date time')

    constraints.constraint(
        date_time.weekday() == week_day,
        'Bad week day')

    return date_time


def clean_imf_fix_date(raw_date):
    # http://httpwg.org/specs/rfc7231.html#preferred.date.format

    # Python has some built-in date parsers
    # (email and datetime) but this is way
    # simpler, faster and securer

    constraints.constraint(
        len(raw_date) == _IMF_FIXDATE_LEN,
        'Date value is not valid')

    try:
        week_day, day, month, year, time, tz = raw_date.split(' ', 5)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected "Ddd, dd Mmm YYYY '
            'HH:MM:SS GMT" format')

    constraints.constraint(
        tz == 'GMT',
        'Time-zone is not valid')
    constraints.constraint(
        len(week_day) == 4 and
        week_day.endswith(','),
        'Week day is not valid')
    constraints.constraint(
        month in _MONTHS,
        'Month is not valid')
    constraints.constraint(
        len(day) == 2,
        'Day is not valid')
    constraints.constraint(
        len(year) == 4,
        'Year is not valid')

    try:
        week_day = _WEEK_DAYS_SHORT[week_day[:-1]]
    except KeyError:
        raise exceptions.BadRequest(
            'Week day is not a valid format')

    hh, mm, ss = _clean_time(time)

    # `Leap second` is not supported by
    # datetime, and it's pretty rare anyways,
    # this is a simple workaround
    # todo: this is fixed in py3.6, see PEP-495
    if ss == 60:
        ss = 59

    return _to_datetime(
        week_day=week_day,
        year=cleaners.clean_number(year),
        month=_MONTHS[month],
        day=cleaners.clean_number(day),
        hh=hh,
        mm=mm,
        ss=ss)


def clean_rfc_850_date(raw_date):
    constraints.constraint(
        (_RFC_850_DATE_MIN_LEN <=
         len(raw_date) <=
         _RFC_850_DATE_MAX_LEN),
        'Invalid date format')

    try:
        week_day, date, time, tz = raw_date.split(' ', 3)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected "Ddddddd, dd-Mmm-yy '
            'hh:mm:ss GMT" format')

    constraints.constraint(
        tz == 'GMT',
        'Time-zone is not valid')
    constraints.constraint(
        week_day.endswith(','),
        'Week day is not valid')

    try:
        week_day = _WEEK_DAYS[week_day[:-1]]
    except KeyError:
        raise exceptions.BadRequest(
            'Week day is not a valid format')

    try:
        day, month, year = date.split('-', 2)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected "dd-Mmm-yy" format')

    constraints.constraint(
        month in _MONTHS,
        'Month is not valid')
    constraints.constraint(
        len(day) == 2,
        'Day is not valid')
    constraints.constraint(
        len(year) == 2,
        'Year is not valid')

    hh, mm, ss = _clean_time(time)

    # No `leap second`
    constraints.constraint(
        0 <= ss <= 59,
        'Seconds must be in between 0-59')

    year = cleaners.clean_number(year)

    # This is how year should be treated
    # according to rfc6265, hopefully
    # rfc850 will be completely unsupported
    # before 2068y arrives
    if year > 68:  # 1969-1999
        year += 1900
    else:  # 2000-2068
        year += 2000

    return _to_datetime(
        week_day=week_day,
        year=year,
        month=_MONTHS[month],
        day=cleaners.clean_number(day),
        hh=hh,
        mm=mm,
        ss=ss)


def clean_asctime_date(raw_date):
    # Sun Nov  7 08:48:37 1994
    # Sun Nov 17 08:48:37 1994

    constraints.constraint(
        len(raw_date) == _ASCTIME_LEN,
        'Invalid date format')

    try:
        week_day, month, raw_date = raw_date.split(' ', 2)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected "Ddd Mmm xd '
            'hh:mm:ss yyyy" format')

    if raw_date.startswith(' '):
        raw_date = raw_date[1:]

    try:
        day, time, year = raw_date.split(' ', 2)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected "Ddd Mmm xd '
            'hh:mm:ss yyyy" format')

    constraints.constraint(
        week_day in _WEEK_DAYS_SHORT,
        'Week day is not valid')
    constraints.constraint(
        month in _MONTHS,
        'Month is not valid')
    constraints.constraint(
        len(day) in {1, 2},
        'Day is not valid')
    constraints.constraint(
        len(year) == 4,
        'Year is not valid')

    hh, mm, ss = _clean_time(time)

    # No `leap second`
    constraints.constraint(
        0 <= ss <= 59,
        'Seconds must be in between 0-59')

    return _to_datetime(
        week_day=_WEEK_DAYS_SHORT[week_day],
        year=cleaners.clean_number(year),
        month=_MONTHS[month],
        day=cleaners.clean_number(day),
        hh=hh,
        mm=mm,
        ss=ss)


def _clean_date_time(raw_date_time):
    assert (
        _ASCTIME_LEN <
        _IMF_FIXDATE_LEN <
        _RFC_850_DATE_MIN_LEN)

    raw_date_time_len = len(raw_date_time)

    if raw_date_time_len == _ASCTIME_LEN:
        return clean_asctime_date(raw_date_time)

    if raw_date_time_len >= _RFC_850_DATE_MIN_LEN:
        return clean_rfc_850_date(raw_date_time)

    # Default to the preferred date-time
    return clean_imf_fix_date(raw_date_time)


def clean_date_time(raw_date_time, **default):
    assert (
        not default or
        (len(default) == 1 and
         'default' in default))

    try:
        return _clean_date_time(raw_date_time)
    except exceptions.HeaderError:
        if default:
            return default['default']

        raise


def format_date(date_time):
    assert isinstance(date_time, datetime.datetime)

    # There is a `strftime()` but
    # it's locale dependent
    return (
        '{week_day}, {day:02} {month} {year} '
        '{hour:02}:{minute:02}:{second:02} GMT'.format(
            week_day=_WEEK_DAYS_SHORT_NUM[date_time.weekday()],
            day=date_time.day,
            month=_MONTHS_NUM[date_time.month],
            year=date_time.year,
            hour=date_time.hour,
            minute=date_time.minute,
            second=date_time.second))
