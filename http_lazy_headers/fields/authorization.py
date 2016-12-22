# -*- coding: utf-8 -*-

import base64

from ..shared import bases
from ..shared import cleaners
from ..shared import helpers
from ..shared import constraints
from ..shared import checkers
from ..shared import parameters
from ..shared import parsers


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

    def values_str(self, values):
        return next(helpers.format_auth_values(values))

    def clean_value(self, raw_value):
        try:
            auth_schema, params_or_token = raw_value.split(' ', 1)
        except ValueError:
            auth_schema = raw_value
            params_or_token = None

        constraints.must_be_token(auth_schema)

        if params_or_token is None:
            return (
                auth_schema.lower(),
                None,
                parameters.ParamsCI())
        elif checkers.is_token68(params_or_token):
            return (
                auth_schema.lower(),
                params_or_token,
                parameters.ParamsCI())
        else:
            return (
                auth_schema.lower(),
                None,
                cleaners.clean_params(
                    parsers.from_raw_params(
                        params_or_token,
                        separator=',')))
