# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class CacheControlTest(utils.FieldTestCase):

    field = hlh.CacheControl

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['no-cache, private', 'max-age=60, foo=bar'],
            (hlh.ParamsCI((
                (hlh.CacheOptions.no_cache, ()),
                (hlh.CacheOptions.private, ()),
                (hlh.CacheOptions.max_age, 60),
                ('foo', 'bar'))),))

        self.assertFieldRawEqual(
            ['max-age="200"'],
            (hlh.ParamsCI((
                (hlh.CacheOptions.max_age, 200),)),))

        self.assertFieldRawEqual(
            ['foo, bar=baz'],
            (hlh.ParamsCI((
                ('foo', ()),
                ('bar', 'baz'))),))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                hlh.ParamsCI((
                    (hlh.CacheOptions.no_cache, ()),
                    (hlh.CacheOptions.private, ()),
                    (hlh.CacheOptions.max_age, 60),
                    ('foo', 'bar'))),),
            'cache-control: no-cache, private, max-age=60, foo=bar')

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
        self.assertRawOK(['max-age=1'])
        self.assertRaisesHeaderError(['foo;'])
        self.assertRaisesHeaderError(['foo='])
        self.assertRaisesHeaderError(['max-age'])
        self.assertRaisesHeaderError(['max-age='])
        self.assertRaisesHeaderError(['no-cache='])
        self.assertRaisesHeaderError(['private='])
        self.assertRaisesHeaderError(['max-age=a'])
        self.assertRaisesHeaderError(['max-age=1.0'])
        self.assertRaisesHeaderError(['max-stale=1.0'])
        self.assertRaisesHeaderError(['min-fresh=1.0'])
        self.assertRaisesHeaderError(['s-maxage=1.0'])
        self.assertRaisesHeaderError(['no-cache=, private='])
        self.assertRaisesHeaderError(['='])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([hlh.ParamsCI([('foo', ())])])
        self.assertOK([hlh.ParamsCI([('no-cache', ('foo',))])])
        self.assertOK([hlh.ParamsCI([('max-age', 1)])])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([('foo', 'bar')])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('foo', None)])])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('no-cache', None)])])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('no-cache', 'foo')])])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('no-cache', ('=',))])])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('max-age', 1.0)])])
        self.assertRaisesInternalError([
            hlh.ParamsCI([('max-age', None)])])
