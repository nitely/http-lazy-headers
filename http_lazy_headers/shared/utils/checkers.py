# -*- coding: utf-8 -*-

from . import ascii_tools


# 0-9 / A-Z / a-z
_ALPHA_NUM = frozenset(
    ascii_tools.ascii_chars(
        (0x30, 0x39),
        (0x41, 0x5A),
        (0x61, 0x7A)))

# All visible ASCII chars except delimiters
_TOKEN_CHARS = frozenset('!#$%&\'*+-.^_`|~') | _ALPHA_NUM

# Does not includes "=" sign
_TOKEN68_CHARS = frozenset('-._~+/') | _ALPHA_NUM

# This does not includes "unwise" chars
_URI_CHARS = frozenset('-._~:/?#[]@!$&\'()*+,;=%') | _ALPHA_NUM

# All visible ASCII chars except double quotes
_ETAG_CHARS = frozenset(
    ascii_tools.ascii_chars(0x21, (0x23, 0x7E)))

_MIME_CHARSET_CHARS = frozenset('!#$%&+-^_`{}~') | _ALPHA_NUM
_MIME_CHARSET_VALUE_CHARS = frozenset('!#$%&+-.^_`|~') | _ALPHA_NUM

_LANG_CHARS = frozenset('-') | _ALPHA_NUM

_DIGIT_CHARS = frozenset(
    ascii_tools.ascii_chars((0x30, 0x39)))

# HTAB / SP / VCHAR
_ASCII_CHARS = frozenset(
    ascii_tools.ascii_chars(0x09, (0x20, 0x7E)))

# Token chars except "*" / "'" / "%"
_EXT_TOKEN = _TOKEN_CHARS - frozenset('*\'%')

# VCHAR
_VISIBLE_CHARS = frozenset(
    ascii_tools.ascii_chars((0x21, 0x7E)))


def is_token(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_TOKEN_CHARS)


def is_quoted_string(txt):
    assert isinstance(txt, str)

    if len(txt) < 2:  # Single quote?
        return False

    if (not txt.startswith('"') or
            not txt.endswith('"')):
        return False

    return True


def is_comment(txt):
    assert isinstance(txt, str)

    if (not txt.startswith('(') and
            not txt.endswith(')')):
        return False

    return True


def is_token68(txt):
    """
    http://httpwg.org/specs/rfc7235.html#challenge.and.response
    """
    assert isinstance(txt, str)

    txt = txt.rstrip('=')

    if not txt:
        return False

    return set(txt).issubset(_TOKEN68_CHARS)


def is_uri(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_URI_CHARS)


def is_etag(txt):
    assert isinstance(txt, str)

    if len(txt) < 2:  # Single quote?
        return False

    if (not txt.startswith('"') or
            not txt.endswith('"')):
        return False

    return set(txt[1:-1]).issubset(_ETAG_CHARS)


def is_mime_charset(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_MIME_CHARSET_CHARS)


def is_mime_charset_value(txt):
    assert isinstance(txt, str)

    # May be empty

    return set(txt).issubset(_MIME_CHARSET_VALUE_CHARS)


def is_lang_value(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_LANG_CHARS)


def is_number(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_DIGIT_CHARS)


def is_ascii(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_ASCII_CHARS)


def is_ext_token(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_EXT_TOKEN)


def is_visible_chars(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_VISIBLE_CHARS)


def is_alphanum(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_ALPHA_NUM)
