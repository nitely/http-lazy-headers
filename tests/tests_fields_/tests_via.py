# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ViaTest(utils.FieldTestCase):

    field = hlh.Via

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['1.0 fred (middle man), 1.1 p.example.net', '2.0 foo'],
            (hlh.via(
                version='1.0',
                pseudonym='fred',
                comment='middle man'),
             hlh.via(
                 version='1.1',
                 host=hlh.host('p.example.net')),
             hlh.via(
                 version='2.0',
                 pseudonym='foo')))

        self.assertFieldRawEqual(
            ['foo/1.0 bar'],
            (hlh.via(
                protocol='foo',
                version='1.0',
                pseudonym='bar'),))

        self.assertFieldRawEqual(
            ['1.0 example.org:8080'],
            (hlh.via(
                version='1.0',
                host=hlh.host(
                    domain='example.org',
                    port=8080)),))

        # Empty port
        self.assertFieldRawEqual(
            ['1.0 example.org:'],
            (hlh.via(
                version='1.0',
                host=hlh.host(domain='example.org')),))

        self.assertFieldRawEqual(
            ['1.0 eXaMplE.org'],
            (hlh.via(
                version='1.0',
                host=hlh.host(domain='example.org')),))

        self.assertFieldRawEqual(
            ['1.0 xn--www.alliancefranaise.nu-dbc'],
            (hlh.via(
                version='1.0',
                host=hlh.host(domain='www.alliancefrançaise.nu')),))

        self.assertFieldRawEqual(
            ['1.0 [::1]'],
            (hlh.via(
                version='1.0',
                host=hlh.host(ipv6='::1')),))

        self.assertFieldRawEqual(
            ['1.0 [::1]:8080'],
            (hlh.via(
                version='1.0',
                host=hlh.host(ipv6='::1', port=8080)),))

        self.assertFieldRawEqual(
            ['1.0 [2001:db8:a0b:12f0::1]'],
            (hlh.via(
                version='1.0',
                host=hlh.host(ipv6='2001:db8:a0b:12f0::1')),))

        self.assertFieldRawEqual(
            ['1.0 127.0.0.1'],
            (hlh.via(
                version='1.0',
                host=hlh.host(ipv4='127.0.0.1')),))

        self.assertFieldRawEqual(
            ['1.0 127.0.0.1:8080'],
            (hlh.via(
                version='1.0',
                host=hlh.host(ipv4='127.0.0.1', port=8080)),))

        self.assertFieldRawEqual(
            ['1.0 [v0.01:77:00:00:00:01]'],
            (hlh.via(
                version='1.0',
                host=hlh.host(ipv_future='v0.01:77:00:00:00:01')),))

        self.assertFieldRawEqual(
            ['1.0 [v0.01:77:00:00:00:01]:8080'],
            (hlh.via(
                version='1.0',
                host=hlh.host(
                    ipv_future='v0.01:77:00:00:00:01',
                    port=8080)),))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.via(
                version='1.0',
                pseudonym='fred',
                comment='middle man'),
             hlh.via(
                 version='1.1',
                 host=hlh.host('p.example.net'))),
            'via: 1.0 fred (middle man), 1.1 p.example.net')

        self.assertFieldStrEqual(
            (hlh.via(
                protocol='foo',
                version='1.0',
                pseudonym='fred'),),
            'via: foo/1.0 fred')

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
