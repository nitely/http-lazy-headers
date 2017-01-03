# -*- coding: utf-8 -*-

import unittest


class FieldTestCase(unittest.TestCase):

    field = None

    def assertFieldRawEqual(self, raw_values, expected):
        self.assertEqual(
            self.field(
                raw_values_collection=raw_values).values(),
            expected)

    def assertFieldStrEqual(self, values, expected):
        self.assertEqual(
            str(self.field(values=values)),
            expected)
