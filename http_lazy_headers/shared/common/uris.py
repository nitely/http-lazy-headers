# -*- coding: utf-8 -*-

import collections

from ..utils import ascii_tools
from ..utils import constraints
from ... import exceptions

from . import hosts


__all__ = [
    'clean_uri']


_ALPHA = frozenset(
    ascii_tools.ascii_chars(
        (0x41, 0x5A),
        (0x61, 0x7A)))

_ALPHANUM = (
    frozenset(
        ascii_tools.ascii_chars((0x30, 0x39))) |
    _ALPHA)

# 0-9 / a-f / A-F
_HEXDIG = _ALPHANUM

# ALPHA / DIGIT / "+" / "-" / "."
_SCHEME = (
    _ALPHANUM |
    frozenset('+-.'))

# unreserved / sub-delims / "%" _HEXDIG / ":"
_USER_INFO = (
    _ALPHANUM |
    frozenset('-._~') |
    frozenset('!$&\'()*+,;=') |
    frozenset('%:'))

# unreserved / sub-delims / "%" _HEXDIG / ":" / "@"
# + "/"
_PATH_CHARS = (
    _ALPHANUM |
    frozenset('-._~') |
    frozenset('!$&\'()*+,;=') |
    frozenset('%:@/'))

# unreserved / sub-delims / "%" _HEXDIG / "@"
_NC_PATH_CHARS = (
    _PATH_CHARS -
    frozenset(':/'))

_QUERY_CHARS = (
    _PATH_CHARS |
    frozenset('?'))


def remove_dot_segments(path):
    # Ref: https://tools.ietf.org/html/rfc3986#section-5.2.4
    # Ref impl: https://gist.github.com/nitely/08ee70e3429d4f174a00aa06e5ebf68c

    assert isinstance(path, str)

    in_buff = collections.deque(path.split('/'))
    out_buff = []

    while in_buff:
        # ./ or ../ or . or ..
        if in_buff[0] in ('.', '..') and not out_buff:
            in_buff.popleft()

            # Last one?
            if len(in_buff) == 1 and not in_buff[0]:
                in_buff.popleft()

            continue

        # /.
        if in_buff[0] == '.':
            in_buff.popleft()

            if not in_buff:
                in_buff.appendleft('')

            continue

        # /..
        if in_buff[0] == '..':
            in_buff.popleft()

            if not in_buff:
                in_buff.appendleft('')

            if out_buff:
                out_buff.pop()

            if not out_buff:
                in_buff.appendleft('')

            continue

        out_buff.append(in_buff.popleft())

    return tuple(out_buff)


def _hier_part(user_info=None, host=None, path=None):
    assert any(
        v is not None
        for v in (user_info, host, path))

    return user_info, host, path


def is_scheme(txt):
    assert isinstance(txt, str)

    return (
        txt and
        txt[0] in _ALPHA and
        set(txt).issubset(_SCHEME))


def is_hex_encoded(txt):
    percent = False
    checked = 0

    # Check "% HEXDIG HEXDIG"
    for c in txt:
        if percent and c not in _HEXDIG:
            return False

        if percent:
            checked += 1

        if checked == 2:
            percent = False
            checked = 0

        if c == '%':
            percent = True

    return True


def is_user_info(txt):
    assert isinstance(txt, str)

    if not txt:
        return True

    return (
        set(txt).issubset(_USER_INFO) and
        is_hex_encoded(txt))


def is_path(raw_path):
    assert isinstance(raw_path, str)

    return set(raw_path).issubset(_PATH_CHARS)


def is_abempty(raw_path):
    assert isinstance(raw_path, str)

    if not raw_path:
        return True

    return (
        raw_path.startswith('/') and
        is_path(raw_path))


def is_absolute(raw_path):
    assert isinstance(raw_path, str)

    # Must start with "/" or "/segment"
    return (
        not raw_path.startswith('//') and
        raw_path.startswith('/') and
        is_path(raw_path))


def is_rootless(raw_path):
    assert isinstance(raw_path, str)

    return (
        raw_path and
        not raw_path.startswith('/') and
        is_path(raw_path))


def is_noscheme(raw_path):
    assert isinstance(raw_path, str)

    if not raw_path:
        return False

    try:
        first_segment, raw_path = raw_path.split('/', 1)
    except ValueError:
        return set(raw_path).issubset(_NC_PATH_CHARS)
    else:
        return (
            set(first_segment).issubset(_NC_PATH_CHARS) and
            set(raw_path).issubset(_PATH_CHARS))


def is_query(txt):
    assert isinstance(txt, str)

    return set(txt).issubset(_QUERY_CHARS)  # and is_hex_encoded(txt) ?


def clean_authority_path(raw_path):
    # https://tools.ietf.org/html/rfc3986#section-3.2

    constraints.constraint(
        raw_path.startswith('//'),
        'Authority URI must start with "//"')

    raw_path = raw_path[2:]

    try:
        userinfo, raw_path = raw_path.split('@', 1)
    except ValueError:
        userinfo = None
    else:
        constraints.constraint(
            is_user_info(userinfo),
            'Userinfo in authority URI is not valid')

    try:
        raw_host, path = raw_path.split('/', 1)
    except ValueError:
        raw_host = raw_path
        path = None
    else:
        constraints.constraint(
            is_abempty(path),
            'Authority URI "path-abempty" is not valid')

    return _hier_part(
        user_info=userinfo,
        host=hosts.clean_host(raw_host),
        path=path)


def clean_hierarchical_part(raw_path):
    if raw_path.startswith('//'):
        return clean_authority_path(raw_path)

    if raw_path.startswith('/'):
        constraints.constraint(
            is_absolute(raw_path),
            'Absolute path is not valid')
        return _hier_part(path=raw_path)

    if raw_path:
        constraints.constraint(
            is_rootless(raw_path),
            'Rootless path is not valid')
        return _hier_part(path=raw_path)

    return _hier_part(path='')


def clean_absolute_uri(raw_uri):
    # ABNF: https://tools.ietf.org/html/rfc3986#appendix-A
    # Scheme: https://tools.ietf.org/html/rfc3986#section-3.1

    try:
        scheme, raw_path = raw_uri.split(':', 1)
    except ValueError:
        raise exceptions.BadRequest(
            'Absolute path is not valid, '
            '"schema:path" was expected')

    constraints.constraint(
        is_scheme(scheme),
        'URI scheme is not valid')

    try:
        raw_path, query = raw_path.split('?', 1)
    except ValueError:
        query = None
    else:
        constraints.constraint(
            is_query(query),
            'URI query is not valid')

    # Scheme must be lowered,
    # also when formatting
    return (
        scheme.lower(),
        clean_hierarchical_part(raw_path),
        query)


def clean_relative_part(raw_path):
    # https://tools.ietf.org/html/rfc3986#section-4.2

    if raw_path.startswith('//'):
        return clean_authority_path(raw_path)

    if raw_path.startswith('/'):
        constraints.constraint(
            is_absolute(raw_path),
            'Rel URI "path-absolute" is not valid')
        return _hier_part(path=raw_path)

    if raw_path:
        constraints.constraint(
            is_noscheme(raw_path),
            'Rel URI "path-noscheme" is not valid')
        return _hier_part(path=raw_path)

    return _hier_part(path='')


def clean_relative_uri(raw_uri):
    # https://tools.ietf.org/html/rfc3986#appendix-A

    try:
        raw_uri, query = raw_uri.split('?', 1)
    except ValueError:
        query = None
    else:
        constraints.constraint(
            is_query(query),
            'Query string is not valid')

    return (
        clean_relative_part(raw_uri),
        query)


def clean_uri(raw_uri):
    try:
        return clean_absolute_uri(raw_uri)
    except exceptions.HeaderError:
        return (
            None,  # Scheme
            *clean_relative_uri(raw_uri))
