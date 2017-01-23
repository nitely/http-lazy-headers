# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ServerTest(utils.FieldTestCase):

    field = hlh.Server

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['CERN/3.0 libwww/2.17 (foo bar) (baz qux)'],
            (('CERN', '3.0', ()), ('libwww', '2.17', ())))

        self.assertFieldRawEqual(
            ['CERN/3.0 libwww/2.17'],
            (('CERN', '3.0', ()), ('libwww', '2.17', ())))

        self.assertFieldRawEqual(
            ['CERN libwww/2.17'],
            (('CERN', None, ()), ('libwww', '2.17', ())))

        self.assertFieldRawEqual(
            ['CERN'],
            (('CERN', None, ()),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('CERN', '3.0', ()),
             ('libwww', '2.17', ('foo bar', 'baz qux'))),
            'server: CERN/3.0 libwww/2.17 (foo bar) (baz qux)')

        self.assertFieldStrEqual(
            (('CERN', None, ()),),
            'server: CERN')

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
        self.assertRawOK(['CERN/3.0 libwww/2.17'])
        self.assertRaisesHeaderError(['CERN/^='])
        self.assertRaisesHeaderError(['^=/3.0'])
        self.assertRaisesHeaderError(['^='])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_lib = ('CERN', '3.0', ())
        self.assertOK([good_lib])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([(1, None, ())])
        self.assertRaisesInternalError([(None, None, ())])
        self.assertRaisesInternalError([('', None, ())])
        self.assertRaisesInternalError([('CERN',)])
        self.assertRaisesInternalError([('CERN', None)])
        self.assertRaisesInternalError([('^=', '3.0', ())])
        self.assertRaisesInternalError([('CERN', '^=', ())])
