# -*- coding: utf-8 -*-


class Encodings:

    # http://www.iana.org/assignments/http-parameters/http-parameters.xhtml

    chunked = 'chunked'
    gzip = 'gzip'
    deflate = 'deflate'
    compress = 'compress'
    identity = 'identity'  # Accept-Encoding only


ENCODING_VALUES = {
    getattr(Encodings,attr)
    for attr in vars(Encodings)
    if not attr.startswith('_')}
