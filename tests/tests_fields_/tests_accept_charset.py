# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AcceptCharsetTest(utils.FieldTestCase):

    field = hlh.AcceptCharset

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['iso-8859-5, unicode-1-1;q=0.8', 'utf-8'],
            ((hlh.Charsets.iso_8859_5.lower(), 1),
             (hlh.Charsets.utf_8.lower(), 1),
             ('unicode-1-1', 0.8)))

        self.assertFieldRawEqual(
            ['*'],
            (('*', 1),))

    def test_str(self):
        self.assertFieldStrEqual(
            ((hlh.Charsets.iso_8859_5, None),
             ('unicode-1-1', 0.8)),
            'accept-charset: ISO-8859-5, unicode-1-1; q=0.8')

        self.assertFieldStrEqual(
            ((hlh.Charsets.iso_8859_5, 0),
             ('unicode-1-1', 1)),
            'accept-charset: ISO-8859-5; q=0, unicode-1-1')

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

    def test_raw_bad_with_param(self):
        """
        Should not allow empty value and non-empty params
        """
        self.assertRaisesHeaderError(['q=1'])

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['iso-8859-5'])
        self.assertRawOK(['iso-8859-5;q=0'])
        self.assertRaisesHeaderError([';'])
        self.assertRaisesHeaderError([';q=0'])
        self.assertRaisesHeaderError([';=;;q=0'])
        self.assertRaisesHeaderError(['iso-8859-5;'])
        self.assertRaisesHeaderError(['iso-8859-5;q'])
        self.assertRaisesHeaderError(['iso-8859-5;q='])
        self.assertRaisesHeaderError(['iso-8859-5;q=a'])
        self.assertRaisesHeaderError(['iso-8859-5;q=5'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_charset = 'iso-8859-5'
        self.assertOK([(good_charset, None)])
        self.assertOK([(good_charset, 1)])
        self.assertOK([(good_charset, 0.5)])
        self.assertRaisesInternalError([('', 1)])
        self.assertRaisesInternalError([(';', 1)])
        self.assertRaisesInternalError([('=', 1)])
        self.assertRaisesInternalError([(good_charset, '')])
        self.assertRaisesInternalError([(good_charset, 'a')])
        self.assertRaisesInternalError([good_charset])
        self.assertRaisesInternalError([
            (good_charset, good_charset, good_charset)])
        self.assertRaisesInternalError([(good_charset, 5)])
        self.assertRaisesInternalError([(None, None)])
