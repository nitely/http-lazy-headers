# -*- coding: utf-8 -*-

from ..shared.utils import assertions
from ..shared.generic import cleaners
from ..shared import bases


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

    def check_one(self, value):
        assertions.must_be_int(value)

    def to_str(self, values):
        return str(values[0])

    def clean_one(self, raw_value):
        return cleaners.clean_number(raw_value, max_chars=4)
