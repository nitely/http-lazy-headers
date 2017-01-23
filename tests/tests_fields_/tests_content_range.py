# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ContentRangeTest(utils.FieldTestCase):

    field = hlh.ContentRange

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['bytes 0-100/100'],
            ((hlh.RangesOptions.bytes, (0, 100), 100, None),))

        self.assertFieldRawEqual(
            ['bytes 0-499/500'],
            ((hlh.RangesOptions.bytes, (0, 499), 500, None),))

        # Undefined length
        self.assertFieldRawEqual(
            ['bytes 0-499/*'],
            ((hlh.RangesOptions.bytes, (0, 499), None, None),))

        # Undefined/unsatisfied range
        self.assertFieldRawEqual(
            ['bytes */500'],
            ((hlh.RangesOptions.bytes, None, 500, None),))

        self.assertFieldRawEqual(
            ['bytes */*'],
            ((hlh.RangesOptions.bytes, None, None, None),))

        self.assertFieldRawEqual(
            ['bytes -/*'],
            ((hlh.RangesOptions.bytes, (None, None), None, None),))

        self.assertFieldRawEqual(
            ['bytes 0-/*'],
            ((hlh.RangesOptions.bytes, (0, None), None, None),))

        self.assertFieldRawEqual(
            ['bytes -1/*'],
            ((hlh.RangesOptions.bytes, (None, 1), None, None),))

        self.assertFieldRawEqual(
            ['none'],
            ((None, None, None, None),))

        self.assertFieldRawEqual(
            ['seconds 1-2'],
            (('seconds', None, None, '1-2'),))

    def test_str(self):
        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, (0, 100), 100, None),),
            'content-range: bytes 0-100/100')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, (0, 499), 500, None),),
            'content-range: bytes 0-499/500')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, (0, 499), None, None),),
            'content-range: bytes 0-499/*')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, None, 500, None),),
            'content-range: bytes */500')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, None, None, None),),
            'content-range: bytes */*')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, (None, None), None, None),),
            'content-range: bytes -/*')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, (0, None), None, None),),
            'content-range: bytes 0-/*')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, (None, 1), None, None),),
            'content-range: bytes -1/*')

        self.assertFieldStrEqual(
            ((None, None, None, None),),
            'content-range: none')

        self.assertFieldStrEqual(
            (('seconds', None, None, '1-2'),),
            'content-range: seconds 1-2')

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
        self.assertRawOK(['bytes 0-499/500'])
        self.assertRaisesHeaderError(['bytes 0-499'])
        self.assertRaisesHeaderError(['bytes'])
        self.assertRaisesHeaderError(['bytes 499-0/500'])
        self.assertRaisesHeaderError(['bytes 1-2/500/600'])
        self.assertRaisesHeaderError(['bytes 1-2-3/500'])
        self.assertRaisesHeaderError([
            'bytes 0-499/500', 'bytes 0-499/500'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([(hlh.RangesOptions.bytes, (0, 100), 100, None)])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            ('foo', None, 100, None)])
        self.assertRaisesInternalError([
            ('foo', (0, 100), None, None)])
        self.assertRaisesInternalError([
            (hlh.RangesOptions.bytes, None, None, 'foo')])
