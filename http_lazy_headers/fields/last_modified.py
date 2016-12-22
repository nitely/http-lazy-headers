# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import dates


class LastModified(bases.SingleHeaderBase):
    """
    Sent by server only.

    The ``Last-Modified`` header field in a\
    response provides a timestamp indicating\
    the date and time at which the origin server\
    believes the selected representation was last\
    modified, as determined at the conclusion of\
    handling the request.

    Example::

        LastModified([
            datetime.datetime.now() - datetime.timedelta(days=1)
        ])

    `Ref. <http://httpwg.org/specs/rfc7232.html#header.last-modified>`_
    """

    name = 'last-modified'

    def values_str(self, values):
        return dates.format_date(values[0])

    def clean_value(self, raw_value):
        return dates.clean_date_time(raw_value)
