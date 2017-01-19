# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class VaryTest(utils.FieldTestCase):

    field = hlh.Vary

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['accept-encoding', 'accept-language, foo'],
            ('accept-encoding', 'accept-language', 'foo'))

        self.assertFieldRawEqual(
            ['*'],
            ('*',))

        self.assertFieldRawEqual(
            ['FoO'],
            ('foo',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('accept-encoding', 'accept-language'),
            'vary: accept-encoding, accept-language')

        self.assertFieldStrEqual(
            ('*',),
            'vary: *')

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
        self.assertRaisesHeaderError(['^='])
        self.assertRaisesHeaderError(['foo bar'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_vary = 'foo'
        self.assertOK([good_vary])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError(['^='])
