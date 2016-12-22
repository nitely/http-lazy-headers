# -*- coding: utf-8 -*-

import datetime

from ..shared import bases
from ..shared import dates


class IfModifiedSince(bases.SingleHeaderBase):
    """
    Sent by client only.

    The ``If-Modified-Since`` header field makes a\
    GET or HEAD request method conditional on the\
    selected representation's modification date being\
    more recent than the date provided in the\
    field-value. Transfer of the selected\
    representation's data is avoided if that data has\
    not changed.

    Example::

        IfModifiedSince([
            datetime.datetime.now() - datetime.timedelta(days=1)
        ])

    `Ref. <http://httpwg.org/specs/rfc7232.html#header.if-modified-since>`_
    """

    name = 'if-modified-since'

    def values_str(self, values):
        return dates.format_date(values[0])

    def clean_value(self, raw_value):
        # This header should be ignore if
        # the date is not valid, but since
        # we can not do that here, min is
        # close to the expected behaviour
        # (i.e always modified)
        return dates.clean_date_time(
            raw_value, default=datetime.datetime.min)
