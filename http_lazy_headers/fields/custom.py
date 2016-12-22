# -*- coding: utf-8 -*-

from .. import exceptions
from ..shared import bases
from ..shared import checkers


_B_TOKEN_CHARS = frozenset(
    bytes(c, 'latin1')
    for c in checkers._TOKEN_CHARS)


def is_token(txt):
    assert isinstance(txt, (str, bytes))

    if not txt:
        return False

    if isinstance(txt, bytes):
        return set(txt).issubset(_B_TOKEN_CHARS)
    else:
        return checkers.is_token(txt)


class Custom(bases.HeaderBase):
    """
    The ``Custom`` header provides simple\
    parsing for unknown headers with comma\
    separated values.

    May not have values (ie: empty field).

    Example::

        Custom(['foo', 'bar'])

    """

    def __init__(
            self,
            name,
            values=None,
            raw_values_collection=None):
        super().__init__(
            values=values,
            raw_values_collection=raw_values_collection)

        if not is_token(name):
            raise exceptions.HeaderError(
                'Header name must '
                'be a valid token')

        self.name = bases.decode_one(name).lower()  # Override class var

    def values_str(self, values):
        return ', '.join(values)

    def prepare_raw_values(self, raw_values_collection):
        return raw_values_collection

    def clean(self, raw_values):
        return tuple(raw_values)
