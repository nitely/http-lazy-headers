# -*- coding: utf-8 -*-

import datetime

import http_lazy_headers as hlh

from . import utils


class RetryAfterTest(utils.FieldTestCase):

    field = hlh.RetryAfter

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['10'],
            (10,))
        self.assertFieldRawEqual(
            ['Tue, 15 Nov 1994 12:45:26 GMT'],
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=12,
                minute=45,
                second=26),))

    def test_str(self):
        self.assertFieldStrEqual(
            (10,),
            'retry-after: 10')
        self.assertFieldStrEqual(
            (datetime.datetime(
                year=1994,
                month=11,
                day=15,
                hour=12,
                minute=45,
                second=26),),
            'retry-after: Tue, 15 Nov 1994 12:45:26 GMT')
