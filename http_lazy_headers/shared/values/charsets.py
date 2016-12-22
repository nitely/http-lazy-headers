# -*- coding: utf-8 -*-


class Charsets:
    # http://www.iana.org/assignments/character-sets/character-sets.xhtml

    us_ascii = 'US-ASCII'
    iso_8859_1 = 'ISO-8859-1'
    iso_8859_2 = 'ISO-8859-2'
    iso_8859_3 = 'ISO-8859-3'
    iso_8859_4 = 'ISO-8859-4'
    iso_8859_5 = 'ISO-8859-5'
    iso_8859_6 = 'ISO-8859-6'
    iso_8859_7 = 'ISO-8859-7'
    iso_8859_8 = 'ISO-8859-8'
    iso_8859_9 = 'ISO-8859-9'
    iso_8859_10 = 'ISO-8859-10'
    shift_jis = 'Shift_JIS'
    euc_jp = 'EUC-JP'
    iso_2022_kr = 'ISO-2022-KR'
    euc_kr = 'EUC-KR'
    iso_2022_jp = 'ISO-2022-JP'
    iso_2022_jp_2 = 'ISO-2022-JP-2'
    iso_8859_6_e = 'ISO-8859-6-E'
    iso_8859_6_i = 'ISO-8859-6-I'
    iso_8859_8_e = 'ISO-8859-8-E'
    iso_8859_8_i = 'ISO-8859-8-I'
    gb2312 = 'GB2312'
    big5 = 'Big5'
    koi8_r = 'KOI8-R'

    # Common
    utf_8 = 'UTF-8'


CHARSET_VALUES = {
    getattr(Charsets, attr)
    for attr in vars(Charsets)
    if not attr.startswith('_')}

