# -*- coding: utf-8 -*-

from ..shared import bases


class Referer(bases.URIHeaderBase):
    """
    Sent by client only.

    Almost anything can be a valid\
    URI (absolute or relative),\
    so this won't validate it.

    The ``Referer`` [sic] header field allows\
    the user agent to specify a URI reference\
    for the resource from which the target URI\
    was obtained (i.e., the "referrer", though\
    the field name is misspelled). A user agent\
    MUST NOT include the fragment and userinfo\
    components of the URI reference, if any,\
    when generating the Referer field value.

    Example::

        Referer(['/People.html#tim'])

        Referer(['http://www.example.net/index.html'])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.referer>`_
    """

    name = 'referer'
