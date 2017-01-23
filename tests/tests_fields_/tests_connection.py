# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ConnectionTest(utils.FieldTestCase):

    field = hlh.Connection

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['keep-alive, upgrade', 'foo'],
            (hlh.ConnectionOptions.keep_alive,
             hlh.ConnectionOptions.upgrade,
             'foo'))

        self.assertFieldRawEqual(
            ['kEEp-aLIVe'],
            (hlh.ConnectionOptions.keep_alive,))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.ConnectionOptions.keep_alive,
             hlh.ConnectionOptions.upgrade,
             'foo'),
            'connection: keep-alive, upgrade, foo')

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
        self.assertRawOK(['upgrade'])
        self.assertRaisesHeaderError(['upgrade;'])
        self.assertRaisesHeaderError(['='])
        self.assertRaisesHeaderError(['('])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK(['upgrade'])
        self.assertOK(['foo'])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([';'])
        self.assertRaisesInternalError(['('])
        self.assertRaisesInternalError([None])
