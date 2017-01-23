# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AgeTest(utils.FieldTestCase):

    field = hlh.Age

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['60'],
            (60,))

    def test_str(self):
        self.assertFieldStrEqual(
            (60,),
            'age: 60')

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
        self.assertRawOK(['60'])
        self.assertRawOK(['1' * 10])
        self.assertRaisesHeaderError(['1' * 11])
        self.assertRaisesHeaderError(['60,60'])
        self.assertRaisesHeaderError(['60 60'])
        self.assertRaisesHeaderError(['60;60'])
        self.assertRaisesHeaderError(['60.60'])
        self.assertRaisesHeaderError(['60', '60'])
        self.assertRaisesHeaderError(['foo'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([60])
        self.assertRaisesInternalError([59.9])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([';'])
        self.assertRaisesInternalError(['('])
        self.assertRaisesInternalError([None])
