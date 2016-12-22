# -*- coding: utf-8 -*-

from ..shared import parsers
from ..shared import bases
from ..shared import cookies
from ..shared import constraints
from ..shared import helpers


def cookie(name, value):
    assert name
    assert value
    assert isinstance(name, str)
    assert isinstance(value, str)

    return name, value


class Cookie(bases.HeaderBase):
    """
    Sent by client only.

    The user agent sends stored cookies\
    to the origin server in the Cookie header.

    Example::

        Cookie([
            cookie(
                name='SID',
                value='31d4d96e407aad42'),
            cookie(
                name='lang',
                value='en-US')
        ])

        Cookie([
            ('SID', '31d4d96e407aad42'),
            ('lang', 'en-US')
        ])

        Cookie([
            ('SID', 'foo'),
            ('SID', 'bar'),
            ('SID', 'baz')
        ])

    `Ref. <http://httpwg.org/specs/rfc6265.html#sane-cookie>`_
    """

    name = 'cookie'

    def values_str(self, values):
        return '; '.join(
            '{}={}'.format(name, value)
            for name, value in self.values())

    def prepare_raw_values(self, raw_values_collection):
        raw_values_collection = helpers.prepare_single_raw_values(
            raw_values_collection)
        return parsers.from_tokens(
            raw_values_collection[0],
            separator=';')

    def clean(self, raw_values):
        # There may be multiple cookies
        # with same name, it may be worth
        # generating a map with composed keys
        # like {(name, domain, path): value},
        # but I'm not sure
        #
        # Cookie-pairs allow quoted pairs but
        # no spaces or escaping within them,
        # so it's safe to parse as tokens
        values = tuple(
            cookies.clean_cookie_pair(rcp)
            for rcp in raw_values)

        constraints.must_not_be_empty(values)

        return values
