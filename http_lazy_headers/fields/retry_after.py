# -*- coding: utf-8 -*-

import datetime

from .. import exceptions
from ..shared import bases
from ..shared import cleaners
from ..shared import dates


class RetryAfter(bases.SingleHeaderBase):
    """
    Sent by server only.

    Servers send the ``Retry-After`` header field\
    to indicate how long the user agent ought to\
    wait before making a follow-up request. When\
    sent with a 503 (Service Unavailable) response,\
    Retry-After indicates how long the service is\
    expected to be unavailable to the client. When\
    sent with any 3xx (Redirection) response,\
    Retry-After indicates the minimum time that the\
    user agent is asked to wait before issuing the\
    redirected request.

    Example::

        RetryAfter([10])

        RetryAfter([
            datetime.datetime.now() + datetime.timedelta(seconds=10)])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.retry-after>`_
    """

    name = 'retry-after'

    def values_str(self, values):
        value = values[0]

        if isinstance(value, datetime.datetime):
            return dates.format_date(value)
        else:
            return str(value)

    def clean_value(self, raw_value):
        try:
            return dates.clean_date_time(raw_value)
        except exceptions.HeaderError:
            return cleaners.clean_delta_seconds(raw_value)
