# -*- coding: utf-8 -*-

import datetime

from ..shared import bases
from ..shared import dates


class IfUnmodifiedSince(bases.SingleHeaderBase):
    """
    Sent by client only.

    The ``If-Unmodified-Since`` header field makes the request\
    method conditional on the selected representation's\
    last modification date being earlier than or equal to\
    the date provided in the field-value. This field\
    accomplishes the same purpose as If-Match for cases\
    where the user agent does not have an entity-tag for\
    the representation.

    Example::

        IfUnmodifiedSince([
            datetime.datetime.now() - datetime.timedelta(days=1)
        ])

    `Ref. <http://httpwg.org/specs/rfc7232.html#header.if-unmodified-since>`_
    """

    name = 'if-unmodified-since'

    def values_str(self, values):
        return dates.format_date(values[0])

    def clean_value(self, raw_value):
        # This header should be ignore if
        # the date is not valid, but since
        # we can not do that here, max is
        # close to the expected behaviour
        # (i.e always unmodified)
        return dates.clean_date_time(
            raw_value, default=datetime.datetime.max)
