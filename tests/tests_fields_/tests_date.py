# -*- coding: utf-8 -*-

import datetime

import http_lazy_headers as hlh

from . import utils


class DateTest(utils.FieldTestCase):

    field = hlh.Date

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['Tue, 15 Nov 1994 08:12:31 GMT'],
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=8,
                minute=12,
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

    def test_str(self):
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=8,
                minute=12,
                second=31),),
            'date: Tue, 15 Nov 1994 08:12:31 GMT')

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
        self.assertRawOK(['Tue, 15 Nov 1994 08:12:31 GMT'])
        self.assertRaisesHeaderError(['Tue, 15 Nov'])
        self.assertRaisesHeaderError(['Sun, 15 Nov 1994 08:12:31 GMT'])
        self.assertRaisesHeaderError(['Tue, 15 Nov 1994 08:12:31 UTC'])
        self.assertRaisesHeaderError(['Tue, 15 Nov 1 08:12:31 UTC'])

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
