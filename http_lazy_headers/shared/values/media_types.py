# -*- coding: utf-8 -*-

from . import charsets
from .. import parameters


def media_type(
        top_level,
        sub_level,
        quality=None,
        charset=None,
        boundary=None):
    assert top_level in _TOP_LEVEL_VALUES
    assert sub_level in _SUB_LEVEL_VALUES
    assert (
        quality is None or
        (isinstance(quality, (int, float)) and
         0 <= quality <= 1))
    assert(
        charset is None or
        charset in charsets.CHARSET_VALUES)

    params = []

    if quality is not None:
        params.append(('q', quality))

    if charset:
        params.append(('charset', charset))

    if boundary:
        params.append(('boundary', boundary))

    return (top_level, sub_level), parameters.ParamsCI(params)


class TopLevel:

    star = '*'
    text = 'text'
    image = 'image'
    audio = 'audio'
    video = 'video'
    application = 'application'
    multipart = 'multipart'
    message = 'message'
    model = 'model'


class SubLevel:

    star = '*'

    # common text/*
    plain = 'plain'
    html = 'html'
    xml = 'xml'
    javascript = 'javascript'
    css = 'css'
    event_stream = 'event-stream'

    # common application/*
    json = 'json'
    www_form_url_encoded = 'x-www-form-urlencoded'
    msgpack = 'msgpack'
    octet_stream = 'octet-stream'

    # multipart/*
    form_data = 'form-data'

    # common image/*
    png = 'png'
    gif = 'gif'
    bmp = 'bmp'
    jpeg = 'jpeg'

    # audio/*
    mpeg = 'mpeg'
    mp4 = 'mp4'
    ogg = 'ogg'


def _attr_values(klass):
    return {
        getattr(klass, attr)
        for attr in vars(klass)
        if not attr.startswith('_')}


_TOP_LEVEL_VALUES = _attr_values(TopLevel)
_SUB_LEVEL_VALUES = _attr_values(SubLevel)


class MediaType(TopLevel, SubLevel):
    """"""
