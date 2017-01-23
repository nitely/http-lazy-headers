# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ContentLocationTest(utils.FieldTestCase):

    field = hlh.ContentLocation

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['/rfc7231.html'],
            ('/rfc7231.html',))

        self.assertFieldRawEqual(
            ['http://example.com/rfc7231.html'],
            ('http://example.com/rfc7231.html',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('/rfc7231.html',),
            'content-location: /rfc7231.html')

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
        self.assertRawOK(['/rfc7231.html'])
        self.assertRaisesHeaderError(['^'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK(['/rfc7231.html'])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['^'])
        self.assertRaisesInternalError([None])
