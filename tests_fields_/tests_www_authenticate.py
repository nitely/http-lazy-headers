# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class WWWAuthenticateTest(utils.FieldTestCase):

    field = hlh.WWWAuthenticate

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Newauth realm="apps", type=1, '
             'title="Login to \\"apps\\"", '
             'Basic realm="simple"',
             'Foo asdqwe=='],
            (('newauth', None, hlh.ParamsCI([
                ('realm', 'apps'),
                ('type', '1'),
                ('title', 'Login to "apps"')])),
             ('basic', None, hlh.ParamsCI([
                 ('realm', 'simple')])),
             ('foo', 'asdqwe==', hlh.ParamsCI())))

        self.assertFieldRawEqual(
            ['foo'],
            (('foo', None, hlh.ParamsCI()),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('newauth', None, hlh.ParamsCI([
                ('realm', 'apps'),
                ('type', '1'),
                ('title', 'Login to "apps"')])),
             ('basic', None, hlh.ParamsCI([
                 ('realm', 'simple')])),
             ('foo', 'asdqwe==', hlh.ParamsCI())),
            'www-authenticate: newauth realm=apps, '
            'type=1, title="Login to \\"apps\\"", '
            'basic realm=simple, foo asdqwe==')

        self.assertFieldStrEqual(
            (('foo', None, hlh.ParamsCI()),),
            'www-authenticate: foo')

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
        self.assertRawOK(['foo asdqwe=='])
        self.assertRawOK(['basic realm=simple'])
        self.assertRawOK(['foo'])
        self.assertRaisesHeaderError(['foo ^='])
        self.assertRaisesHeaderError(['^='])
        self.assertRaisesHeaderError(['foo=bar'])
        self.assertRaisesHeaderError(['foo asdqwe==, bar=baz'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_auth = ('foo', None, hlh.ParamsCI())
        self.assertOK([good_auth])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            ('', None, hlh.ParamsCI())])
        self.assertRaisesInternalError([
            (None, None, hlh.ParamsCI())])
        self.assertRaisesInternalError([
            ('foo', 'asdqwe==', hlh.ParamsCI([('realm', 'simple')]))])
        self.assertRaisesInternalError([
            ('foo', None, None)])
        self.assertRaisesInternalError([
            ('foo', 1, None)])
        self.assertRaisesInternalError([
            ('foo', '^=', hlh.ParamsCI())])
        self.assertRaisesInternalError([
            ('^=', None, hlh.ParamsCI())])
