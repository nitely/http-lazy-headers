# -*- coding: utf-8 -*-

import collections
import encodings.idna

from ..shared.common import cookies
from ..shared.common import dates
from ..shared.generic import cleaners
from ..shared.utils import ascii_tools
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared.utils import assertions
from .. import exceptions
from ..shared import bases


# 0x20-0x7E (except ";")
_COOKIE_CHARS = (
    frozenset(ascii_tools.ascii_chars((0x20, 0x7E))) -
    frozenset(';'))


class CookiePair:

    def __init__(
            self,
            name,
            value,
            expires=None,
            max_age=None,
            domain=None,
            path=None,
            extension=None,
            secure=False,
            http_only=False):
        assert (
            extension is None or
            isinstance(
                extension, (tuple, list)))

        if extension is not None:
            extension = tuple(extension)

        self.name = name
        self.value = value
        self.expires = expires
        self.max_age = max_age
        self.domain = domain
        self.path = path
        self.extension = extension
        self.secure = secure
        self.http_only = http_only


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

    return CookiePair(
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

    def check_values(self, values):
        for c in values:
            assertions.must_be_instance_of(c, CookiePair)

        cookies.check_cookie(tuple(
            (c.name, c.value)
            for c in values))

        for c in values:
            c.expires is None or dates.check_date(c.expires)
            c.max_age is None or assertions.must_be_int(c.max_age)
            c.domain is None or assertions.assertion(
                isinstance(c.domain, str) and
                cookies.is_domain(c.domain),
                '"{}" received, a valid '
                'domain was expected'.format(c.domain))
            c.path is None or assertions.assertion(
                isinstance(c.path, str) and
                is_path(c.path),
                '"{}" received, a valid '
                'path was expected'.format(c.path))
            c.extension is None or assertions.assertion(
                isinstance(c.path, tuple) and
                all(is_extension(e)
                    for e in c.extension),
                '"{}" received, a valid '
                'extension was expected'.format(c.extension))
            assertions.must_be_instance_of(c.secure, bool)
            assertions.must_be_instance_of(c.http_only, bool)

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
