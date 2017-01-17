# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class TrailerTest(utils.FieldTestCase):

    field = hlh.Trailer

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['CRC32, Content-Length', 'foo'],
            ('crc32', hlh.ContentLength.name, 'foo'))

        self.assertFieldRawEqual(
            ['foo'],
            ('foo',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('CRC32', hlh.ContentLength.name, 'foo'),
            'trailer: CRC32, content-length, foo')

        self.assertFieldStrEqual(
            ('foo',),
            'trailer: foo')

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
        self.assertRaisesHeaderError(['foo bar'])
        self.assertRaisesHeaderError(['foo;'])
        self.assertRaisesHeaderError(['^='])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_trailer = 'foo'
        self.assertOK([good_trailer])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError(['^='])
        self.assertRaisesInternalError(['foo bar'])
        self.assertRaisesInternalError(['foo', '^='])
