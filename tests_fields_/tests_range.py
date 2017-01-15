# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class RangeTest(utils.FieldTestCase):

    field = hlh.Range

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['bytes=0-499'],
            ((hlh.RangesOptions.bytes, ((0, 499),)),))

        self.assertFieldRawEqual(
            ['bytes=-500'],
            ((hlh.RangesOptions.bytes, ((None, 500),)),))

        self.assertFieldRawEqual(
            ['bytes=9500-'],
            ((hlh.RangesOptions.bytes, ((9500, None),)),))

        self.assertFieldRawEqual(
            ['bytes=0-0,-1'],
            ((hlh.RangesOptions.bytes, ((0, 0), (None, 1))),))

        self.assertFieldRawEqual(
            ['bytes=500-600,601-999'],
            ((hlh.RangesOptions.bytes, ((500, 600), (601, 999))),))

        self.assertFieldRawEqual(
            ['bytes=500-700,601-999'],
            ((hlh.RangesOptions.bytes, ((500, 700), (601, 999))),))

        self.assertFieldRawEqual(
            ['bytes=1-100,200-'],
            ((hlh.RangesOptions.bytes, ((1, 100), (200, None))),))

        self.assertFieldRawEqual(
            ['foo=1-100'],
            (('foo', '1-100'),))

    def test_str(self):
        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, ((0, 499),)),),
            'range: bytes=0-499')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, ((None, 500),)),),
            'range: bytes=-500')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, ((9500, None),)),),
            'range: bytes=9500-')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, ((0, 0), (None, 1))),),
            'range: bytes=0-0,-1')

        self.assertFieldStrEqual(
            ((hlh.RangesOptions.bytes, ((1, 100), (200, None))),),
            'range: bytes=1-100,200-')

        self.assertFieldStrEqual(
            (('foo', '1-100'),),
            'range: foo=1-100')

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
        self.assertRawOK(['bytes=0-499'])
        self.assertRaisesHeaderError(['bytes=-'])
        self.assertRaisesHeaderError(['bytes=0-499,'])
        self.assertRaisesHeaderError(['bytes=1-100,,101-200'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_range = (
            hlh.RangesOptions.bytes,
            ((1, 100), (200, None)))
        self.assertOK([good_range])
        self.assertOK([('foo', 'bar')])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([good_range, good_range])
        self.assertRaisesInternalError([
            (hlh.RangesOptions.bytes,
             ((None, None),))])
        self.assertRaisesInternalError([
            (hlh.RangesOptions.bytes,
             ((1, 100, 200),))])
        self.assertRaisesInternalError([
            (hlh.RangesOptions.bytes,
             (('1', '2'),))])
        self.assertRaisesInternalError([('foo', 'á')])
        self.assertRaisesInternalError([('^=', 'bar')])
