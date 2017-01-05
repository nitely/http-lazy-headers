# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AcceptEncodingTest(utils.FieldTestCase):

    field = hlh.AcceptEncoding

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['compress, gzip'],
            ((hlh.Encodings.compress, 1),
             (hlh.Encodings.gzip, 1)))

        self.assertFieldRawEqual(
            ['*'],
            (('*', 1),))

        self.assertFieldRawEqual(
            ['compress;q=0.5, gzip;q=1.0'],
            ((hlh.Encodings.gzip, 1),
             (hlh.Encodings.compress, 0.5)))

        self.assertFieldRawEqual(
            ['gzip;q=1.0, identity; q=0.5', '*;q=0'],
            ((hlh.Encodings.gzip, 1),
             (hlh.Encodings.identity, 0.5),
             ('*', 0)))

    def test_str(self):
        self.assertFieldStrEqual(
            ((hlh.Encodings.gzip, 1.0),
             (hlh.Encodings.identity, 0.5),
             ('*', 0)),
            'accept-encoding: gzip, identity; q=0.5, *; q=0')

    def test_raw_empty(self):
        """
        Should allow empty raw value
        """
        self.assertFieldRawEqual(
            [''],
            ())

    def test_empty(self):
        """
        Should allow empty value
        """
        self.assertFieldStrEqual(
            (),
            'accept-encoding: ')

    def test_raw_bad_with_param(self):
        """
        Should not allow empty value and non-empty params
        """
        self.assertRaisesHeaderError(['q=1'])

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['gzip'])
        self.assertRawOK(['gzip;q=0'])
        self.assertRaisesHeaderError([';'])
        self.assertRaisesHeaderError([';=;;q=0'])
        self.assertRaisesHeaderError(['gzip;'])
        self.assertRaisesHeaderError(['gzip;q'])
        self.assertRaisesHeaderError(['gzip;q='])
        self.assertRaisesHeaderError(['gzip;q=1.1'])
        self.assertRaisesHeaderError(['gzip;q=a'])
        self.assertRaisesHeaderError(['gzip;bad=1'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_encoding = 'gzip'
        self.assertOK([(good_encoding, None)])
        self.assertOK([(good_encoding, 1)])
        self.assertOK([(good_encoding, 0.5)])
        self.assertRaisesInternalError([('', 1)])
        self.assertRaisesInternalError([(good_encoding, '')])
        self.assertRaisesInternalError([(good_encoding, 'a')])
        self.assertRaisesInternalError([(good_encoding, 5)])
        self.assertRaisesInternalError([
            (good_encoding, good_encoding, good_encoding)])
        self.assertRaisesInternalError([(None, 5)])
        self.assertRaisesInternalError([(None, None)])
