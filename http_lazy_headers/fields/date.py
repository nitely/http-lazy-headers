# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import dates


class Date(bases.SingleHeaderBase):
    """
    The ``Date`` header field represents\
    the date and time at which the message was originated.

    Example::

        Date([
            datetime.now()
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.date>`_
    """

    name = 'date'

    def values_str(self, values):
        return dates.format_date(values[0])

    def clean_value(self, raw_value):
        return dates.clean_date_time(raw_value)
