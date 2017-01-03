# -*- coding: utf-8 -*-

from ..shared.common import language_tags
from ..shared import bases


content_language = language_tags.language_tag


class ContentLanguage(bases.TokensHeaderBase):
    """
    The ``Content-Language`` header field describes the\
    natural language(s) of the intended audience for\
    the representation. Note that this might not be\
    equivalent to all the languages used within the\
    representation.

    Example::

        ContentLanguage([
            content_language('mi'),
            content_language('en')
            content_language('en', region='gb')
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.content-language>`_
    """

    name = 'content-language'

    def check_value(self, value):
        language_tags.check_language_tag(value)

    def values_str(self, values):
        return ', '.join(
            language_tags.format_language_tag(*value)
            for value in values)

    def clean_value(self, raw_value):
        return language_tags.clean_language_tag(raw_value)
