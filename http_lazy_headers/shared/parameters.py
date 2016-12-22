# -*- coding: utf-8 -*-

import collections

from . import parsers


class Params:
    """
    An immutable DS for header-value parameters.
    """

    def __init__(self, params=None):
        self._params = collections.OrderedDict(params or ())

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            tuple(self.items()))

    def __str__(self):
        return self.as_str()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return tuple(self.items()) == tuple(other.items())

    def __contains__(self, key):
        return key in self._params

    def __iter__(self):
        return self._params.keys()

    def __getitem__(self, key):
        return self._params[key]

    def __len__(self):
        return len(self._params)

    def as_str(self, separator=';'):
        separator = ''.join((
            separator.strip(),
            ' '))

        return separator.join(
            '='.join((
                p,
                parsers.quote_maybe(str(v))))
            for p, v in self.items())

    def items(self):
        return self._params.items()

    def merge(self, other):
        """
        Return a copy of the params\
        with the updated fields.

        :param dict other: A dict with\
        immutable key-values
        :return: Params instance
        """
        params = self.__class__()
        params._params = self._params.copy()
        params._params.update(other)
        return params


class ParamsCI(Params):
    """
    Case-insensitive params.\
    Values are case-sensitive.
    """

    def __init__(self, params=None):
        if isinstance(params, dict):
            params = params.items()

        super().__init__(
            (p.lower(), v)
            for p, v in params or ())
