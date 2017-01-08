# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AuthorizationTest(utils.FieldTestCase):

    field = hlh.Authorization

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Bearer foo'],
            (('bearer', 'foo', hlh.ParamsCI()),))

        self.assertFieldRawEqual(
            ['Bearer token68=='],
            (('bearer', 'token68==', hlh.ParamsCI()),))

        self.assertFieldRawEqual(
            ['foo'],
            (('foo', None, hlh.ParamsCI()),))

        self.assertFieldRawEqual(
            ['foo foo=bar, baz=qux, foobar="foo bar"'],
            (('foo', None, hlh.ParamsCI([
                ('foo', 'bar'),
                ('baz', 'qux'),
                ('foobar', 'foo bar')])),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('bearer', 'foo', hlh.ParamsCI()),),
            'authorization: bearer foo')

        self.assertFieldStrEqual(
            (('foo', None, hlh.ParamsCI()),),
            'authorization: foo')

        self.assertFieldStrEqual(
            (('foo', 'token68==', hlh.ParamsCI()),),
            'authorization: foo token68==')

        self.assertFieldStrEqual(
            (('foo', None, hlh.ParamsCI([
                ('foo', 'bar'),
                ('baz', 'qux'),
                ('foobar', 'foo bar')])),),
            'authorization: foo foo=bar, baz=qux, foobar="foo bar"')

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
        self.assertRawOK(['foo token68=='])
        self.assertRawOK(['foo foo=bar, baz=qux'])
        self.assertRaisesHeaderError(['foo;'])
        self.assertRaisesHeaderError(['foo tok;en68=='])
        self.assertRaisesHeaderError(['foo token68== foo=bar'])
        self.assertRaisesHeaderError(['foo token68==, foo=bar'])
        self.assertRaisesHeaderError(['foo foo=ba;r, baz=q;ux'])
        self.assertRaisesHeaderError(['foo ,'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([('foo', None, hlh.ParamsCI())])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([';'])
        self.assertRaisesInternalError(['('])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([('', None, hlh.ParamsCI())])
        self.assertRaisesInternalError([(';', None, hlh.ParamsCI())])
        self.assertRaisesInternalError([(';', None, None)])
        self.assertRaisesInternalError([
            ('foo', 'token68==', hlh.ParamsCI([('foo', 'bar')]))])
        self.assertRaisesInternalError([
            ('', 'token68==', hlh.ParamsCI())])
        self.assertRaisesInternalError([
            ('foo', None, hlh.ParamsCI()),
            ('bar', None, hlh.ParamsCI())])
