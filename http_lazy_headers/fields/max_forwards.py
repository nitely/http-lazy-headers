# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import cleaners


class MaxForwards(bases.SingleHeaderBase):
    """
    Sent by client only.

    The ``Max-Forwards`` header field provides a\
    mechanism with the TRACE and OPTIONS request\
    methods to limit the number of times that the\
    request is forwarded by proxies. This can be\
    useful when the client is attempting to trace\
    a request that appears to be failing or looping\
    mid-chain.

    Example::

        MaxForwards([2])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.max-forwards>`_
    """

    name = 'max-forwards'

    def values_str(self, values):
        return str(values[0])

    def clean_value(self, raw_value):
        return cleaners.clean_number(raw_value, max_chars=4)
