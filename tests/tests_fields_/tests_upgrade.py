# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class UpgradeTest(utils.FieldTestCase):

    field = hlh.Upgrade

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['HTTP/2.0, SHTTP/1.3', 'IRC/6.9, RTA/x11'],
            ((hlh.ProtocolOptions.http, '2.0'),
             ('SHTTP', '1.3'),
             ('IRC', '6.9'),
             ('RTA', 'x11')))

        self.assertFieldRawEqual(
            ['HTTP'],
            ((hlh.ProtocolOptions.http, None),))

    def test_str(self):
        self.assertFieldStrEqual(
            ((hlh.ProtocolOptions.http, '2.0'),
             ('SHTTP', '1.3'),
             ('IRC', '6.9'),
             ('RTA', 'x11')),
            'upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11')

        self.assertFieldStrEqual(
            ((hlh.ProtocolOptions.http, None),),
            'upgrade: HTTP')

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
        self.assertRawOK(['HTTP'])
        self.assertRaisesHeaderError(['^='])
        self.assertRaisesHeaderError(['HTTP/^='])
        self.assertRaisesHeaderError(['^=/2.0'])
        self.assertRaisesHeaderError(['/2.0'])
        self.assertRaisesHeaderError(['HTTP/'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_proto = (hlh.ProtocolOptions.http, None)
        self.assertOK([good_proto])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([(None, '2.0')])
        self.assertRaisesInternalError([(hlh.ProtocolOptions.http, '')])
        self.assertRaisesInternalError([(None, None)])
        self.assertRaisesInternalError([(hlh.ProtocolOptions.http, 1)])
