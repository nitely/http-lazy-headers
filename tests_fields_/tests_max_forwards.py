# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class MaxForwardsTest(utils.FieldTestCase):

    field = hlh.MaxForwards

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['2'],
            (2,))

    def test_str(self):
        self.assertFieldStrEqual(
            (2,),
            'max-forwards: 2')

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
        self.assertRawOK(['2'])
        self.assertRaisesHeaderError(['a'])
        self.assertRaisesHeaderError(['2, 2'])
        self.assertRaisesHeaderError(['2' * 100])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([2])
        self.assertRaisesInternalError([2.0])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['^'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([2, 2])
