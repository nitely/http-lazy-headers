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


class AcceptTest(FieldTestCase):

    field = fields.Accept

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['text/html, foo/bar;baz=qux', '*/*;q=0.5'],
            (
                (('foo', 'bar'), parameters.ParamsCI([('baz', 'qux'), ('q', 1)])),
                (('text', 'html'), parameters.ParamsCI([('q', 1)])),
                (('*', '*'), parameters.ParamsCI([('q', 0.5)]))))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                (('foo', 'bar'), parameters.ParamsCI([('baz', 'qux')])),
                (('*', '*'), parameters.ParamsCI([('q', 0.5)]))),
            'accept: foo/bar;baz=qux, */*;q=0.5')


class AcceptCharsetTest(FieldTestCase):

    field = fields.AcceptCharset

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['iso-8859-5, unicode-1-1;q=0.8', 'utf-8'],
            (
                ('iso-8859-5', parameters.ParamsCI([('q', 1)])),
                ('utf-8', parameters.ParamsCI([('q', 1)])),
                ('unicode-1-1', parameters.ParamsCI([('q', 0.8)]))))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('iso-8859-5', parameters.ParamsCI()),
                ('unicode-1-1', parameters.ParamsCI([('q', 0.8)]))),
            'accept-charset: iso-8859-5, unicode-1-1;q=0.8')


class AcceptEncodingTest(FieldTestCase):

    field = fields.AcceptEncoding

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['gzip;q=1.0, identity; q=0.5', '*;q=0'],
            (
                ('gzip', parameters.ParamsCI([('q', 1)])),
                ('identity', parameters.ParamsCI([('q', 0.5)])),
                ('*', parameters.ParamsCI([('q', 0)]))))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('gzip', parameters.ParamsCI([('q', 1.0)])),
                ('identity', parameters.ParamsCI([('q', 0.5)])),
                ('*', parameters.ParamsCI([('q', 0)]))),
            'accept-encoding: gzip;q=1.0, identity;q=0.5, *;q=0')


class AcceptLanguageTest(FieldTestCase):

    field = fields.AcceptLanguage

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['da, en-gb;q=0.8', 'en;q=0.7'],
            (
                (('da', (), None, None, (), (), (), None),
                 parameters.ParamsCI([('q', 1)])),
                (('en', (), None, 'gb', (), (), (), None),
                 parameters.ParamsCI([('q', 0.8)])),
                (('en', (), None, None, (), (), (), None),
                 parameters.ParamsCI([('q', 0.7)]))))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                (('da', (), None, None, (), (), (), None),
                 parameters.ParamsCI()),
                (('en', (), None, 'gb', (), (), (), None),
                 parameters.ParamsCI([('q', 0.8)])),
                (('en', (), None, None, (), (), (), None),
                 parameters.ParamsCI([('q', 0.7)]))),
            'accept-language: da, en-gb;q=0.8, en;q=0.7')


class AcceptRangesTest(FieldTestCase):

    field = fields.AcceptRanges

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['bytes'],
            ('bytes',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('bytes',),
            'accept-ranges: bytes')


class AgeTest(FieldTestCase):

    field = fields.Age

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['60'],
            (60,))

    def test_str(self):
        self.assertFieldStrEqual(
            (60,),
            'age: 60')


class AllowTest(FieldTestCase):

    field = fields.Allow

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['GET, POST', 'PATCH'],
            (
                'GET',
                'POST',
                'PATCH'))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                'GET',
                'POST',
                'PATCH'),
            'allow: GET, POST, PATCH')


class AuthorizationTest(FieldTestCase):

    field = fields.Authorization

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Bearer foo'],
            (
                (('bearer', 'foo', parameters.ParamsCI()),)))

    def test_str(self):
        self.assertFieldStrEqual(
            (('bearer', 'foo', parameters.ParamsCI()),),
            'authorization: bearer foo')


class CacheControlTest(FieldTestCase):

    field = fields.CacheControl

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['no-cache, private', 'max-age=60, foo=bar'],
            (
                parameters.ParamsCI((
                    ('no-cache', ()),
                    ('private', ()),
                    ('max-age', 60),
                    ('foo', 'bar'))),))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                parameters.ParamsCI((
                    ('no-cache', ()),
                    ('private', ()),
                    ('max-age', 60),
                    ('foo', 'bar'))),),
            'cache-control: no-cache, private, max-age=60, foo=bar')


class ConnectionTest(FieldTestCase):

    field = fields.Connection

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['keep-alive, upgrade', 'foo'],
            ('keep-alive', 'upgrade', 'foo'))

    def test_str(self):
        self.assertFieldStrEqual(
            ('keep-alive', 'upgrade', 'foo'),
            'connection: keep-alive, upgrade, foo')


class ContentEncodingTest(FieldTestCase):

    field = fields.ContentEncoding

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['compress', 'gzip, deflate'],
            ('compress', 'gzip', 'deflate'))

    def test_str(self):
        self.assertFieldStrEqual(
            ('compress', 'gzip', 'deflate'),
            'content-encoding: compress, gzip, deflate')


class ContentLanguageTest(FieldTestCase):

    field = fields.ContentLanguage

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['mi, da', 'en'],
            (('mi', (), None, None, (), (), (), None),
             ('da', (), None, None, (), (), (), None),
             ('en', (), None, None, (), (), (), None)))

    def test_str(self):
        self.assertFieldStrEqual(
            (('mi', (), None, None, (), (), (), None),
             ('da', (), None, None, (), (), (), None),
             ('en', (), None, None, (), (), (), None)),
            'content-language: mi, da, en')


class ContentLengthTest(FieldTestCase):

    field = fields.ContentLength

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['3495'],
            (3495,))

    def test_str(self):
        self.assertFieldStrEqual(
            (3495,),
            'content-length: 3495')


class ContentLocationTest(FieldTestCase):

    field = fields.ContentLocation

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['rfc7231.html'],
            ('rfc7231.html',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('rfc7231.html',),
            'content-location: rfc7231.html')


class ContentRangeTest(FieldTestCase):

    field = fields.ContentRange

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['bytes 0-100/100'],
            (('bytes', (0, 100), 100, None),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('bytes', (0, 100), 100, None),),
            'content-range: bytes 0-100/100')


class ContentTypeTest(FieldTestCase):

    field = fields.ContentType

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['text/html; charset=ISO-8859-4'],
            (
                (('text', 'html'),
                 parameters.ParamsCI([
                     ('charset', 'ISO-8859-4')])),))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                (('text', 'html'),
                 parameters.ParamsCI([
                     ('charset', 'ISO-8859-4')])),),
            'content-type: text/html;charset=ISO-8859-4')


class CustomTestCase(unittest.TestCase):

    def test_raw_values(self):
        self.assertEqual(
            fields.Custom(
                name='foo',
                raw_values_collection=['foo, bar', 'baz']).values(),
            ('foo, bar', 'baz'))

    def test_str(self):
        self.assertEqual(
            str(fields.Custom(
                name='foo',
                values=('foo', 'bar', 'baz'))),
            'foo: foo, bar, baz')


class DateTest(FieldTestCase):

    field = fields.Date

    def test_raw_values(self):

        self.assertFieldRawEqual(
            ['Tue, 15 Nov 1994 08:12:31 GMT'],
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=8,
                minute=12,
                second=31),))

    def test_str(self):
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=8,
                minute=12,
                second=31),),
            'date: Tue, 15 Nov 1994 08:12:31 GMT')


class ETagTest(FieldTestCase):

    field = fields.ETag

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['W/"xyzzy"'],
            (('xyzzy', True),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('xyzzy', True),),
            'etag: W/"xyzzy"')


class ExpectTest(FieldTestCase):

    field = fields.Expect

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['100-continue'],
            ('100-continue',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('100-continue',),
            'expect: 100-continue')


class ExpiresTest(FieldTestCase):

    field = fields.Expires

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Thu, 01 Dec 1994 16:00:00 GMT'],
            (datetime.datetime(
                year=1994,
                month=12,
                day=1,
                hour=16,
                minute=0,
                second=0),))

    def test_str(self):
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=12,
                day=1,
                hour=16,
                minute=0,
                second=0),),
            'expires: Thu, 01 Dec 1994 16:00:00 GMT')


class FromTest(FieldTestCase):

    field = fields.From

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['webmaster@example.org'],
            ('webmaster@example.org',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('webmaster@example.org',),
            'from: webmaster@example.org')


class HostTest(FieldTestCase):

    field = fields.Host

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['example.org'],
            (('example.org', None, None, None, None, None),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('example.org', None, None, None, None, None),),
            'host: example.org')


class IfMatchTest(FieldTestCase):

    field = fields.IfMatch

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['"xyzzy", "r2d2xxxx"', '"c3piozzzz"'],
            (
                ('xyzzy', False),
                ('r2d2xxxx', False),
                ('c3piozzzz', False)))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('xyzzy', False),
                ('r2d2xxxx', False),
                ('c3piozzzz', False)),
            'if-match: "xyzzy", "r2d2xxxx", "c3piozzzz"')


class IfModifiedSinceTest(FieldTestCase):

    field = fields.IfModifiedSince

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Sat, 29 Oct 1994 19:43:31 GMT'],
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),))

    def test_str(self):
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),),
            'if-modified-since: Sat, 29 Oct 1994 19:43:31 GMT')


class IfNoneMatchTest(FieldTestCase):

    field = fields.IfNoneMatch

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['W/"xyzzy", "r2d2xxxx"', '"c3piozzzz"'],
            (
                ('xyzzy', True),
                ('r2d2xxxx', False),
                ('c3piozzzz', False)))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('xyzzy', True),
                ('r2d2xxxx', False),
                ('c3piozzzz', False)),
            'if-none-match: W/"xyzzy", "r2d2xxxx", "c3piozzzz"')


class IfRangeTest(FieldTestCase):

    field = fields.IfRange

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['"xyzzy"'],
            (('xyzzy', False),))
        self.assertFieldRawEqual(
            ['Sat, 29 Oct 1994 19:43:31 GMT'],
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('xyzzy', False),),
            'if-range: "xyzzy"')
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),),
            'if-range: Sat, 29 Oct 1994 19:43:31 GMT')


class IfUnmodifiedSinceTest(FieldTestCase):

    field = fields.IfUnmodifiedSince

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Sat, 29 Oct 1994 19:43:31 GMT'],
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),))

    def test_str(self):
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),),
            'if-unmodified-since: Sat, 29 Oct 1994 19:43:31 GMT')


class LastModifiedTest(FieldTestCase):

    field = fields.LastModified

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Tue, 15 Nov 1994 12:45:26 GMT'],
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=12,
                minute=45,
                second=26),))

    def test_str(self):
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=12,
                minute=45,
                second=26),),
            'last-modified: Tue, 15 Nov 1994 12:45:26 GMT')


class LocationTest(FieldTestCase):

    field = fields.Location

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['/People.html#tim'],
            ('/People.html#tim',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('/People.html#tim',),
            'location: /People.html#tim')


class MaxForwardsTest(FieldTestCase):

    field = fields.MaxForwards

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['2'],
            (2,))

    def test_str(self):
        self.assertFieldStrEqual(
            (2,),
            'max-forwards: 2')


class PragmaTest(FieldTestCase):

    field = fields.Pragma

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['no-cache, foo=bar', 'baz=qux'],
            (parameters.ParamsCI([
                ('no-cache', ()),
                ('foo', 'bar'),
                ('baz', 'qux')]),))

    def test_str(self):
        self.assertFieldStrEqual(
            (parameters.ParamsCI([
                ('no-cache', ()),
                ('foo', 'bar'),
                ('baz', 'qux')]),),
            'pragma: no-cache, foo=bar, baz=qux')


class RangeTest(FieldTestCase):

    field = fields.Range

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['bytes=0-499'],
            (parameters.ParamsCI([
                ('bytes', ((0, 499),))]),))

    def test_str(self):
        self.assertFieldStrEqual(
            (parameters.ParamsCI([
                ('bytes', ((0, 499),))]),),
            'range: bytes=0-499')


class RefererTest(FieldTestCase):

    field = fields.Referer

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['/People.html#tim'],
            ('/People.html#tim',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('/People.html#tim',),
            'referer: /People.html#tim')


class RetryAfterTest(FieldTestCase):

    field = fields.RetryAfter

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['10'],
            (10,))
        self.assertFieldRawEqual(
            ['Tue, 15 Nov 1994 12:45:26 GMT'],
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=12,
                minute=45,
                second=26),))

    def test_str(self):
        self.assertFieldStrEqual(
            (10,),
            'retry-after: 10')
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=12,
                minute=45,
                second=26),),
            'retry-after: Tue, 15 Nov 1994 12:45:26 GMT')


class ServerTest(FieldTestCase):

    field = fields.Server

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['CERN/3.0 libwww/2.17 (foo bar) (baz qux)'],
            (('CERN', '3.0', ()), ('libwww', '2.17', ())))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('CERN', '3.0', ()),
                ('libwww', '2.17', ('foo bar', 'baz qux'))),
            'server: CERN/3.0 libwww/2.17 (foo bar) (baz qux)')


class TETest(FieldTestCase):

    field = fields.TE

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['gzip, deflate;q=0.5', 'compress'],
            (
                ('gzip', parameters.ParamsCI([('q', 1)])),
                ('compress', parameters.ParamsCI([('q', 1)])),
                ('deflate', parameters.ParamsCI([('q', 0.5)]))))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('gzip', parameters.ParamsCI([('q', 1)])),
                ('compress', parameters.ParamsCI([('q', 1)])),
                ('deflate', parameters.ParamsCI([('q', 0.5)]))),
            'te: gzip;q=1, compress;q=1, deflate;q=0.5')


class TrailerTest(FieldTestCase):

    field = fields.Trailer

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['CRC32, Content-Length', 'foo'],
            ('crc32', 'content-length', 'foo'))

    def test_str(self):
        self.assertFieldStrEqual(
            ('CRC32', 'Content-Length', 'foo'),
            'trailer: CRC32, Content-Length, foo')


class TransferEncodingTest(FieldTestCase):

    field = fields.TransferEncoding

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['gzip, chunked', 'foobar;bar=qux'],
            (
                ('gzip', parameters.ParamsCI()),
                ('chunked', parameters.ParamsCI()),
                ('foobar', parameters.ParamsCI([('bar', 'qux')]))))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('gzip', parameters.ParamsCI()),
                ('chunked', parameters.ParamsCI()),
                ('foobar', parameters.ParamsCI([('bar', 'qux')]))),
            'transfer-encoding: gzip, chunked, foobar;bar=qux')


class UpgradeTest(FieldTestCase):

    field = fields.Upgrade

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['HTTP/2.0, SHTTP/1.3', 'IRC/6.9, RTA/x11'],
            (
                ('HTTP', '2.0'),
                ('SHTTP', '1.3'),
                ('IRC', '6.9'),
                ('RTA', 'x11')))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('HTTP', '2.0'),
                ('SHTTP', '1.3'),
                ('IRC', '6.9'),
                ('RTA', 'x11')),
            'upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11')


class UserAgentTest(FieldTestCase):

    field = fields.UserAgent

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['CERN-LineMode/2.15 libwww/2.17b3 (foo bar) (baz qux)'],
            (('CERN-LineMode', '2.15', ()), ('libwww', '2.17b3', ())))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                ('CERN-LineMode', '2.15', ()),
                ('libwww', '2.17b3', ('foo bar', 'baz qux'))),
            'user-agent: CERN-LineMode/2.15 libwww/2.17b3 (foo bar) (baz qux)')


class VaryTest(FieldTestCase):

    field = fields.Vary

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['accept-encoding', 'accept-language, foo'],
            ('accept-encoding', 'accept-language', 'foo'))
        self.assertFieldRawEqual(
            ['*'],
            ('*',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('accept-encoding', 'accept-language'),
            'vary: accept-encoding, accept-language')
        self.assertFieldStrEqual(
            ('*',),
            'vary: *')


class ViaTest(FieldTestCase):

    field = fields.Via

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['1.0 fred (middle man), 1.1 p.example.net', '2.0 foo'],
            (
                ('1.0', 'fred', 'middle man'),
                ('1.1', 'p.example.net', None),
                ('2.0', 'foo', None)))

    def test_str(self):
        self.assertFieldStrEqual(
            (('1.0', 'fred', 'middle man'), ('1.1', 'p.example.net', None)),
            'via: 1.0 fred (middle man), 1.1 p.example.net')


class WarningTest(FieldTestCase):

    field = fields.Warning
    date = datetime.datetime(
        year=2012,
        month=8,
        day=25,
        hour=23,
        minute=34,
        second=45)

    def test_raw_values(self):
        self.assertFieldRawEqual(
            [
                '112 - "network down" "Sat, 25 Aug 2012 23:34:45 GMT", 112 - "err"',
                '112 - "foo"'],
            (
                (112, '-', 'network down', self.date),
                (112, '-', 'err', None),
                (112, '-', 'foo', None)))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                (112, '-', 'network down', self.date),
                (112, '-', 'err', None),
                (112, '-', 'foo', None)),
            'warning: 112 - "network down" "Sat, 25 Aug 2012 23:34:45 GMT", '
            '112 - "err", 112 - "foo"')


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
            [
                'SID=31d4d96e407aad42; Path=/; Domain=example.com',
                'SID2=foobar; Path=/foo; Secure; HttpOnly'],
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
