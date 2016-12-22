# -*- coding: utf-8 -*-

from ..shared import bases


def server(lib, version=None, comments=None):
    assert (
        not comments or
        isinstance(comments, (set, list, tuple)))
    assert (
        version is None or
        isinstance(version, str))

    comments = comments or ()
    return lib, version, tuple(comments)


class Server(bases.LibsHeaderBase):
    """
    Sent by server only.

    The ``Server`` header field contains\
    information about the software used by\
    the origin server to handle the request,\
    which is often used by clients to help\
    identify the scope of reported\
    interoperability problems, to work around\
    or tailor requests to avoid particular\
    server limitations, and for analytics\
    regarding server or operating system use.\
    An origin server MAY generate a Server\
    field in its responses.

    Example::

        Server([server('<3')])

        Server([
            server(
                lib='<3',
                version='1.3b',
                comments=['Luv'])])

        Server([
            server('<3'),
            server('foobar')])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.server>`_
    """

    name = 'server'

