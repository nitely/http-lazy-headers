# -*- coding: utf-8 -*-

import datetime

from ..shared import bases
from ..shared import dates


class Expires(bases.SingleHeaderBase):
    """
    Sent by server only.

    The ``Expires`` header field gives the\
    date/time after which the response is\
    considered stale.

    Example::

        Expires([
            datetime.datetime.now() + datetime.timedelta(days=2)
        ])

        Expires([datetime.datetime.min])  # Expired

        Expires([0])  # Expired

    `Ref. <http://httpwg.org/specs/rfc7234.html#header.expires>`_
    """

    name = 'expires'

    def values_str(self, values):
        value = values[0]

        if isinstance(value, datetime.datetime):
            return dates.format_date(values[0])

        # Invalid date
        return str(value)

    def clean_value(self, raw_value):
        # Invalid dates are represented
        # as a time in the past
        return dates.clean_date_time(
            raw_value, default=datetime.datetime.min)
