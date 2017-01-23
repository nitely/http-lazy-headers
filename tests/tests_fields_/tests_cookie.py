# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class CookieTest(utils.FieldTestCase):

    field = hlh.Cookie

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; lang=en-US'],
            (('SID', '31d4d96e407aad42'),
             ('lang', 'en-US')))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42'],
            (('SID', '31d4d96e407aad42'),))

        self.assertFieldRawEqual(
            ['SID = 31d4d96e407aad42'],
            (('SID', '31d4d96e407aad42'),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42;lang=en-US'],
            (('SID', '31d4d96e407aad42'),
             ('lang', 'en-US')))

        self.assertFieldRawEqual(
            ['SID="31d4d96e407aad42"'],
            (('SID', '31d4d96e407aad42'),))

        self.assertFieldRawEqual(
            ['SID=""'],
            (('SID', ''),))

        self.assertFieldRawEqual(
            ['SID='],
            (('SID', ''),))

        self.assertFieldRawEqual(
            ['SID=; lang=en-US'],
            (('SID', ''),
             ('lang', 'en-US')))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; SID=foo'],
            (('SID', '31d4d96e407aad42'),
             ('SID', 'foo')))

        # todo: fixme, Not allowed by the ABNF
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42;'],
            (('SID', '31d4d96e407aad42'),))

        # todo: fixme, Not allowed by the ABNF
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; ;lang=en-US'],
            (('SID', '31d4d96e407aad42'),
             ('lang', 'en-US')))

    def test_str(self):
        self.assertFieldStrEqual(
            (('SID', '31d4d96e407aad42'),
             ('lang', 'en-US')),
            'cookie: SID=31d4d96e407aad42; lang=en-US')

        self.assertFieldStrEqual(
            (('SID', '31d4d96e407aad42'),),
            'cookie: SID=31d4d96e407aad42')

        self.assertFieldStrEqual(
            (('SID', ''),),
            'cookie: SID=')

        self.assertFieldStrEqual(
            (('SID', '31d4d96e407aad42'),
             ('SID', 'foo')),
            'cookie: SID=31d4d96e407aad42; SID=foo')

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
        self.assertRawOK(['SID=31d4d96e407aad42; lang=en-US'])
        self.assertRawOK(['SID="foo"'])
        self.assertRaisesHeaderError(['SID="\""'])
        self.assertRaisesHeaderError(['SID=foo"'])
        self.assertRaisesHeaderError(['SID="foo'])
        self.assertRaisesHeaderError(['SID="foo\\"'])
        self.assertRaisesHeaderError(['SID="foo;"'])
        self.assertRaisesHeaderError(['SID="foo,"'])
        self.assertRaisesHeaderError(['SID="foo bar"'])
        self.assertRaisesHeaderError(['SID="'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_cookie = ('SID', '31d4d96e407aad42')
        self.assertOK([good_cookie])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            ('SID', '"31d4d96e407aad42"')])
        self.assertRaisesInternalError([
            ('SID', '"\""')])
        self.assertRaisesInternalError([
            ('SID', '"')])
