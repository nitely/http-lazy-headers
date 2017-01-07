# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ContentEncodingTest(utils.FieldTestCase):

    field = hlh.ContentEncoding

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['compress', 'gzip, deflate'],
            (hlh.Encodings.compress,
             hlh.Encodings.gzip,
             hlh.Encodings.deflate))

        self.assertFieldRawEqual(
            ['br, compress, deflate, exi, gzip, '
             'identity, pack200-gzip, x-compress, x-gzip'],
            (hlh.Encodings.br,
             hlh.Encodings.compress,
             hlh.Encodings.deflate,
             hlh.Encodings.exi,
             hlh.Encodings.gzip,
             hlh.Encodings.identity,
             hlh.Encodings.pack200_gzip,
             hlh.Encodings.x_compress,
             hlh.Encodings.x_gzip))

        self.assertFieldRawEqual(
            ['GziP'],
            (hlh.Encodings.gzip,))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.Encodings.compress,
             hlh.Encodings.gzip,
             hlh.Encodings.deflate),
            'content-encoding: compress, gzip, deflate')

        self.assertFieldStrEqual(
            (hlh.Encodings.br,
             hlh.Encodings.compress,
             hlh.Encodings.deflate,
             hlh.Encodings.exi,
             hlh.Encodings.gzip,
             hlh.Encodings.identity,
             hlh.Encodings.pack200_gzip,
             hlh.Encodings.x_compress,
             hlh.Encodings.x_gzip),
            'content-encoding: br, compress, deflate, '
            'exi, gzip, identity, pack200-gzip, '
            'x-compress, x-gzip')

        self.assertFieldStrEqual(
            ('GziP',),
            'content-encoding: GziP')

    def test_raw_empty(self):
        """
        Should NOT allow empty raw value
        """
        self.assertRaisesHeaderError([''])

    def test_empty(self):
        """
        Should NOT allow empty value
        """
        self.assertRaisesInternalError(())

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['gzip'])
        self.assertRaisesHeaderError(['gzip;'])
        self.assertRaisesHeaderError(['='])
        self.assertRaisesHeaderError(['('])
        self.assertRaisesHeaderError(['unknown'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK(['gzip'])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([';'])
        self.assertRaisesInternalError(['('])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError(['unknown'])
