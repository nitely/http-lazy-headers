# -*- coding: utf-8 -*-

import encodings.idna

from ..settings import settings
from .. import exceptions
from ..shared import bases
from ..shared import constraints
from ..shared import cleaners
from ..shared import cookies
from ..shared import ascii_tools


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


def _host(
        domain=None,
        ipv4=None,
        ipv6=None,
        ipv_future=None,
        unsafe=None,
        port=None):
    assert any(
        v is not None
        for v in locals())
    return domain, ipv4, ipv6, ipv_future, unsafe, port


def is_ipv4(raw_ipv4):
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

        if part < 255:
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
    assert any(
        v is not None
        for v in (
            domain,
            ipv4,
            ipv_future,
            unsafe))
    assert (
        port is None or
        isinstance(port, int))

    return domain, ipv4, ipv6, ipv_future, unsafe, port


class Host(bases.SingleHeaderBase):
    """
    Sent by client only

    This field may be empty.

    This will validate the ``format`` for port,\
    domain, ipv4, ipv6, ipvFuture and unsafe host.\
    However, that does not mean that the value\
    is actually valid.

    Make sure to check the value against a\
    white-list of valid domains. Search for\
    "host poisoning" for examples of what\
    may happen failing to do that.

    The ``Host`` header field in a request\
    provides the host and port information\
    from the target URI, enabling the origin\
    server to distinguish among resources\
    while servicing requests for multiple\
    host names on a single IP address.

    Example::

        # Empty host
        Host([
            host()
        ])

        Host([
            host('example.org')
        ])

        Host([
            host('example.org', port=8000)
        ])

        Host([
            host('www.Alliancefrançaise.nu')
        ])

        Host([
            host(ipv4='123.123.123.123')
        ])

        Host([
            host(ipv6='2001:db8:a0b:12f0::1')
        ])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.host>`_
    """

    name = 'host'

    def values_str(self, values):
        (domain,
         ipv4,
         ipv6,
         ipv_future,
         unsafe,
         port) = values[0]

        if not values[0]:
            return ''

        if domain:
            domain = str(
                encodings.idna.ToASCII(domain),
                encoding='ascii')

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

    def clean_value(self, raw_value):
        # https://tools.ietf.org/html/rfc3986#appendix-A

        try:
            raw_host, port = raw_value.rsplit(':', 1)
        except ValueError:
            raw_host = raw_value
            port = None

        port = port or None  # It can be empty

        if port:
            try:
                port = cleaners.clean_number(port, max_chars=5)
            except exceptions.HeaderError:
                raw_host = raw_value

        # For some reason this is actually valid
        if not raw_host:
            return _host(port=port)

        if (raw_host.startswith('[v') and
                raw_host.endswith(']')):
            ipv_some = raw_host[1:-1]

            constraints.constraint(
                is_ipv_future(ipv_some),
                'Value is not a valid IPvFuture')

            return _host(
                ipv_future=ipv_some[1:],
                port=port)

        if (raw_host.startswith('[') and
                raw_host.endswith(']')):
            ipv_some = raw_host[1:-1]

            constraints.constraint(
                is_ipv6(ipv_some),
                'Value is not a valid IPv6')

            return _host(ipv6=ipv_some, port=port)

        if is_ipv4(raw_host):
            return _host(ipv4=raw_host, port=port)

        try:
            return _host(
                domain=cookies.clean_domain(raw_host),
                port=port)
        except exceptions.HeaderError:
            pass

        if (settings.HOST_UNSAFE_ALLOW and
                is_unsafe_host(raw_host)):
            return _host(unsafe=raw_host.lower())

        raise exceptions.BadRequest('Bad host name')

    def clean(self, raw_values):
        # Allow empty value
        constraints.constraint(
            len(raw_values) == 1,
            'Header must have one '
            'value and be unique',
            status=400)
        raw_value = raw_values[0].strip()

        if raw_value:
            return (
                self.clean_value(raw_value),)
        else:
            return ()
