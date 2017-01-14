# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class IfMatchTest(utils.FieldTestCase):

    field = hlh.IfMatch

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['"xyzzy", "r2d2xxxx"', '"c3piozzzz"'],
            (('xyzzy', False),
             ('r2d2xxxx', False),
             ('c3piozzzz', False)))

    def test_str(self):
        self.assertFieldStrEqual(
            (('xyzzy', False),
             ('r2d2xxxx', False),
             ('c3piozzzz', False)),
            'if-match: "xyzzy", "r2d2xxxx", "c3piozzzz"')

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
        self.assertRaisesHeaderError(['xyzzy'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_match = ('xyzzy', False)
        self.assertOK([good_match])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([('"', False)])
        self.assertRaisesInternalError([(None, False)])
        self.assertRaisesInternalError([('xyzzy', None)])
