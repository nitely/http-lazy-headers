# -*- coding: utf-8 -*-

import unittest

from http_lazy_headers import exceptions


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

    def assertRaisesHeaderError(self, raw_values):
        self.assertRaises(exceptions.HeaderError, self.field(
                raw_values_collection=raw_values).values)

    def assertRawOK(self, raw_values):
        self.assertIsInstance(
            self.field(
                raw_values_collection=raw_values).values(),
            tuple)

    def assertRaisesInternalError(self, values):
        self.assertRaises(
            exceptions.InternalError,
            self.field,
            values=values)

    def assertOK(self, values):
        self.assertIsInstance(
            self.field(values=values),
            self.field)
