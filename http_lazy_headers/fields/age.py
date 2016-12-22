# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import cleaners


class Age(bases.SingleHeaderBase):
    """
    Sent by (cache) server only.

    The ``Age`` header field conveys the\
    sender's estimate of the amount of time\
    since the response was generated or\
    successfully validated at the origin\
    server.

    Example::

        Age([60])

    `Ref. <http://httpwg.org/specs/rfc7234.html#header.age>`_
    """

    name = 'age'

    def values_str(self, values):
        return str(values[0])

    def clean_value(self, raw_value):
        return cleaners.clean_delta_seconds(raw_value)
