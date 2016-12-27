# -*- coding: utf-8 -*-


class HTTPLazyHeadersError(Exception):
    """
    Base exception for any other\
    (custom) exception raised by this library
    """

    status = 500


class InternalError(HTTPLazyHeadersError):
    """"""


class HeaderError(HTTPLazyHeadersError):
    """
    This is raised by ``fields`` while\
    parsing/validating headers
    """

    def __init__(self, explanation='', status=None, **kwargs):
        if status:
            self.status = status

        self.explanation = explanation
        super().__init__(
            self.explanation,
            **kwargs)


class BadRequest(HeaderError):

    status = 400
