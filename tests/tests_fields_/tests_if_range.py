# -*- coding: utf-8 -*-

import datetime

import http_lazy_headers as hlh

from . import utils


class IfRangeTest(utils.FieldTestCase):

    field = hlh.IfRange

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['"xyzzy"'],
            (('xyzzy', False),))

        self.assertFieldRawEqual(
            ['Sat, 29 Oct 1994 19:43:31 GMT'],
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),))

        self.assertFieldRawEqual(
            ['Sunday, 06-Nov-94 08:49:37 GMT'],
            (datetime.datetime(
                year=1994,
                month=11,
                day=6,
                hour=8,
                minute=49,
                second=37),))

        self.assertFieldRawEqual(
            ['Sun Nov  6 08:49:37 1994'],
            (datetime.datetime(
                year=1994,
                month=11,
                day=6,
                hour=8,
                minute=49,
                second=37),))

        self.assertFieldRawEqual(
            ['bad-date'],
            (datetime.datetime.max,))

    def test_str(self):
        self.assertFieldStrEqual(
            (('xyzzy', False),),
            'if-range: "xyzzy"')

        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=10,
                day=29,
                hour=19,
                minute=43,
                second=31),),
            'if-range: Sat, 29 Oct 1994 19:43:31 GMT')

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
        self.assertRawOK(['"xyzzy"'])

        # Weak e-tag not allowed, treat it as a bad date
        self.assertFieldRawEqual(
            ['W/"xyzzy"'],
            (datetime.datetime.max,))

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_date = datetime.datetime(
            year=1994,
            month=11,
            day=15,
            hour=8,
            minute=12,
            second=31)
        good_etag = ('xyzzy', False)
        self.assertOK([good_date])
        self.assertOK([good_etag])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([good_date, good_date])
        self.assertRaisesInternalError([good_etag, good_etag])
        self.assertRaisesInternalError([('xyzzy', True)])
        self.assertRaisesInternalError([('xyzzy', None)])
        self.assertRaisesInternalError([(1, False)])
        self.assertRaisesInternalError([(None, False)])
