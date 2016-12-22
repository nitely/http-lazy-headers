# -*- coding: utf-8 -*-

from ..shared import bases


class AcceptRanges(bases.TokensHeaderBase):
    """
    Sent by Server only.

    The ``Accept-Ranges`` header field allows a\
    server to indicate that it supports range\
    requests for the target resource.

    Example::

        AcceptRanges([Ranges.bytes])

        AcceptRanges(['bytes'])

    `Ref. <http://httpwg.org/specs/rfc7233.html#header.accept-ranges>`_
    """

    name = 'accept-ranges'
    ranges = frozenset((
        'bytes',
        'none'))  # todo: warning if not one of these
