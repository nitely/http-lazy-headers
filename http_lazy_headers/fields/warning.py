# -*- coding: utf-8 -*-

from .. import exceptions
from ..shared import bases
from ..shared import checkers
from ..shared import cleaners
from ..shared import constraints
from ..shared import dates
from ..shared import parsers


def warning(code, uri_or_token, message, date_time=None):
    return code, uri_or_token, message, date_time


class Warning(bases.MultiHeaderBase):
    """
    Sent by server only.

    The ``Warning`` header field is used to carry\
    additional information about the status or\
    transformation of a message that might not be\
    reflected in the status code. This information\
    is typically used to warn about possible\
    incorrectness introduced by caching operations\
    or transformations applied to the payload\
    of the message.

    Example::

        Warning([
            warning(
                code=112,
                uri_or_token='-',
                message='network down',
                date_time=datetime.now())
        ])

        Warning([
            warning(
                code=112,
                uri_or_token='-',
                message='network down')
        ])

    Date-time must match the Date header.

    `Ref. <http://httpwg.org/specs/rfc7234.html#header.warning>`_
    """

    name = 'warning'
    codes = {
        110,
        111,
        112,
        113,
        199,
        214,
        299}
    codes_str = {
        str(c)
        for c in codes}

    def __init__(self, values=None, raw_values_collection=None):
        """

        assert len(values) == 1
        assert values[0][0] in {110, 111, 112, 113, 199, 214, 299}
        assert (checkers.is_token(values[0][1]) or
                checkers.is_uri(values[0][1]))
        assert (values[0][3] is None or
                isinstance(values[0][3], datetime.datetime))
                """

        # ((3 digit code, uri/token, quoted-string), ) or
        # ((3 digit code, uri/token, quoted-string, quoted-date-time), )
        super().__init__(
            values=values,
            raw_values_collection=raw_values_collection)

    def value_str(self, value):
        code, uri_or_token, message, date_time = value

        if date_time:
            return (
                '{code} {token} '
                '{message} "{date_time}"'
                .format(
                    code=code,
                    token=uri_or_token,
                    message=parsers.quote(message),
                    date_time=dates.format_date(date_time)))
        else:
            return '{code} {token} {message}'.format(
                code=code,
                token=uri_or_token,
                message=parsers.quote(message))

    def values_str(self, values):
        return ', '.join(
            self.value_str(v)
            for v in values)

    def clean_value(self, raw_value):
        raw_values = tuple(parsers.from_raw_values(
            raw_value,
            separator=' '))

        try:
            code, agent, text, date = raw_values
        except ValueError:
            try:
                code, agent, text = raw_values
            except ValueError:
                raise exceptions.BadRequest(
                    'Expected "code agent text date" '
                    'or "code agent text" format')
            else:
                date = None

        constraints.must_be_in(code, self.codes_str)
        constraints.constraint(
            checkers.is_uri(agent) or
            checkers.is_token(agent),
            'Agent value is not a valid uri or token')
        constraints.constraint(
            checkers.is_quoted_string(text),
            'Text value must be a quoted-string')
        constraints.constraint(
            date is None or
            (len(date) >= 2 and
             date.startswith('"') and
             date.endswith('"')),
            'Date must be a quoted date')

        code = cleaners.clean_number(code, max_chars=3)
        text = parsers.dequote(text)

        if date is not None:
            date = dates.clean_date_time(date[1:-1])

        return code, agent, text, date
