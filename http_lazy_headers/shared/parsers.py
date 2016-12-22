# -*- coding: utf-8 -*-

from ..settings import settings
from . import checkers
from .. import exceptions


_QUOTE_OR_COMMENT_CHARS_MAP = {'"': '"', '(': ')'}


def from_raw(raw_values, max_values, separator=','):
    """
    This works just like the built-in ``str.split()``,\
    except it's aware of ``quoted-strings`` and\
    ``comments``, so it won't split them.

    Example::

        parse_values_list('foo, bar, baz', max_values=10)
        # ('foo', 'bar', 'baz')

        parse_values_list('"foo, bar", baz', max_values=10)
        # ('"foo, bar"', 'baz')

        parse_values_list('foo "baz, qux" bar', max_values=10, separator=' ')
        # ('foo', '"baz, qux"', 'bar')

        parse_values_list('foo (baz, qux) bar', max_values=10, separator=' ')
        # ('foo', '(baz, qux)', 'bar')

        parse_values_list('', max_values=10)
        # ('',)

        parse_values_list(',', max_values=10)
        # ('', '')

    """
    start_i = 0
    escape = False
    quote_or_comment_char = None
    values_count = 0

    for curr_i, char in enumerate(raw_values):
        if values_count >= max_values:
            raise exceptions.BadRequest('Too many values')

        if escape:
            escape = False
            continue

        if quote_or_comment_char:
            if char == '\\':
                escape = True

            if char == quote_or_comment_char:
                quote_or_comment_char = None

            continue

        if char in _QUOTE_OR_COMMENT_CHARS_MAP:
            quote_or_comment_char = _QUOTE_OR_COMMENT_CHARS_MAP[char]
            continue

        if char == separator:
            yield raw_values[start_i:curr_i].strip()
            start_i = curr_i + 1  # + skip separator
            values_count += 1

    # If start is zero and there are
    # no spaces, this won't copy the str
    yield raw_values[start_i:].strip()


def from_raw_values(raw_values, separator=','):
    return (
        rv
        for rv in from_raw(
            raw_values,
            max_values=settings.HEADER_VALUES_MAX,
            separator=separator)
        if rv)


def from_raw_params(raw_params, separator=';'):
    return from_raw(
        raw_params,
        max_values=settings.VALUE_PARAMS_MAX,
        separator=separator)


def from_raw_value_with_params(raw_value, separator=';'):
    raw_value_params = from_raw_params(raw_value, separator)
    return (
        next(raw_value_params, ''),
        raw_value_params)


def from_tokens(raw_tokens, separator=','):
    """
    This is an optimization of ``from_raw_values``\
    for the special ``tokens`` case.

    Use it over ``from_raw_values`` when the header's\
    values don't allow ``quoted-string`` anywhere.

    :param raw_tokens:
    :param separator:
    :return:
    """
    tokens = raw_tokens.split(
        sep=separator,
        maxsplit=settings.HEADER_VALUES_MAX + 1)

    if len(tokens) > settings.HEADER_VALUES_MAX:
        raise exceptions.BadRequest('Too many tokens')

    for token in tokens:
        token = token.strip()

        if token:
            yield token


def dequote(raw_value):
    """
    :param raw_value:
    :return:
    """
    assert checkers.is_quoted_string(raw_value)

    return (raw_value
            .replace('\\"', '"')
            .replace('\\\\', '\\')[1:-1])


def dequote_comment(raw_value):
    """

    :param raw_value:
    :return:
    """
    assert checkers.is_comment(raw_value)

    return (raw_value
            .replace('\\(', '(')
            .replace('\\)', ')')
            .replace('\\\\', '\\')[1:-1])


def dequote_DEPRECATED(raw_value):
    """
    This won't validate whether the\
    raw_value is a quoted-string or\
    a token, so make sure\
    ``is_quoted`` or ``is_comment``

    :param raw_value:
    :return:
    """
    # todo split into dequote and uncomment?
    # todo: raise if quotes_count > 1 (ie: don't allow '"foo" bar "foo"')

    assert (
        checkers.is_quoted_string(raw_value) or
        checkers.is_comment(raw_value)), (
        'Not a quoted-string nor a comment')

    part = []
    escape = False
    quote_or_comment = False
    quote_or_comment_char = ''

    for char in raw_value:
        if escape:
            part.append(char)
            escape = False
            continue

        if quote_or_comment:
            if char == '\\':
                escape = True
                continue

            if char == quote_or_comment_char:
                quote_or_comment = False
                quote_or_comment_char = ''
                continue

            part.append(char)

        if char in _QUOTE_OR_COMMENT_CHARS_MAP:
            quote_or_comment = True
            quote_or_comment_char = _QUOTE_OR_COMMENT_CHARS_MAP[char]

        part.append(char)

    return ''.join(part[1:-1])


def quote(raw_value):
    return '"{}"'.format(
        raw_value
        .replace('\\', '\\\\')
        .replace('"', '\\"'))


def quote_comment(raw_value):
    return '({})'.format(
        raw_value
        .replace('\\', '\\\\')
        .replace('(', '\\(')
        .replace(')', '\\)'))


def quote_maybe(raw_value):
    assert isinstance(raw_value, str)

    if checkers.is_token(raw_value):
        return raw_value

    return quote(raw_value)
