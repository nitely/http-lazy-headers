# -*- coding: utf-8 -*-

from ..shared.generic import cleaners
from ..shared.generic import preparers
from ..shared.utils import checkers
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared.utils import assertions
from ..shared import bases
from ..shared import parameters


def pragma(no_cache=False, params=()):
    assert no_cache or params

    if no_cache:
        params = (('no-cache', ()), *params)

    return parameters.ParamsCI(params)


class Pragma(bases.HeaderBase):
    """
    Sent by client only.

    The ``Pragma`` header field allows\
    backwards compatibility with HTTP/1.0\
    caches, so that clients can specify a\
    "no-cache" request that they will understand\
    (as Cache-Control was not defined until\
    HTTP/1.1). When the Cache-Control header\
    field is also present and understood in a\
    request, Pragma is ignored.

    Example::

        Pragma([
            pragma(no_cache=True)
        ])

        Pragma([
            pragma(
                no_cache=True,
                params=[
                    ('foo', 'bar'),
                    ('baz', 'qux')
                ])
        ])

        Pragma([
            Params({'no-cache': ()})
        ])

    `Ref. <http://httpwg.org/specs/rfc7234.html#header.pragma>`_
    """

    name = 'pragma'

    def check_values(self, values):
        assertions.must_have_one_value(values)
        params = values[0]
        assertions.must_be_params(params)
        assertions.must_not_be_empty(params)

        for t, v in params.items():
            assertions.must_be_token(t)
            not v or assertions.must_be_ascii(v)

    def value_str(self, value):
        param_name, param_value = value

        if not param_value:
            return param_name

        return '{}={}'.format(
            param_name,
            parsers.quote_maybe(param_value))

    def values_str(self, values):
        params = values[0]

        return ', '.join(
            self.value_str(p)
            for p in params.items())

    def prepare_raw_values(self, raw_values_collection):
        return preparers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, raw_value):
        if checkers.is_token(raw_value):
            return raw_value, ()

        return cleaners.clean_param(raw_value)

    def clean(self, raw_values):
        params = parameters.ParamsCI(
            self.clean_value(v)
            for v in raw_values)

        constraints.must_not_be_empty(params)

        return (
            params,)
