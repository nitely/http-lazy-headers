# -*- coding: utf-8 -*-

import datetime

import http_lazy_headers as hlh

from . import utils


class ExpiresTest(utils.FieldTestCase):

    field = hlh.Expires

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Thu, 01 Dec 1994 16:00:00 GMT'],
            (datetime.datetime(
                year=1994,
                month=12,
                day=1,
                hour=16,
                minute=0,
                second=0),))

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
            ['0'],
            (datetime.datetime.min,))

        self.assertFieldRawEqual(
            ['bad value'],
            (datetime.datetime.min,))

    def test_str(self):
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=12,
                day=1,
                hour=16,
                minute=0,
                second=0),),
            'expires: Thu, 01 Dec 1994 16:00:00 GMT')

        self.assertFieldStrEqual(
            (0,),
            'expires: 0')

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
        self.assertOK([good_date])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([good_date, good_date])
