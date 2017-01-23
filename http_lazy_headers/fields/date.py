# -*- coding: utf-8 -*-

from ..shared import bases


class Date(bases.DateSomeBase):
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
