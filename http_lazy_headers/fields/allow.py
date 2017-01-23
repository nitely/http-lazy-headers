# -*- coding: utf-8 -*-

from ..shared.utils import constraints
from ..shared import bases


class Allow(bases.TokensHeaderBase):
    """
    Sent by server only.

    May be empty.

    The "Allow" header field lists the\
    set of methods advertised as supported\
    by the target resource. The purpose of\
    this field is strictly to inform the\
    recipient of valid request methods\
    associated with the resource.

    Example::

        Allow([
            Methods.get,
            Methods.post
        ])

        Allow([
            'GET',
            'POST'
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.allow>`_
    """

    name = 'allow'
    # methods = constants.METHODS  # todo: warning if not one of these, case-sensitive

    def check_values(self, values):
        # Allow empty field
        for v in values:
            self.check_value(v)

    def clean_value(self, raw_value):
        constraints.must_be_token(raw_value)
        return raw_value

    def clean(self, raw_values):
        # Allow empty field
        return tuple(
            self.clean_value(rv)
            for rv in raw_values)
