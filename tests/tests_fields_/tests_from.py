# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class FromTest(utils.FieldTestCase):

    field = hlh.From

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['webmaster@example.org'],
            ('webmaster@example.org',))

        self.assertFieldRawEqual(
            ['<webmaster@example.org>'],
            ('<webmaster@example.org>',))

        self.assertFieldRawEqual(
            ['John <webmaster@example.org>'],
            ('John <webmaster@example.org>',))

        self.assertFieldRawEqual(
            ['"John Doe" <webmaster@example.org>'],
            ('"John Doe" <webmaster@example.org>',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('webmaster@example.org',),
            'from: webmaster@example.org')

        self.assertFieldStrEqual(
            ('<webmaster@example.org>',),
            'from: <webmaster@example.org>')

        self.assertFieldStrEqual(
            ('John <webmaster@example.org>',),
            'from: John <webmaster@example.org>')

        self.assertFieldStrEqual(
            ('"John Doe" <webmaster@example.org>',),
            'from: "John Doe" <webmaster@example.org>')

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
        good_from = 'webmaster@example.org'
        self.assertRawOK([good_from])
        self.assertRaisesHeaderError([good_from, good_from])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_from = 'webmaster@example.org'
        self.assertOK([good_from])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['á'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([good_from, good_from])
