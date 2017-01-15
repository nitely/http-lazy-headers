# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class IfNoneMatchTest(utils.FieldTestCase):

    field = hlh.IfNoneMatch

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['W/"xyzzy", "r2d2xxxx"', '"c3piozzzz"'],
            (('xyzzy', True),
             ('r2d2xxxx', False),
             ('c3piozzzz', False)))

        self.assertFieldRawEqual(
            ['""'],
            (('', False),))

        self.assertFieldRawEqual(
            ['W/""'],
            (('', True),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('xyzzy', True),
             ('r2d2xxxx', False),
             ('c3piozzzz', False)),
            'if-none-match: W/"xyzzy", "r2d2xxxx", "c3piozzzz"')

        self.assertFieldStrEqual(
            (('', True),),
            'if-none-match: W/""')

        self.assertFieldStrEqual(
            (('', False),),
            'if-none-match: ""')

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
        self.assertRaisesHeaderError(['w/"xyzzy"'])
        self.assertRaisesHeaderError(['w/""'])
        self.assertRaisesHeaderError(['xyzzy'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_etag = ('xyzzy', False)
        self.assertOK([good_etag])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['^'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([('xyzzy', None)])
        self.assertRaisesInternalError([(1, False)])
        self.assertRaisesInternalError([(None, False)])
