# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class TransferEncodingTest(utils.FieldTestCase):

    field = hlh.TransferEncoding

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['gzip, chunked', 'foobar;bar=qux'],
            ((hlh.Encodings.gzip, hlh.ParamsCI()),
             (hlh.Encodings.chunked, hlh.ParamsCI()),
             ('foobar', hlh.ParamsCI([('bar', 'qux')]))))

        self.assertFieldRawEqual(
            ['GziP'],
            ((hlh.Encodings.gzip, hlh.ParamsCI()),))

    def test_str(self):
        self.assertFieldStrEqual(
            ((hlh.Encodings.gzip, hlh.ParamsCI()),
             (hlh.Encodings.chunked, hlh.ParamsCI()),
             ('foobar', hlh.ParamsCI([('bar', 'qux')]))),
            'transfer-encoding: gzip, chunked, foobar; bar=qux')

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
        self.assertRawOK(['foo'])
        self.assertRawOK(['foo;bar=baz'])
        self.assertRaisesHeaderError(['^='])
        self.assertRaisesHeaderError(['foo;'])
        self.assertRaisesHeaderError(['foo;='])
        self.assertRaisesHeaderError(['foo;bar='])
        self.assertRaisesHeaderError(['foo;bar = baz'])
        self.assertRaisesHeaderError(['foo;bar= baz'])
        self.assertRaisesHeaderError(['foo;bar =baz'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_te = ('foo', hlh.ParamsCI())
        self.assertOK([good_te])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([('', hlh.ParamsCI())])
        self.assertRaisesInternalError([(None, hlh.ParamsCI())])
        self.assertRaisesInternalError([('foo', None)])
