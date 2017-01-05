# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AcceptRangesTest(utils.FieldTestCase):

    field = hlh.AcceptRanges

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['bytes'],
            (hlh.RangesOptions.bytes,))

        self.assertFieldRawEqual(
            ['none'],
            (hlh.RangesOptions.none,))

        self.assertFieldRawEqual(
            ['unknown-unit'],
            ('unknown-unit',))

        self.assertFieldRawEqual(
            ['bytes, unknown-unit'],
            (hlh.RangesOptions.bytes, 'unknown-unit'))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.RangesOptions.bytes,),
            'accept-ranges: bytes')

        self.assertFieldStrEqual(
            (hlh.RangesOptions.bytes, 'unknown-unit'),
            'accept-ranges: bytes, unknown-unit')

    def test_raw_empty(self):
        """
        Should NOT allow empty raw value
        """
        self.assertRaisesHeaderError([''])

    def test_empty(self):
        """
        Should allow empty value
        """
        self.assertRaisesInternalError(())

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['bytes'])
        self.assertRaisesHeaderError([';'])
        self.assertRaisesHeaderError(['bytes;'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK(['bytes'])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([';'])
        self.assertRaisesInternalError(['('])
        self.assertRaisesInternalError([None])
