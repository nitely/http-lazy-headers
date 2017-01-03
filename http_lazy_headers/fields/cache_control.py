# -*- coding: utf-8 -*-

from ..shared.generic import cleaners
from ..shared.generic import preparers
from ..shared.utils import checkers
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared import bases
from ..shared import parameters
from ..shared.utils import assertions


def cache_control(
        no_cache=None,
        private=None,
        max_age=None,
        max_stale=None,
        min_fresh=None,
        s_maxage=None):
    assert any(
        v is not None
        for v in locals().values())
    assert all(
        (v is None or
         isinstance(v, (bool, tuple, list, set)))
        for v in (no_cache, private))
    assert all(
        (v is None or
         isinstance(v, int))
        for v in (
            max_age,
            max_stale,
            min_fresh,
            s_maxage))

    params = []

    for param_name, param_value in (
            ('no-cache', no_cache),
            ('private', private),
            ('max-age', max_age),
            ('max-stale', max_stale),
            ('min-fresh', min_fresh),
            ('s-maxage', s_maxage)):
        if param_value is None:
            continue

        if isinstance(param_value, bool):
            if param_value:
                param_value = ()
            else:
                continue

        if isinstance(param_value, (list, set)):
            param_value = tuple(param_value)

        params.append(
            (param_name, param_value))

    return parameters.Params(params)


class CacheControl(bases.HeaderBase):
    """
    Be aware ``no-cache`` and ``private`` may be params\
    instead of values depending on whether they have\
    an argument or not. However, the former is very rare.

    The ``Cache-Control`` header field is used to specify\
    directives for caches along the request/response chain.\
    Such cache directives are unidirectional in that the\
    presence of a directive in a request does not imply\
    that the same directive is to be given in the response.

    Example::

        CacheControl([
            cache_control(
                no_cache=True,
                private=True,
                max_age=60)
        ])

        CacheControl([
            cache_control(
                no_cache=('accept',),
                private=('allow',),
                max_age=60)
        ])

        CacheControl([
            Params([
                ('no-cache', ()),
                ('private', ()),
                ('max-age', 60)
            ])
        ])

    `Ref. <http://httpwg.org/specs/rfc7234.html#header.cache-control>`_
    """

    # if no-cache/private is param it must always
    # be quoted (even if not needed),
    # param values are case-insensitive

    name = 'cache-control'
    directives_with_delta_secs = frozenset((
        'max-age',
        'max-stale',
        'min-fresh',
        's-maxage'))
    directives_with_header_values = frozenset((
        'no-cache',
        'private'))

    def check_value(self, value):
        assertions.must_be_tuple_of(value, 2)
        param_name, param_value = value
        assertions.must_be_token(param_name)
        param_name = param_name.lower()

        if param_name in self.directives_with_header_values:
            assertions.must_be_instance_of(param_value, tuple)

            for t in param_value:
                assertions.must_be_token(t)

            return

        if param_name in self.directives_with_delta_secs:
            assertions.must_be_instance_of(param_value, int)
            return

        if isinstance(param_value, tuple):
            for v in param_value:
                assertions.must_be_ascii(v)

            return

        assertions.must_be_ascii(param_value)

    def check_values(self, values):
        assertions.must_have_one_value(values)
        value = values[0]
        assertions.must_be_params(value)

        for item in value.items():
            self.check_value(item)

    def value_str(self, value):
        param_name, param_value = value

        if param_name in self.directives_with_delta_secs:
            return '{}={}'.format(
                param_name,
                str(param_value))

        if (param_name in self.directives_with_header_values and
                param_value):
            return '{}="{}"'.format(
                param_name,
                ', '.join(param_value))

        if param_value:
            return '{}={}'.format(
                param_name,
                parsers.quote_maybe(param_value))

        return param_name

    def values_str(self, values):
        params = values[0]

        return ', '.join(
            self.value_str(p)
            for p in params.items())

    def prepare_raw_values(self, raw_values_collection):
        return preparers.prepare_multi_raw_values(raw_values_collection)

    def clean_value(self, raw_value):
        # Directives with delta secs
        # must have values
        if (raw_value not in self.directives_with_delta_secs and
                checkers.is_token(raw_value)):
            return raw_value, ()

        directive, argument = cleaners.clean_param(raw_value)

        if directive.lower() in self.directives_with_delta_secs:
            return directive, cleaners.clean_delta_seconds(argument)

        # Custom directives, no-cache and
        # private have optional arguments
        # and may be formatted as directive=""
        if not argument:
            return directive, ()

        if directive.lower() in self.directives_with_header_values:
            return directive, cleaners.clean_tokens_ci(argument)

        return directive, argument

    def clean(self, raw_values):
        constraints.must_not_be_empty(raw_values)
        return (
            parameters.ParamsCI(
                self.clean_value(v)
                for v in raw_values),)
