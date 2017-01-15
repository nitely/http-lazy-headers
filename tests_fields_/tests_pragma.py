# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class PragmaTest(utils.FieldTestCase):

    field = hlh.Pragma

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['no-cache, foo=bar', 'baz=qux'],
            (hlh.ParamsCI([
                (hlh.CacheOptions.no_cache, ()),
                ('foo', 'bar'),
                ('baz', 'qux')]),))

        self.assertFieldRawEqual(
            ['fOoBaR'],
            (hlh.ParamsCI([
                ('foobar', ())]),))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.ParamsCI([
                (hlh.CacheOptions.no_cache, ()),
                ('foo', 'bar'),
                ('baz', 'qux')]),),
            'pragma: no-cache, foo=bar, baz=qux')

        self.assertFieldStrEqual(
            (hlh.ParamsCI([
                (hlh.CacheOptions.no_cache, ())]),),
            'pragma: no-cache')

        self.assertFieldStrEqual(
            (hlh.ParamsCI([
                ('fOoBaR', ())]),),
            'pragma: foobar')

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
        self.assertRawOK(['foo=1'])
        self.assertRaisesHeaderError(['foo;'])
        self.assertRaisesHeaderError(['foo='])
        self.assertRaisesHeaderError(['no-cache='])
        self.assertRaisesHeaderError(['='])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([hlh.ParamsCI([('foo', ())])])
        self.assertOK([hlh.ParamsCI([('no-cache', 'foo, bar')])])
        self.assertRaisesInternalError('foo')
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([('foo', 'bar')])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('no-cache', ('a', 'b'))])])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('foo', 1.0)])])
