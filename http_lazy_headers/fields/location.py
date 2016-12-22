# -*- coding: utf-8 -*-

from ..shared import bases


class Location(bases.URIHeaderBase):
    """
    Sent by server only.

    The ``Location`` header field is used in\
    some responses to refer to a specific\
    resource in relation to the response.\
    The type of relationship is defined by the\
    combination of request method and status\
    code semantics.

    Example::

        Location(['/People.html#tim'])

        Location(['http://www.example.net/index.html'])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.location>`_
    """

    name = 'location'
