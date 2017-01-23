# -*- coding: utf-8 -*-

import datetime

import http_lazy_headers as hlh

from . import utils


class SetCookieTest(utils.FieldTestCase):

    field = hlh.SetCookie
    date = datetime.datetime(
        year=1994,
        month=11,
        day=15,
        hour=8,
        minute=12,
        second=31)

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42'),))

        self.assertFieldRawEqual(
            ['SID = 31d4d96e407aad42'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42'),))

        self.assertFieldRawEqual(
            ['SID=""'],
            (hlh.cookie_pair(
                'SID',
                ''),))

        self.assertFieldRawEqual(
            ['SID='],
            (hlh.cookie_pair(
                'SID',
                ''),))

        # todo: fixme, Not allowed by the ABNF
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42;'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42'),))

        # todo: fixme, Not allowed by the ABNF
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; ; Path=/'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/'),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42', 'SID2=foobar'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42'),
             hlh.cookie_pair(
                 'SID2',
                 'foobar')))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; Path=/AbOuT'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/AbOuT'),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42;pAtH=/'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/'),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42;Path=/'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/'),))

        self.assertFieldRawEqual(
            ['SID=; Path=/'],
            (hlh.cookie_pair(
                'SID',
                '',
                path='/'),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'Domain=xn--www.alliancefranaise.nu-dbc'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                domain='www.alliancefrançaise.nu'),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; Path=/; Domain=example.com',
             'SID2=foobar; Path=/foo; Secure; HttpOnly'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/',
                domain='example.com'),
             hlh.cookie_pair(
                 'SID2',
                 'foobar',
                 path='/foo',
                 secure=True,
                 http_only=True)))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; pAtH=/; dOmAiN=example.com'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/',
                domain='example.com'),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'Expires=Tue, 15 Nov 1994 08:12:31 GMT'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                expires=self.date),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'eXpIrEs=Tue, 15 Nov 1994 08:12:31 GMT'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                expires=self.date),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'max-age=360'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                max_age=360),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'mAx-aGe=360'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                max_age=360),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'foo'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                extension=['foo']),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'FoO'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                extension=['FoO']),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'foo; '
             'bar; '
             'baz=quz'],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                extension=['foo', 'bar', 'baz=quz']),))

        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; '
             'secure; '
             'httpOnly; '],
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                extension=['secure', 'httpOnly']),))

        self.assertFieldRawEqual(
            ['SID2=foobar; '
             'Path=/foo; '
             'Domain=example.com ; '
             'Expires=Tue, 15 Nov 1994 08:12:31 GMT; '
             'Max-Age=360; '
             'Secure; '
             'HttpOnly'],
            (hlh.cookie_pair(
                'SID2',
                'foobar',
                path='/foo',
                domain='example.com',
                expires=self.date,
                max_age=360,
                secure=True,
                http_only=True),))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42'),),
            'set-cookie: SID=31d4d96e407aad42')

        self.assertFieldStrEqual(
            (hlh.cookie_pair(
                'SID',
                ''),),
            'set-cookie: SID=')

        self.assertFieldStrEqual(
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/',
                domain='example.com'),
             hlh.cookie_pair(
                 'SID2',
                 'foobar',
                 path='/foo',
                 secure=True,
                 http_only=True)),
            'set-cookie: SID=31d4d96e407aad42; path=/; domain=example.com\r\n'
            'set-cookie: SID2=foobar; path=/foo; Secure; HttpOnly')

        self.assertFieldStrEqual(
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/AbOuT'),),
            'set-cookie: SID=31d4d96e407aad42; path=/AbOuT')

        self.assertFieldStrEqual(
            (hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                domain='www.alliancefrançaise.nu'),),
            'set-cookie: SID=31d4d96e407aad42; '
            'domain=xn--www.alliancefranaise.nu-dbc')

        self.assertFieldStrEqual(
            (hlh.cookie_pair(
                'SID2',
                'foobar',
                path='/foo',
                domain='example.com',
                expires=self.date,
                max_age=360,
                extension=['foo', 'bar', 'baz=qux'],
                secure=True,
                http_only=True),),
            'set-cookie: SID2=foobar; path=/foo; '
            'domain=example.com; expires=Tue, 15 Nov 1994 08:12:31 GMT; '
            'max-age=360; Secure; HttpOnly; foo; bar; baz=qux')

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
        self.assertRawOK(['SID=31d4d96e407aad42'])
        self.assertRawOK(['SID="foo"; Path=/'])
        self.assertRaisesHeaderError(['foo'])
        self.assertRaisesHeaderError(['foo; Path=/'])
        self.assertRaisesHeaderError(['SID="foo"; Path='])
        self.assertRaisesHeaderError(['SID="foo"; Path=foo'])
        self.assertRaisesHeaderError(['SID="foo"; Domain='])
        self.assertRaisesHeaderError(['SID="foo"; Domain=foo'])
        self.assertRaisesHeaderError(['SID="foo"; Domain=127.0.0.1'])
        self.assertRaisesHeaderError(['SID="foo"; expires='])
        self.assertRaisesHeaderError(['SID="foo"; expires=0'])
        self.assertRaisesHeaderError([
            'SID="foo"; expires=Mon, 15 Nov 1994 08:12:31 GMT'])
        self.assertRaisesHeaderError(['SID="foo"; max-age='])
        self.assertRaisesHeaderError(['SID="foo"; max-age=foo'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_set_cookie = hlh.cookie_pair(
            'SID',
            '31d4d96e407aad42')
        self.assertOK([good_set_cookie])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='')])
        self.assertRaisesInternalError([
            hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='foo')])
        self.assertRaisesInternalError([
            hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                domain='foo')])
        self.assertRaisesInternalError([
            hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                max_age='foo')])
        self.assertRaisesInternalError([
            hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                expires=0)])
        self.assertRaisesInternalError([
            hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                extension=[''])])
        self.assertRaisesInternalError([
            hlh.cookie_pair(
                'SID',
                '31d4d96e407aad42',
                extension=[';'])])
