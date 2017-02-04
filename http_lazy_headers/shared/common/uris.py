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
_HEXDIG = _ALPHANUM  # todo: fixme, this should be a-f not a-z

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


def uri(
        schema=None,
        user_info=None,
        host=None,
        path=None,
        query=None,
        fragment=None):
    # todo: remove path, add segments

    if path is not None:
        path = tuple(path)

    return (
        schema,
        user_info,
        host or hosts.host(),
        path or (),
        query,
        fragment)


def resolve_relative_reference(uri_base, uri_rel):
    # https://tools.ietf.org/html/rfc3986#section-5.4
    (schema,
     user_info,
     host,
     path,
     query,
     fragment) = uri_base

    (schema_rel,
     user_info_rel,
     host_rel,
     path_rel,
     query_rel,
     fragment_rel) = uri_rel

    if (user_info_rel is not None or
            any(h is not None
                for h in host_rel)):
        return (
            schema,
            user_info_rel,
            host_rel,
            remove_dot_segments_parts(path_rel),
            query_rel,
            fragment_rel)

    user_info_ = user_info
    host_ = host
    path_ = path
    query_ = query
    fragment_ = fragment

    if path and not path[-1] and path_rel and path_rel[0]:
        path_ = remove_dot_segments_parts((
            *path, *path_rel))

    if path and path[-1] and path_rel and path_rel[0]:
        path_ = remove_dot_segments_parts((
            *path[:-1], *path_rel))

    if path_rel and not path_rel[0]:
        path_ = remove_dot_segments_parts(path_rel)

    if query_rel is not None or path != path_:
        query_ = query_rel

    if fragment_rel is not None or path != path_:
        fragment_ = fragment_rel

    return (
        schema,
        user_info_,
        host_,
        path_,
        query_,
        fragment_)


def remove_dot_segments_parts(segments):
    # Ref: https://tools.ietf.org/html/rfc3986#section-5.2.4
    # Ref impl: https://gist.github.com/nitely/08ee70e3429d4f174a00aa06e5ebf68c

    assert isinstance(segments, (tuple, list))

    in_buff = collections.deque(segments)
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


def remove_dot_segments(path):
    assert isinstance(path, str)

    return '/'.join(
        remove_dot_segments_parts(
            path.split('/')))


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


_HEXDIG = '0123456789ABCDEFabcdef'

_HEXDIG_MAP = {
    (a, b): bytes((int(a + b, 16),))
    for a in _HEXDIG
    for b in _HEXDIG}


def decode_percent_encoded(txt):
    assert isinstance(txt, str)

    if '%' not in txt:
        return txt

    percent = False
    checked = 0
    hex_first = ''
    res = []

    # "% HEXDIG HEXDIG"
    for c in bytes(txt, 'utf-8', 'strict'):
        if percent:
            checked += 1

        if checked == 1:
            hex_first = c
            continue

        if checked == 2:
            percent = False
            checked = 0

            try:
                c_decoded = _HEXDIG_MAP[(hex_first, c)]
            except IndexError:
                raise exceptions.HTTPLazyHeadersError(
                    'Bad percent encoded pair %{}{}'
                    .format(hex_first, c))

            res.append(c_decoded)
            continue

        if c == b'%':
            percent = True
            continue

        res.append(c)

    if percent:
        raise exceptions.HTTPLazyHeadersError(
            'Missing percent encoded pair')

    try:
        return str(b''.join(res), 'utf-8', 'strict')
    except UnicodeDecodeError:
        raise exceptions.HTTPLazyHeadersError(
            'Can\'t decode non-utf-8 sequence from text')


def is_hex_encoded(txt):
    # todo: remove
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

    if percent:
        return False

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


def clean_path(raw_path):
    try:
        return decode_percent_encoded(raw_path)
    except exceptions.HTTPLazyHeadersError:
        raise exceptions.BadRequest(
            'Can\'t decode percent encoded uri-path')


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
        path = ''
    else:
        path = ''.join(('/', path))  # Put "/" back
        constraints.constraint(
            is_abempty(path),
            'Authority URI "path-abempty" is not valid')

    return _hier_part(
        user_info=userinfo,
        host=hosts.clean_host(raw_host),
        path=clean_path(path))


def clean_hierarchical_part(raw_path):
    if raw_path.startswith('//'):
        return clean_authority_path(raw_path)

    if raw_path.startswith('/'):
        constraints.constraint(
            is_absolute(raw_path),
            'Absolute path is not valid')
        return _hier_part(path=clean_path(raw_path))

    if raw_path:
        constraints.constraint(
            is_rootless(raw_path),
            'Rootless path is not valid')
        return _hier_part(path=clean_path(raw_path))

    return _hier_part(path=clean_path(''))


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
    return uri(
        scheme.lower(),
        *clean_hierarchical_part(raw_path),
        query)


def clean_relative_part(raw_path):
    # https://tools.ietf.org/html/rfc3986#section-4.2

    if raw_path.startswith('//'):
        return clean_authority_path(raw_path)

    if raw_path.startswith('/'):
        constraints.constraint(
            is_absolute(raw_path),
            'Rel URI "path-absolute" is not valid')
        return _hier_part(path=clean_path(raw_path))

    if raw_path:
        constraints.constraint(
            is_noscheme(raw_path),
            'Rel URI "path-noscheme" is not valid')
        return _hier_part(path=clean_path(raw_path))

    return _hier_part(path=clean_path(''))


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

    return uri(
        None,  # Scheme
        *clean_relative_part(raw_uri),
        query)


def clean_uri(raw_uri):
    try:
        return clean_absolute_uri(raw_uri)
    except exceptions.HeaderError:
        return clean_relative_uri(raw_uri)


def _format_uri(value):
    (schema,
     user_info,
     host,
     path,
     query,
     fragment) = value

    if schema:
        yield '{}:'.format(schema)

    has_host = any(
        h
        for h in host
        if h is not None)

    # Authority
    if user_info is not None or has_host:
        yield '//'

    if user_info is not None:
        yield '{}@'.format(user_info)

    if has_host:
        yield hosts.format_host(host)

    yield path

    if query is not None:
        yield '?{}'.format(query)

    if fragment is not None:
        yield '#{}'.format(fragment)


def format_uri(value):
    return ''.join(_format_uri(value))
