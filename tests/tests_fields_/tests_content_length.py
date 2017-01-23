# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ContentLengthTest(utils.FieldTestCase):

    field = hlh.ContentLength

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['3495'],
            (3495,))

        self.assertFieldRawEqual(
            ['3495, 3495, 3495, 3495'],
            (3495,))

    def test_str(self):
        self.assertFieldStrEqual(
            (3495,),
            'content-length: 3495')

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
        self.assertRawOK(['3495'])
        self.assertRaisesHeaderError(['3495;'])
        self.assertRaisesHeaderError(['='])
        self.assertRaisesHeaderError(['('])
        self.assertRaisesHeaderError(['3495.10'])
        self.assertRaisesHeaderError(['1, 2'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([3495])
        self.assertRaisesInternalError([1, 2, 3])
        self.assertRaisesInternalError(['1'])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([';'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([3495.10])
