# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ETagTest(utils.FieldTestCase):

    field = hlh.ETag

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['W/"xyzzy"'],
            (('xyzzy', True),))

        self.assertFieldRawEqual(
            ['"xyzzy"'],
            (('xyzzy', False),))

        self.assertFieldRawEqual(
            ['""'],
            (('', False),))

        self.assertFieldRawEqual(
            ['W/""'],
            (('', True),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('xyzzy', True),),
            'etag: W/"xyzzy"')

        self.assertFieldStrEqual(
            (('xyzzy', False),),
            'etag: "xyzzy"')

        self.assertFieldStrEqual(
            (('', True),),
            'etag: W/""')

        self.assertFieldStrEqual(
            (('', False),),
            'etag: ""')

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
        self.assertRaisesHeaderError(['"xyzzy", "xyzzy"'])

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
        self.assertRaisesInternalError([good_etag, good_etag])
        self.assertRaisesInternalError([('xyzzy', None)])
        self.assertRaisesInternalError([(1, False)])
        self.assertRaisesInternalError([(None, False)])
