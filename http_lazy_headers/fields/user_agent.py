# -*- coding: utf-8 -*-

from ..shared import bases
from . import server


user_agent = server.server


class UserAgent(bases.LibsHeaderBase):
    """
    Sent by client only.

    Comments are striped from values.

    The "User-Agent" header field contains\
    information about the user agent originating\
    the request, which is often used by servers to\
    help identify the scope of reported\
    interoperability problems, to work around or\
    tailor responses to avoid particular user agent\
    limitations, and for analytics regarding browser\
    or operating system use. A user agent SHOULD\
    send a User-Agent field in each request unless\
    specifically configured not to do so.

    Example::

        UserAgent([
            user_agent('<3')
        ])

        UserAgent([
            user_agent(
                lib='<3',
                version='1.3b',
                comments=['Luv'])
        ])

        UserAgent([
            user_agent('<3'),
            user_agent('foobar')
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.user-agent>`_
    """

    name = 'user-agent'
