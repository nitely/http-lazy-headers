# -*- coding: utf-8 -*-

import encodings.idna

from ..shared import ascii_tools
from .. import exceptions
from ..shared import constraints


# %x21 / %x23-2B / %x2D-3A / %x3C-5B / %x5D-7E
_COOKIE_OCTET_CHARS = frozenset(
    ascii_tools.ascii_chars(
        0x21,
        (0x23, 0x2B),
        (0x2D, 0x3A),
        (0x3C, 0x5B),
        (0x5D, 0x7E)))

# https://tools.ietf.org/html/rfc2616#section-2.2
# Any CHAR except CTLs or separators
# Separators:
# "(" | ")" | "<" | ">" | "@" |
# "," | ";" | ":" | "\" | <"> |
# "/" | "[" | "]" | "?" | "=" |
# "{" | "}" | SP | HT
_COOKIE_TOKEN_CHARS = (
    frozenset(ascii_tools.ascii_chars((0x21, 0x7E))) -
    frozenset('()<>@,;:\\"/[]?={}'))

_DIGITS = frozenset(
    ascii_tools.ascii_chars(
        (0x30, 0x39)))

# a-z / A-Z / 0-9 / - / .
_DOMAIN_CHARS = frozenset(
    ascii_tools.ascii_chars(
        (0x30, 0x39),
        (0x41, 0x5A),
        (0x61, 0x7A),
        0x2D,
        0x2E))


def is_cookie_octets(txt):
    if not txt:
        return False

    return set(txt).issubset(_COOKIE_OCTET_CHARS)


def is_quoted_cookie_octets(txt):
    # Empty, single quoted or
    # double quoted with no octets in it
    if len(txt) <= 2:
        return False

    if (not txt.startswith('"') and
            not txt.endswith('"')):
        return False

    return is_cookie_octets(txt[1:-1])


def must_be_cookie_token(txt):
    if not txt:
        return False

    return set(txt).issubset(_COOKIE_TOKEN_CHARS)


def clean_cookie_pair(raw_cookie_pair):
    # http://httpwg.org/specs/rfc6265.html#sane-set-cookie-syntax

    try:
        name, value = raw_cookie_pair.split('=', 1)
    except ValueError:
        raise exceptions.BadRequest(
            'Cookie must contain "name=value" '
            'as first pair')

    name = name.strip()
    value = value.strip()

    must_be_cookie_token(name)
    constraints.constraint(
        not value or
        is_cookie_octets(value) or
        is_quoted_cookie_octets(value),
        'Cookie value must be '
        'a token, be quoted or be empty')

    if value.startswith('"'):
        value = value[1:-1]

    return name, value


def is_domain(txt):
    # https://tools.ietf.org/html/rfc1034#section-3.5
    # https://tools.ietf.org/html/rfc1123#section-2.1

    if not txt:
        return False

    if txt.startswith('.'):
        return False

    if len(txt) > 255:
        return False

    # Check is not an IP
    if txt[-1] in _DIGITS:
        return False

    if not set(txt).issubset(_DOMAIN_CHARS):
        return False

    parts = txt.split('.', 128)
    parts_len = len(parts)

    if (parts_len < 2 or
            parts_len > 128):
        return False

    # Each part len must be equal/less than
    # 255 but that's validated above
    for part in parts:
        if not part:
            return False

        if part.startswith('-'):
            return False

        if part.endswith('-'):
            return False

    return True


def clean_domain(raw_domain):
    # http://httpwg.org/specs/rfc6265.html#domain-attribute

    constraints.constraint(
        is_domain(raw_domain),
        'Value is not a valid domain')

    try:
        raw_domain = encodings.idna.ToUnicode(raw_domain)
    except UnicodeError:
        raise exceptions.BadRequest(
            'Invalid IDN label')

    return raw_domain.lower()
