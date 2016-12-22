# -*- coding: utf-8 -*-

from . import parser


def from_wsgi(headers):
    """
    Convert WSGI raw headers
    into lazy ``Headers``.

    Usage::

        from_wsgi([
            ('Content-Length', '100, 100'),
            ('Accept', 'text/html')])
        # Headers((
        #    ('Content-Length', '100'),
        #    ('Accept', 'text/html')))

    :param headers:
    :return:
    """
    return parser.to_headers(
        (h.lower(), (v, ))
        for h, v in headers)


def from_environ(environ):
    return from_wsgi(
        (k[5:], v)
        for k, v in environ.items()
        if k.startswith('HTTP_'))


def to_wsgi(headers):
    """
    Convert ``Headers`` into WSGI\
    compatible headers.

    This is meant to be used to\
    pass the headers to a WSGI server\
    as a response.

    Usage::

        to_wsgi(
            Headers([
                ContentLength((100, )),
                Accept(('text/html', ))]))
        # [('content-length', '100')]

    :param headers: ``Headers`` collection
    :return: Headers list
    """
    # todo: set-cookie in multiple headers
    wsgi_headers = []

    for header in headers:
        wsgi_headers.append(
            (header.name, header.values_str()))

    return wsgi_headers
