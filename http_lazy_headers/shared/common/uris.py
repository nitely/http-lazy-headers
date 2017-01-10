# -*- coding: utf-8 -*-

from ..utils import ascii_tools
from ..utils import constraints
from ... import exceptions

from . import hosts


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
_SLASH_PATH_CHARS = (
    _ALPHANUM |
    frozenset('-._~') |
    frozenset('!$&\'()*+,;=') |
    frozenset('%:@/'))

# unreserved / sub-delims / "%" _HEXDIG / "@"
_NC_PATH_CHARS = (
    _SLASH_PATH_CHARS -
    frozenset(':/'))

_QUERY_CHARS = (
    _SLASH_PATH_CHARS |
    frozenset('?'))


def _hier_part(user_info=None, host=None, path=None):
    assert any(
        v is not None
        for v in (user_info, host, path))

    return user_info, host, path


def is_scheme(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    if txt[0] not in _ALPHA:
        return False

    return set(txt).issubset(_SCHEME)


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

    return set(raw_path).issubset(_SLASH_PATH_CHARS)


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
    if raw_path.startswith('//'):
        return False

    return (
        raw_path.startswith('/') and
        is_path(raw_path))


def is_rootless(raw_path):
    assert isinstance(raw_path, str)

    if not raw_path:
        return False

    return (
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
            set(raw_path).issubset(_SLASH_PATH_CHARS))


def is_query(txt):
    assert isinstance(txt, str)

    return set(txt).issubset(_QUERY_CHARS)


def clean_authority_path(raw_path):
    constraints.constraint(
        raw_path.startswith('//'))

    raw_path = raw_path[2:]

    try:
        userinfo, raw_path = raw_path.split('@', 1)
    except ValueError:
        userinfo = None
    else:
        constraints.constraint(is_user_info(userinfo))

    try:
        raw_host, path = raw_path.split('/', 1)
    except ValueError:
        raw_host = raw_path
        path = None
    else:
        constraints.constraint(is_abempty(path))

    return _hier_part(
        user_info=userinfo,
        host=hosts.clean_host(raw_host),
        path=path)


def clean_hierarchical_part(raw_path):
    if raw_path.startswith('//'):
        return clean_authority_path(raw_path)

    if raw_path.startswith('/'):
        constraints.constraint(is_absolute(raw_path))
        return _hier_part(path=raw_path)

    if raw_path:
        constraints.constraint(is_rootless(raw_path))
        return _hier_part(path=raw_path)

    return _hier_part(path='')


def clean_absolute_uri(raw_uri):
    try:
        scheme, raw_path = raw_uri.split(':', 1)
    except ValueError:
        raise

    constraints.constraint(is_scheme(scheme))

    try:
        raw_path, query = raw_path.split('?', 1)
    except ValueError:
        query = None
    else:
        constraints.constraint(is_query(query))

    return (
        scheme,
        clean_hierarchical_part(raw_path),
        query)


def clean_relative_part(raw_path):
    if raw_path.startswith('//'):
        return clean_authority_path(raw_path)

    if raw_path.startswith('/'):
        constraints.constraint(is_absolute(raw_path))
        return _hier_part(path=raw_path)

    if raw_path:
        constraints.constraint(is_noscheme(raw_path))
        return _hier_part(path=raw_path)

    return _hier_part(path='')


def clean_relative_uri(raw_uri):
    try:
        raw_uri, query = raw_uri.split('?', 1)
    except ValueError:
        query = None
    else:
        constraints.constraint(is_query(query))

    return (
        clean_relative_part(raw_uri),
        query)


def clean_uri(raw_uri):
    try:
        return clean_absolute_uri(raw_uri)
    except exceptions.HeaderError:
        return clean_relative_uri(raw_uri)
