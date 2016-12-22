# -*- coding: utf-8 -*-

from .. import exceptions
from ..shared import constraints
from ..shared import checkers


(LANG,
 EXT_LANG,
 SCRIPT,
 REGION,
 VARIANT,
 EXTENSION,
 PRIVATE_USE,
 GRANDFATHERED) = range(8)

_GRANDFATHERED_MAP = {
    # Irregular
    'en-gb-oed': 'en-gb-oxendict',
    'i-ami': 'ami',
    'i-bnn': 'bnn',
    'i-default': None,
    'i-enochian': None,
    'i-hak': 'hak',
    'i-klingon': 'tlh',
    'i-lux': 'lb',
    'i-mingo': None,
    'i-navajo': 'nv',
    'i-pwn': 'pwn',
    'i-tao': 'tao',
    'i-tay': 'tay',
    'i-tsu': 'tsu',
    'sgn-be-fr': 'sfb',
    'sgn-be-nl': 'vgt',
    'sgn-ch-de': 'sgg',

    # Regular
    'art-lojban': 'jbo',
    'cel-gaulish': None,
    'no-bok': 'nb',
    'no-nyn': 'nn',
    'zh-guoyu': 'cmn',
    'zh-hakka': 'hak',
    'zh-min': None,
    'zh-min-nan': 'nan',
    'zh-xiang': 'hsn'}


def is_alphanum(txt):
    return True


def is_alpha(txt):
    return True


def format_language_tag(
        lang,
        ext_lang,
        script,
        region,
        variant,
        extension,
        private_use,
        grandfathered):
    if grandfathered:
        return grandfathered

    # Extensions must be ordered,
    # see https://tools.ietf.org/html/rfc5646#section-4.5
    extension = (
        '{}-{}'.format(key, '-'.join(ext))
        for key, ext in sorted(extension))

    return '-'.join(
        sub_tag
        for sub_tag in (
            lang,
            '-'.join(ext_lang),
            script,
            region,
            '-'.join(variant),
            '-'.join(extension),
            '-'.join(private_use))
        if sub_tag)


def accept_language_value(
        lang=None,
        ext_lang=(),
        script=None,
        region=None,
        variant=(),
        extension=(),
        private_use=(),
        grandfathered=None):
    assert any(locals())

    return (
        lang,
        ext_lang,
        script,
        region,
        variant,
        extension,
        private_use,
        grandfathered)


def _preferred_language_tag(raw_language_tag):
    return (_GRANDFATHERED_MAP.get(raw_language_tag, None) or
            raw_language_tag)


def clean_language_tag(raw_language_tag):
    # https://tools.ietf.org/html/rfc5646#section-2.1

    raw_language_tag = _preferred_language_tag(
        raw_language_tag.lower())

    if raw_language_tag in _GRANDFATHERED_MAP:
        return accept_language_value(
            grandfathered=raw_language_tag)

    curr = LANG
    lang_tag = [None for _ in range(8)]
    ext_lang = []
    variants = []
    extensions = []
    seen_extensions = set()
    privates = []

    for sub_tag in raw_language_tag.split('-', 50):
        constraints.constraint(
            len(sub_tag) <= 8,
            'Sub-tag is too long')
        constraints.constraint(
            is_alphanum(sub_tag))

        sub_tag_len = len(sub_tag)

        if curr == LANG:
            constraints.constraint(
                sub_tag_len >= 2)
            constraints.constraint(
                is_alpha(sub_tag))

            lang_tag[LANG] = sub_tag

            if sub_tag_len < 4:
                curr = EXT_LANG
            else:
                curr = SCRIPT

            continue

        if curr == EXT_LANG:
            if (sub_tag_len == 3 and
                    len(ext_lang) < 3 and
                    is_alpha(sub_tag)):
                ext_lang.append(sub_tag)
                continue

            curr = SCRIPT

        if curr == SCRIPT:
            curr = REGION

            if sub_tag_len == 4 and is_alpha(sub_tag):
                lang_tag[SCRIPT] = sub_tag
                continue

        if curr == REGION:
            curr = VARIANT

            if sub_tag_len == 2 and is_alpha(sub_tag):
                lang_tag[REGION] = sub_tag
                continue

            if sub_tag_len == 3 and checkers.is_number(sub_tag):
                lang_tag[REGION] = sub_tag
                continue

        if curr == VARIANT:
            if sub_tag_len >= 5:
                variants.append(sub_tag)
                continue

            if sub_tag_len == 4 and checkers.is_number(sub_tag[0]):
                variants.append(sub_tag)
                continue

            curr = EXTENSION

        # https://tools.ietf.org/html/rfc5646#section-2.2.6
        if curr == EXTENSION:
            if sub_tag_len == 1 and sub_tag[0] != 'x':
                constraints.constraint(
                    sub_tag not in seen_extensions,
                    'Extension must not be duplicated')

                extensions.append((sub_tag, []))
                seen_extensions.add(sub_tag)
                continue

            if sub_tag_len >= 2 and extensions:
                extensions[-1][1].append(sub_tag)
                continue

            curr = PRIVATE_USE

        if curr == PRIVATE_USE:
            if sub_tag_len == 1 and sub_tag[0] == 'x':
                privates.append(sub_tag)
                continue

            if privates:
                privates.append(sub_tag)
                continue

        raise exceptions.HeaderError('Bad language-tag')

    constraints.constraint(
        lang_tag[LANG] or privates,
        'Value must have a language, '
        'private-use or grandfathered')
    constraints.constraint(
        all(
            ext[1]
            for ext in extensions),
        'Extension must have a value')
    constraints.constraint(
        not privates or len(privates) > 1,
        'Private-use must have a value')

    lang_tag[EXT_LANG] = tuple(ext_lang)
    lang_tag[VARIANT] = tuple(variants)
    lang_tag[EXTENSION] = tuple(
        (ext[0], tuple(ext[1]))
        for ext in extensions)
    lang_tag[PRIVATE_USE] = tuple(privates)

    return accept_language_value(*lang_tag)
