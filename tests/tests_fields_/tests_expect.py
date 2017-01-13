# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ExpectTest(utils.FieldTestCase):

    field = hlh.Expect

    def test_raw_values(self):
        self.assertFieldRawEqual(
            [hlh.expect_continue()],
            ('100-continue',))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.expect_continue(),),
            'expect: 100-continue')

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
        self.assertRawOK([hlh.expect_continue()])
        self.assertRaisesHeaderError([hlh.expect_continue().upper()])
        self.assertRaisesHeaderError(['foo'])
        self.assertRaisesHeaderError([
            hlh.expect_continue(), hlh.expect_continue()])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([hlh.expect_continue()])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['^'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            hlh.expect_continue(), hlh.expect_continue()])
        self.assertRaisesInternalError([hlh.expect_continue().upper()])
