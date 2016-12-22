# -*- coding: utf-8 -*-

from ..shared import bases


class ConnectionOptions:

    keep_alive = 'keep-alive'
    close = 'close'


class Connection(bases.TokensHeaderBase):
    """
    The ``Connection`` header field allows the\
    sender to indicate desired control options\
    for the current connection. In order to avoid\
    confusing downstream recipients, a proxy or\
    gateway MUST remove or replace any received\
    connection options before forwarding the message.

    Example::

        Connection([
            ConnectionOptions.keep_alive])

        Connection([
            ConnectionOptions.close])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.connection>`_
    """

    name = 'connection'
