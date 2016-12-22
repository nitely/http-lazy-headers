# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import language_tags


# todo: this is basically the same as accept_language
def content_language(
        lang=None,
        ext_lang=(),
        script=None,
        region=None,
        variant=(),
        extension=(),
        private_use=(),
        grandfathered=None):
    assert lang or private_use or grandfathered
    assert (
        not private_use or
        (len(private_use) > 1 and
         private_use[0].lower() == 'x'))
    assert all(
        s and ext
        for s, ext in extension)
    assert all(private_use)
    assert all(variant)
    assert all(ext_lang)
    assert len(ext_lang) <= 3

    return (
        lang,
        ext_lang,
        script,
        region,
        variant,
        extension,
        private_use,
        grandfathered)


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

    def values_str(self, values):
        return ', '.join(
            language_tags.format_language_tag(*value)
            for value in values)

    def clean_value(self, raw_value):
        return language_tags.clean_language_tag(raw_value)
