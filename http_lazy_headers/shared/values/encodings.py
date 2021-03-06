# -*- coding: utf-8 -*-

from ..utils import misc


class CEncodings:

    br = 'br'
    compress = 'compress'
    deflate = 'deflate'
    exi = 'exi'
    gzip = 'gzip'
    identity = 'identity'
    pack200_gzip = 'pack200-gzip'
    x_compress = 'x-compress'
    x_gzip = 'x-gzip'


class TEncodings:

    chunked = 'chunked'
    compress = 'compress'
    deflate = 'deflate'
    gzip = 'gzip'
    identity = 'identity'
    x_compress = 'x-compress'
    x_gzip = 'x-gzip'


class Encodings(CEncodings, TEncodings):
    """
    All encodings, including content and transfer

    `Ref. <http://www.iana.org/assignments/http-parameters/http-parameters.xhtml>`_
    """


CONTENT_ENCODING_VALUES = misc.vars_for(CEncodings)
ENCODING_VALUES = misc.vars_for(Encodings)
