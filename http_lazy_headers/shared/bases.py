# -*- coding: utf-8 -*-

from ..shared import ascii_tools
from . import checkers
from . import cleaners
from . import constraints
from . import helpers
from . import parsers
from . import quality
from .. import exceptions
from ..settings import settings


# HTAB / SP / VCHAR
_B_HEADER_VALUE_CHARS = frozenset(
    ascii_tools.ascii_bytes(0x09, (0x20, 0x7E)))
_U_HEADER_VALUE_CHARS = frozenset(
    ascii_tools.ascii_chars(0x09, (0x20, 0x7E)))


def is_value(raw_value):
    assert isinstance(raw_value, (str, bytes))

    if isinstance(raw_value, bytes):
        return set(raw_value).issubset(_B_HEADER_VALUE_CHARS)
    else:
        return set(raw_value).issubset(_U_HEADER_VALUE_CHARS)


def decode_one(raw_values):
    if not isinstance(raw_values, bytes):
        return raw_values

    try:
        return str(raw_values, 'latin1')
    except UnicodeDecodeError:
        raise exceptions.BadRequest(
            'Value can\'t be decoded')


def pre_clean(strings_collection):
    total_len = 0

    for rvs in strings_collection:
        total_len += len(rvs)

        if total_len > settings.HEADER_MAX_LEN:
            raise exceptions.HeaderError(
                'Value is too long', status=431)

        if not is_value(rvs):
            raise exceptions.BadRequest(
                'Value chars are not valid')

        yield decode_one(rvs)


class HeaderBase:

    name = None

    def __init__(
            self,
            values=None,
            raw_values_collection=None):
        assert (
            values is not None or
            raw_values_collection is not None)
        assert (
            raw_values_collection is None or
            isinstance(
                raw_values_collection,
                (tuple, list)))

        if values is not None:
            values = tuple(values)

        self._values = values
        self._raw_values_collection = raw_values_collection

    def __repr__(self):
        name = self.__class__.__name__

        if self._raw_values_collection is not None:
            return '{}(raw_values_collection={})'.format(
                name, self._raw_values_collection)

        if self._values is not None:
            return '{}({})'.format(name, self._values)

        return '{}()'.format(name)

    def __str__(self):
        return ': '.join((
            self.name,
            self.values_str(self.values())))

    def values(self):
        self.validate()
        return self._values

    def validate(self):
        if self._raw_values_collection is None:
            return

        try:
            self._values = self.clean(
                self.prepare_raw_values(
                    pre_clean(self._raw_values_collection)))
        except exceptions.HeaderError as err:
            err.explanation = '{}: {}'.format(
                self.name, err.explanation)
            raise

        self._raw_values_collection = None

    def check_values(self, values):
        raise NotImplementedError

    def values_str(self, values):
        raise NotImplementedError

    def prepare_raw_values(self, raw_values_collection):
        raise NotImplementedError

    def clean(self, raw_values):
        raise NotImplementedError


class MultiHeaderBase(HeaderBase):

    def values_str(self, values):
        return ', '.join(values)

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, raw_value):
        raise NotImplementedError

    def clean(self, raw_values):
        values = tuple(
            self.clean_value(rv)
            for rv in raw_values)
        constraints.must_not_be_empty(values)
        return values


class SingleHeaderBase(HeaderBase):
    """
    Single Value Header
    """

    def __init__(
            self,
            values=None,
            raw_values_collection=None):
        super().__init__(values, raw_values_collection)
        assert (
            self._values is None or
            len(self._values) == 1)

    def values_str(self, values):
        return values[0]

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_single_raw_values(raw_values_collection)

    def clean_value(self, raw_value):
        raise NotImplementedError

    def clean(self, raw_values):
        raw_value = raw_values[0]
        constraints.must_not_be_empty(raw_value)
        return (
            self.clean_value(raw_value),)


class URIHeaderBase(SingleHeaderBase):

    def clean_value(self, raw_value):
        constraints.must_be_uri(raw_value)
        return raw_value


class TokensHeaderBase(MultiHeaderBase):

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_tokens(raw_values_collection)

    def clean_value(self, raw_value):
        constraints.must_be_token(raw_value)
        return raw_value.lower()


class IfMatchSomeBase(MultiHeaderBase):
    """
    Sent by client only.

    Format::

        if_match.values()
        # (('foo', False), )

    """

    def values_str(self, values):
        etag, is_weak = values[0]

        if etag == '*':
            return etag

        return ', '.join(helpers.format_etag_values(values))

    def clean_value(self, raw_value):
        # todo: validate is single value when value is "*"

        if raw_value == '*':
            return raw_value, False

        return cleaners.clean_etag(raw_value)

    def match(self, etag, is_weak=False):
        values = set(self.values())
        return ((etag, is_weak) in values or
                ('*', False) in values)


class AcceptSomeBase(HeaderBase):

    # todo: remove, no header use this as is (well just one)

    def values_str(self, values):
        return ', '.join(
            helpers.format_values_with_params(values))

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_tokens(raw_values_collection)

    def clean_value(self, value):
        return cleaners.clean_accept_some(value)

    def clean(self, raw_values):
        values = tuple(sorted(
            (
                self.clean_value(raw_value)
                for raw_value in raw_values),
            key=quality.quality_sort_key))

        constraints.must_not_be_empty(values)

        return values

    def first_of(self, values):
        return quality.first_of(self.values(), values)

    def best_of(self, values):
        return quality.best_of(self.values(), values)


class LibsHeaderBase(HeaderBase):

    def value_str(self, value):
        lib, version, comments = value

        if version:
            lib = '{lib}/{version}'.format(
                lib=lib,
                version=version)

        if comments:
            lib = '{lib} {comments}'.format(
                lib=lib,
                comments=' '.join(
                    parsers.quote_comment(c)
                    for c in comments))

        return lib

    def values_str(self, values):
        return ' '.join(
            self.value_str(v)
            for v in values)

    def prepare_raw_values(self, raw_values_collection):
        raw_values_collection = helpers.prepare_single_raw_values(
            raw_values_collection)
        return parsers.from_raw_values(
            raw_values_collection[0],
            separator=' ')

    def clean_value(self, raw_value):
        try:
            product, version = raw_value.split('/', 1)
        except ValueError:
            constraints.must_be_token(raw_value)
            return raw_value, None, ()
        else:
            constraints.must_be_token(product)
            constraints.must_be_token(version)
            return product, version, ()

    def clean(self, raw_values):
        # Skip comments
        values = tuple(
            self.clean_value(raw_value)
            for raw_value in raw_values
            if not checkers.is_comment(raw_value))

        constraints.must_not_be_empty(values)

        return values
