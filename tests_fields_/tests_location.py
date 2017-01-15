# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class LocationTest(utils.FieldTestCase):

    field = hlh.Location

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['/People.html#tim'],
            ('/People.html#tim',))

    def test_str(self):
        self.assertFieldStrEqual(
            ('/People.html#tim',),
            'location: /People.html#tim')

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
        self.assertRawOK(['/People.html#tim'])
        self.assertRaisesHeaderError(['^'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK(['/People.html#tim'])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['^'])
        self.assertRaisesInternalError([None])
