# -*- coding: utf-8 -*-

import encodings.idna
import urllib.parse

from . import cookies
from ..generic import cleaners
from ..utils import ascii_tools
from ..utils import constraints
from ..utils import assertions
from ... import exceptions
from ...settings import settings


# 0-9 / a-f / A-F
_HEXDIG = frozenset(
    ascii_tools.ascii_chars(
        (0x30, 0x39),
        (0x41, 0x46),
        (0x61, 0x66)))

# unreserved / sub-delims / ":"
_IPV_FUTURE_TAIL = (
    frozenset(
        ascii_tools.ascii_chars(
            (0x30, 0x39),
            (0x41, 0x5A),
            (0x61, 0x7A))) |
    frozenset('-._~') |
    frozenset('!$&\'()*+,;=') |
    frozenset(':'))

# unreserved / sub-delims / "%" _HEXDIG
_REG_NAME = (
    frozenset(
        ascii_tools.ascii_chars(
            (0x30, 0x39),
            (0x41, 0x5A),
            (0x61, 0x7A))) |
    frozenset('-._~') |
    frozenset('!$&\'()*+,;=') |
    frozenset('%'))

_DIGITS = frozenset(
    ascii_tools.ascii_chars(
        (0x30, 0x39)))


def is_ipv4(raw_ipv4):
    # Quick check to avoid
    # extra computation
    if raw_ipv4[-1] not in _DIGITS:
        return False

    ipv4 = raw_ipv4.split('.', 3)

    if len(ipv4) != 4:
        return False

    for part in ipv4:
        if part != '0' and part.startswith('0'):
            return False

        try:
            part = cleaners.clean_number(part, max_chars=3)
        except exceptions.HeaderError:
            return False

        if part > 255:
            return False

    return True


def _is_h16(raw_h16):
    if not 1 <= len(raw_h16) <= 4:
        return False

    return set(raw_h16).issubset(_HEXDIG)


def is_ipv6(raw_ipv6):
    # http://download.dartware.com/thirdparty/test-ipv6-regex.pl

    # https://tools.ietf.org/html/rfc3986#appendix-A
    #
    # Validation algorithm:
    # has no head and has a tail of 8 or 7
    # has head of 0 and has a tail of 7 or 6
    # has head of <= 1 and has a tail of 6 or 5
    # has head of <= 2 and has a tail of 5 or 4
    # has head of <= 3 and has a tail of 4 or 3
    # has head of <= 4 and has a tail of 3 or 2
    # has head of <= 5 and has a tail of 2 or 1
    # has head of <= 6 and has a tail of 1
    # has head of <= 7 and has a tail of 0
    #
    # If ls32 is IPv4address there is one
    # part less than if it is h16:h16,
    # so must add 1 to the len to
    # make up for the missing part.
    #
    # The "no head" is a special case.
    #
    # 7 <= len(tail) <= 8 ; if no head
    # 0 <= len(head) <= 7 - len(tail) - 1 ; if IPv4address
    # 0 <= len(head) <= 7 - len(tail) ; else

    try:
        head, tail = raw_ipv6.split('::', 1)
    except ValueError:
        head = None
        tail = raw_ipv6

    if head == '':
        head = ()
    else:
        head = head.split(':', 6)

    if not all(
            _is_h16(h)
            for h in head):
        return False

    if tail == '':
        tail = ()
    else:
        tail = tail.split(':', 6)

    if tail:
        has_ipv4 = is_ipv4(tail[-1])
    else:
        has_ipv4 = False

    if has_ipv4 and not all(
            _is_h16(t)
            for t in tail[:-1]):
        return False

    if not has_ipv4 and not all(
            _is_h16(t)
            for t in tail):
        return False

    if head is None:
        return 7 <= len(tail) <= 8

    if has_ipv4:
        head_max_len = 7 - len(tail) - 1
    else:
        head_max_len = 7 - len(tail)

    return 0 <= len(head) <= head_max_len


def is_ipv_future(raw_ipv_future):
    # https://tools.ietf.org/html/rfc3986#appendix-A

    if not raw_ipv_future.startswith('v'):
        return False

    raw_ipv_future = raw_ipv_future[1:]

    try:
        head, tail = raw_ipv_future.split('.', 1)
    except ValueError:
        return False

    if not head or not tail:
        return False

    if not set(head).issubset(_HEXDIG):
        return False

    if not set(tail).issubset(_IPV_FUTURE_TAIL):
        return False

    return True


def is_unsafe_host(raw_host):
    if not set(raw_host).issubset(_REG_NAME):
        return False

    percent = False
    checked = 0

    # Check "% HEXDIG HEXDIG"
    for c in raw_host:
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


def host(
        domain=None,
        ipv4=None,
        ipv6=None,
        ipv_future=None,
        unsafe=None,
        port=None):
    assert len(tuple(
        x
        for x in (
            domain,
            ipv4,
            ipv6,
            ipv_future,
            unsafe)
        if x is not None)) < 2
    assert (ipv_future is None or
            (isinstance(ipv_future, str) and
             ipv_future.startswith('v')))
    assert (
        port is None or
        isinstance(port, int))

    return domain, ipv4, ipv6, ipv_future, unsafe, port


def check_host(value):
    assertions.must_be_tuple_of(value, 6)
    assertions.assertion(
        len(tuple(
            v
            for v in value[:5]
            if v is not None)) < 2,
        '"{}" received, only one '
        'non-empty value was expected'
        .format(value[:5]))

    for v, check_func in zip(
            value[1:5],
            (is_ipv4,
             is_ipv6,
             is_ipv_future,
             is_unsafe_host)):
        assertions.assertion(
            v is None or
            (isinstance(v, str) and
             check_func(v)),
            '"{}" received, a valid host '
            'was expected'.format(v))

    domain = value[0]
    domain is None or assertions.assertion(
        isinstance(domain, str) and
        cookies.is_domain(str(
            encodings.idna.ToASCII(domain),
            encoding='ascii')),
        '"{}" received, a valid domain '
        'was expected'.format(domain))

    port = value[5]
    port is None or assertions.must_be_int(port)


def format_host(value):
    (domain,
     ipv4,
     ipv6,
     ipv_future,
     unsafe,
     port) = value

    if domain:
        domain = str(
            encodings.idna.ToASCII(domain),
            encoding='ascii')

    if ipv6:
        ipv6 = '[{}]'.format(ipv6)

    if ipv_future:
        ipv_future = '[{}]'.format(ipv_future)

    # Default to '' if no value
    host_name = next((
        h for h in (
            domain,
            ipv4,
            ipv6,
            ipv_future,
            unsafe)
        if h is not None),
        '')

    if port is not None:
        return '{}:{}'.format(host_name, port)

    return host_name


def _clean_unsafe_host(raw_host):
    """
    This tries to unquote the host.\
    If there is nothing to unquote,\
    then it tries to idna decode it.

    :param raw_host:
    :return:
    """
    constraints.constraint(
        is_unsafe_host(raw_host),
        'Host is not a valid reg-name')

    try:
        raw_host_unquoted = urllib.parse.unquote(
            raw_host,
            encoding='utf-8',
            errors='strict')
    except UnicodeDecodeError:
        raw_host_unquoted = raw_host

    if raw_host != raw_host_unquoted:
        return raw_host_unquoted

    try:
        return encodings.idna.ToUnicode(raw_host)
    except UnicodeError:
        # A broken idna encoded name
        # or something that looks
        # too much like it
        return raw_host


def clean_host(raw_value):
    # ABNF: https://tools.ietf.org/html/rfc3986#appendix-A
    # Host: https://tools.ietf.org/html/rfc3986#section-3.2.2

    # Port may be a empty str
    try:
        raw_host, port = raw_value.rsplit(':', 1)
    except ValueError:
        raw_host = raw_value
        port = None

    # Allow empty port
    port = port or None

    if port:
        try:
            port = cleaners.clean_number(port, max_chars=5)
        except exceptions.HeaderError:
            # Likely an IPv6/Future. Not a port
            raw_host = raw_value
            port = None

    # Host must be case-insensitive,
    # including ipv_future that may
    # start with "v" or "V"
    raw_host = raw_host.lower()

    # For some reason this is actually valid
    if not raw_host:
        return host(port=port)

    if (raw_host.startswith('[v') and
            raw_host.endswith(']')):
        ipv_some = raw_host[1:-1]

        constraints.constraint(
            is_ipv_future(ipv_some),
            'Value is not a valid IPvFuture')

        return host(
            ipv_future=ipv_some,
            port=port)

    if (raw_host.startswith('[') and
            raw_host.endswith(']')):
        ipv_some = raw_host[1:-1]

        constraints.constraint(
            is_ipv6(ipv_some),
            'Value is not a valid IPv6')

        return host(ipv6=ipv_some, port=port)

    # Must check for ipv4 before domain
    if is_ipv4(raw_host):
        return host(ipv4=raw_host, port=port)

    try:
        return host(
            domain=cookies.clean_domain(raw_host),
            port=port)
    except exceptions.HeaderError:
        pass

    if settings.HOST_UNSAFE_ALLOW:
        return host(
            unsafe=_clean_unsafe_host(raw_host),
            port=port)

    raise exceptions.BadRequest('Bad host name')
