# -*- coding: utf-8 -*-

import base64

from ..shared.generic import formatters
from ..shared.generic import cleaners
from ..shared.utils import checkers
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared import bases
from ..shared import parameters
from ..shared.utils import assertions


def authorization_basic(username, password):
    assert isinstance(username, str)
    assert isinstance(password, str)

    return (
        'Basic',
        base64.b64encode(bytes(
            '{username}:{password}'.format(
                username=username,
                password=password),
            encoding='latin1')),
        parameters.Params())


class Authorization(bases.SingleHeaderBase):
    """
    Sent by client only.

    Multiple headers are not supported\
    per the spec (no values list allowed).

    If it includes an encoded-string,\
    be aware the encoding is not verified\
    nor tested.

    Example::

        import base64

        Authorization([
            authorization_basic(
                username='nitely',
                password='foobar')
        ])

        Authorization([
            (
                'Basic',
                base64.b64encode(bytes(
                    '{username}:{password}'.format(
                        username='nitely',
                        password='foobar')
                    encoding='latin1')),
                Params()
            )
        ])

        Authorization([
            (
                'Custom',
                None,
                Params({'secret': 'shhhh'})
            )
        ])

    `Ref. <http://httpwg.org/specs/rfc7235.html#header.authorization>`_
    """

    name = 'authorization'

    def check_one(self, value):
        assertions.must_be_tuple_of(value, 3)

        schema, token, params = value

        assertions.must_be_token(schema)
        not token or assertions.must_be_token68(token)
        assertions.must_be_params(params)
        assertions.assertion(
            not (token and params),
            '"{}" and "{}" received, either '
            'token or params was expected'
                .format(token, params))

    def to_str(self, values):
        return next(formatters.format_auth_values(values))

    def clean_one(self, raw_value):
        try:
            auth_schema, params_or_token = raw_value.split(' ', 1)
        except ValueError:
            auth_schema = raw_value
            params_or_token = None

        constraints.must_be_token(auth_schema)

        auth_schema = auth_schema.lower()

        if params_or_token is None:
            return (
                auth_schema,
                None,
                parameters.ParamsCI())

        if checkers.is_token68(params_or_token):
            return (
                auth_schema,
                params_or_token,
                parameters.ParamsCI())

        return (
            auth_schema,
            None,
            cleaners.clean_params(
                parsers.from_raw_params(
                    params_or_token,
                    separator=',')))
