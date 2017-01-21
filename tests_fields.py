# -*- coding: utf-8 -*-

import unittest
import datetime

from http_lazy_headers import fields
from http_lazy_headers.shared import parameters


class FieldTestCase(unittest.TestCase):

    field = None

    def assertFieldRawEqual(self, raw_values, expected):
        self.assertEqual(
            self.field(
                raw_values_collection=raw_values).values(),
            expected)

    def assertFieldStrEqual(self, values, expected):
        self.assertEqual(
            str(self.field(values=values)),
            expected)


class WWWAuthenticateTest(FieldTestCase):

    field = fields.WWWAuthenticate

    def test_raw_values(self):
        self.assertFieldRawEqual(
            [
                'Newauth realm="apps", type=1, '
                'title="Login to \\"apps\\"", '
                'Basic realm="simple"',
                'Foo asdqwe=='],
            (
                ('newauth', None, parameters.ParamsCI([
                    ('realm', 'apps'),
                    ('type', '1'),
                    ('title', 'Login to "apps"')])),
                ('basic', None, parameters.ParamsCI([
                    ('realm', 'simple')])),
                ('foo', 'asdqwe==', parameters.ParamsCI())))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('newauth', None, parameters.ParamsCI([
                    ('realm', 'apps'),
                    ('type', '1'),
                    ('title', 'Login to "apps"')])),
                ('basic', None, parameters.ParamsCI([
                    ('realm', 'simple')])),
                ('foo', 'asdqwe==', parameters.ParamsCI())),
            'www-authenticate: newauth realm=apps, '
            'type=1, title="Login to \\"apps\\"", '
            'basic realm=simple, foo asdqwe==')


class ContentDispositionTest(FieldTestCase):

    field = fields.ContentDisposition

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['attachment; filename="EURO rates"; '
             'filename*=utf-8\'en\'%e2%82%ac%20rates'],
            (
                ('attachment', parameters.ParamsCI([
                    ('filename', 'EURO rates'),
                    ('filename*', ('utf-8', 'en', '€ rates'))])),))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('attachment', parameters.ParamsCI([
                    ('filename', 'EURO rates'),
                    ('filename*', ('utf-8', 'en', '€ rates'))])),),
            'content-disposition: attachment;'
            'filename="EURO rates";'
            'filename*=utf-8\'en\'%E2%82%AC%20rates')


class CookieTest(FieldTestCase):

    field = fields.Cookie

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; lang=en-US'],
            (
                ('SID', '31d4d96e407aad42'),
                ('lang', 'en-US')))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('SID', '31d4d96e407aad42'),
                ('lang', 'en-US')),
            'cookie: SID=31d4d96e407aad42; lang=en-US')


from http_lazy_headers.fields.set_cookie import cookie_pair


class SetCookieTest(FieldTestCase):

    field = fields.SetCookie

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['SID=31d4d96e407aad42; Path=/; Domain=example.com',
             'SID2=foobar; Path=/foo; Secure; HttpOnly'],
            (cookie_pair(
                'SID',
                '31d4d96e407aad42',
                path='/',
                domain='example.com'),
             cookie_pair(
                 'SID2',
                 'foobar',
                 path='/foo',
                 secure=True,
                 http_only=True)))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                cookie_pair(
                    'SID',
                    '31d4d96e407aad42',
                    path='/',
                    domain='example.com'),
                cookie_pair(
                    'SID2',
                    'foobar',
                    path='/foo',
                    secure=True,
                    http_only=True)),
            'set-cookie: SID=31d4d96e407aad42; path=/; domain=example.com\r\n'
            'set-cookie: SID2=foobar; path=/foo; Secure; HttpOnly')


"""
class Test(FieldTestCase):

    field = fields.

    def test_raw_values(self):
        self.assertFieldRawEqual(
            [],
            ())

    def test_str(self):
        self.assertFieldStrEqual(
            (),
            '')
"""
