# -*- coding: utf-8 -*-

from ..shared import bases


class ContentLocation(bases.URIHeaderBase):
    """
    Sent by server only.

    A canonical URI.

    The ``Content-Location`` header field references\
    a URI that can be used as an identifier for a\
    specific resource corresponding to the\
    representation in this message's payload. In other\
    words, if one were to perform a GET request on\
    this URI at the time of this message's generation,\
    then a 200 (OK) response would contain the same\
    representation that is enclosed as payload in this\
    message.

    Example::

        ContentLocation(['rfc7231.html'])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.content-location>`_
    """

    name = 'content-location'
