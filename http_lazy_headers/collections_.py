# -*- coding: utf-8 -*-

import collections

from .shared import bases


_CLRF = '\r\n'


class Headers:
    """
    Headers collection
    """

    def __init__(self, headers=None):
        assert all(
            isinstance(h, bases.HeaderBase)
            for h in headers or ())

        self._headers = collections.OrderedDict(
            (h.name, h)
            for h in headers or ())

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            str(self))

    def __str__(self):
        return ''.join((
            _CLRF.join(
                str(header)
                for header in self.fields()),
            _CLRF))

    def __contains__(self, key):
        assert isinstance(key, bases.HeaderBase)

        return key.name in self._headers

    def __getitem__(self, key):
        assert isinstance(key, bases.HeaderBase)

        return self._headers[key.name]

    def __iter__(self):
        return self._headers.values()

    def __len__(self):
        return len(self._headers)

    def fields(self):
        return self._headers.values()

    def get(self, header, *args):
        assert isinstance(header, bases.HeaderBase)

        if args:
            return self._headers.get(
                header.name, *args)
        else:
            return self._headers[header.name]


class HeadersMut(Headers):

    def set(self, header):
        assert isinstance(header, bases.HeaderBase)

        self._headers[header.name] = header

    def pop(self, header, default=None):
        assert isinstance(header, bases.HeaderBase)

        return self._headers.pop(
            header.name, default)

    def clear(self):
        self._headers.clear()

    def frozen_copy(self):
        headers = Headers()
        headers._headers = self._headers.copy()
        return headers
