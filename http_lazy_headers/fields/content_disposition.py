# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import constraints
from ..shared import parsers
from ..shared import cleaners
from ..shared import parameters
from ..shared import helpers


def content_disposition_filename(
        file_name,
        charset='utf-8',
        lang='en',
        disposition_type='attachment',
        fallback_name=None):
    assert (
        file_name and
        isinstance(file_name, str))
    assert (
        not fallback_name or
        isinstance(fallback_name, str))

    fallback_name = str(
            bytes(
                fallback_name or file_name,
                encoding='ascii',
                errors='replace'),
            encoding='ascii')

    return (
        disposition_type,
        parameters.Params((
            ('filename', fallback_name),
            ('filename*', (charset, lang, file_name)),)))


class ContentDisposition(bases.SingleHeaderBase):
    """
    Sent by server only.

    Is up to the user to recover from a bad file name or not.

    The ``Content-Disposition`` response header field is\
    used to convey additional information about how to\
    process the response payload, and also can be used\
    to attach additional metadata, such as the filename\
    to use when saving the response payload locally.

    Example::

        ContentDisposition([
            content_disposition_filename('áéíóú.zip')
        ])

        ContentDisposition([(
            Disposition.attachment,
            Params([
                ('filename*', ('utf-8', 'en', 'áéíóú.zip'))
            ])
        )])

        ContentDisposition([(
            Disposition.attachment,
            Params([
                ('filename*', ('utf-8', None, 'áéíóú.zip'))
            ])
        )])

        ContentDisposition([(
            Disposition.attachment,
            Params([
                ('filename', 'aeiou.zip'),
                ('filename*', ('utf-8', None, 'áéíóú.zip'))
            ])
        )])

    `Ref. <https://tools.ietf.org/html/rfc6266>`_
    """

    name = 'content-disposition'

    def values_str(self, values):
        disposition_type, params = values[0]

        if not params:
            return disposition_type

        return '{};{}'.format(
            disposition_type,
            ';'.join(
                helpers.format_ext_params(params)))

    def clean_value(self, raw_value):
        raw_value, raw_params = parsers.from_raw_value_with_params(raw_value)
        constraints.must_be_token(raw_value)
        return raw_value.lower(), cleaners.clean_extended_params(raw_params)
