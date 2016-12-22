# -*- coding: utf-8 -*-

import collections
import encodings.idna

from ..shared import ascii_tools
from .. import exceptions
from ..shared import bases
from ..shared import cleaners
from ..shared import constraints
from ..shared import cookies
from ..shared import dates
from ..shared import parsers


# 0x20-0x7E (except ";")
_COOKIE_CHARS = (
    frozenset(ascii_tools.ascii_chars((0x20, 0x7E))) -
    frozenset(';'))


CookiePair = collections.namedtuple(
    'CookiePair',
    [
        'name',
        'value',
        'expires',
        'max_age',
        'domain',
        'path',
        'extension',
        'secure',
        'http_only'])
CookiePair.__doc__ = (
    """
    """)


def cookie_pair(
        name,
        value,
        expires=None,
        max_age=None,
        domain=None,
        path=None,
        extension=None,
        secure=False,
        http_only=False):
    return CookiePair(
        name,
        value,
        expires=expires,
        max_age=max_age,
        domain=domain,
        path=path,
        extension=extension,
        secure=secure,
        http_only=http_only)


def clean_expires(raw_expires):
    # http://httpwg.org/specs/rfc6265.html#expires-attribute

    return dates.clean_date_time(raw_expires)


def clean_max_age(raw_age):
    # http://httpwg.org/specs/rfc6265.html#max-age-attribute

    if raw_age.startswith('0'):
        raise exceptions.BadRequest(
            'Value must start with '
            'a number between 1-9')

    return cleaners.clean_delta_seconds(raw_age)


def is_path(raw_path):
    if not raw_path:
        return False

    if not raw_path.startswith('/'):
        return False

    return set(raw_path).issubset(_COOKIE_CHARS)


def is_extension(raw_extension):
    if not raw_extension:
        return False

    return set(raw_extension).issubset(_COOKIE_CHARS)


def clean_path(raw_path):
    # http://httpwg.org/specs/rfc6265.html#path-attribute

    constraints.constraint(
        is_path(raw_path),
        'Value is not a valid path')

    return raw_path


def clean_extension(raw_extension):
    constraints.constraint(
        is_extension(raw_extension),
        'Value is not a valid extension')

    return raw_extension


_CLEANERS = {
    'expires': clean_expires,
    'domain': cookies.clean_domain,
    'max-age': clean_max_age,
    'path': clean_path}

_TO_PY_ATTR = {
    'Secure': 'secure',
    'HttpOnly': 'http_only'}

_FROM_PY_ATTR = {
    v: k
    for k, v in _TO_PY_ATTR.items()}


def clean_attr(raw_attribute):
    if raw_attribute in {'Secure', 'HttpOnly'}:
        return _TO_PY_ATTR[raw_attribute], True

    try:
        attribute, value = raw_attribute.split('=', 1)
    except ValueError:
        return 'extension', clean_extension(raw_attribute)

    attribute = attribute.strip().lower()

    try:
        cleaner = _CLEANERS[attribute]
    except KeyError:
        return 'extension', clean_extension(raw_attribute)

    return attribute, cleaner(value.lower())


def clean_attrs(raw_attrs):
    extensions = []

    for raw_attr in raw_attrs:
        attr, value = clean_attr(raw_attr)

        if attr == 'extension':
            extensions.append(value)
            continue

        yield attr, value

    if extensions:
        yield 'extension', tuple(extensions)


def clean(raw_values):
    raw_values = parsers.from_tokens(raw_values, ';')

    return cookie_pair(
        *cookies.clean_cookie_pair(next(raw_values)),
        **dict(clean_attrs(raw_values)))


class SetCookie(bases.HeaderBase):
    """
    Sent by server only.

    The ``Set-Cookie`` HTTP response header\
    is used to send cookies from the server\
    to the user agent.

    Informally, the ``Set-Cookie`` response\
    header contains the header name ``Set-Cookie``\
    followed by a ":" and a cookie. Each cookie\
    begins with a name-value-pair, followed by\
    zero or more attribute-value pairs.

    Example::

        SetCookie([
            cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/',
                domain='example.com',
                secure=True,
                http_only=True)
        ])

    `Ref. <http://httpwg.org/specs/rfc6265.html#sane-set-cookie>`_
    """

    name = 'set-cookie'

    def __str__(self):
        # Support multi headers
        return '\r\n'.join(
            '{}: {}'.format(
                self.name,
                self.cookie_str(cookie))
            for cookie in self.values())

    def _cookie_str(self, cookie):
        yield '{}={}'.format(cookie.name, cookie.value)

        if cookie.expires is not None:
            yield 'expires={}'.format(
                dates.format_date(cookie.expires))

        if cookie.max_age is not None:
            yield 'max-age={}'.format(cookie.max_age)

        if cookie.path:
            yield 'path={}'.format(cookie.path)

        if cookie.domain:
            yield 'domain={}'.format(str(
                encodings.idna.ToASCII(cookie.domain),
                encoding='ascii'))

        for attr in ('secure', 'http_only'):
            value = getattr(cookie, attr)

            if value:
                yield _FROM_PY_ATTR[attr]

        if cookie.extension is not None:
            for ext in cookie.extension:
                yield ext

    def cookie_str(self, cookie):
        return '; '.join(
            self._cookie_str(cookie))

    def prepare_raw_values(self, raw_values_collection):
        return raw_values_collection

    def clean(self, raw_values):
        return tuple(
            clean(rvs)
            for rvs in raw_values)
