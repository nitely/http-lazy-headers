# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class HostTest(utils.FieldTestCase):

    field = hlh.Host

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['example.org'],
            (hlh.host(domain='example.org'),))

        self.assertFieldRawEqual(
            ['example.org:8080'],
            (hlh.host(domain='example.org', port=8080),))

        # Empty port
        self.assertFieldRawEqual(
            ['example.org:'],
            (hlh.host(domain='example.org'),))

        self.assertFieldRawEqual(
            ['eXaMplE.org'],
            (hlh.host(domain='example.org'),))

        self.assertFieldRawEqual(
            ['xn--www.alliancefranaise.nu-dbc'],
            (hlh.host(domain='www.alliancefrançaise.nu'),))

        self.assertFieldRawEqual(
            ['[::1]'],
            (hlh.host(ipv6='::1'),))

        self.assertFieldRawEqual(
            ['[::1]:8080'],
            (hlh.host(ipv6='::1', port=8080),))

        self.assertFieldRawEqual(
            ['[2001:db8:a0b:12f0::1]'],
            (hlh.host(ipv6='2001:db8:a0b:12f0::1'),))

        self.assertFieldRawEqual(
            ['127.0.0.1'],
            (hlh.host(ipv4='127.0.0.1'),))

        self.assertFieldRawEqual(
            ['127.0.0.1:8080'],
            (hlh.host(ipv4='127.0.0.1', port=8080),))

        self.assertFieldRawEqual(
            ['[v0.01:77:00:00:00:01]'],
            (hlh.host(ipv_future='v0.01:77:00:00:00:01'),))

        self.assertFieldRawEqual(
            ['[v0.01:77:00:00:00:01]:8080'],
            (hlh.host(ipv_future='v0.01:77:00:00:00:01', port=8080),))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.host(domain='example.org'),),
            'host: example.org')

        self.assertFieldStrEqual(
            (hlh.host(domain='example.org', port=8080),),
            'host: example.org:8080')

        self.assertFieldStrEqual(
            (hlh.host(domain='www.Alliancefrançaise.nu'),),
            'host: xn--www.alliancefranaise.nu-dbc')

        self.assertFieldStrEqual(
            (hlh.host(domain='xn--www.Alliancefranaise.nu-dbc'),),
            'host: xn--www.Alliancefranaise.nu-dbc')

        self.assertFieldStrEqual(
            (hlh.host(ipv6='::1'),),
            'host: [::1]')

        self.assertFieldStrEqual(
            (hlh.host(ipv6='::1', port=8080),),
            'host: [::1]:8080')

        self.assertFieldStrEqual(
            (hlh.host(ipv4='127.0.0.1'),),
            'host: 127.0.0.1')

        self.assertFieldStrEqual(
            (hlh.host(ipv4='127.0.0.1', port=8080),),
            'host: 127.0.0.1:8080')

        self.assertFieldStrEqual(
            (hlh.host(ipv_future='v0.01:77:00:00:00:01'),),
            'host: [v0.01:77:00:00:00:01]')

        self.assertFieldStrEqual(
            (hlh.host(ipv_future='v0.01:77:00:00:00:01', port=8080),),
            'host: [v0.01:77:00:00:00:01]:8080')

    @hlh.override_settings(HOST_UNSAFE_ALLOW=True)
    def test_raw_unsafe_hostname(self):
        """
        Should parse an unsafe host
        """
        self.assertFieldRawEqual(
            ['foo'],
            (hlh.host(unsafe='foo'),))

        self.assertFieldRawEqual(
            ['foo:8080'],
            (hlh.host(unsafe='foo', port=8080),))

        self.assertFieldRawEqual(
            ['FoO'],
            (hlh.host(unsafe='foo'),))

    @hlh.override_settings(HOST_UNSAFE_ALLOW=False)
    def test_unsafe_hostname(self):
        """
        Should allow unsafe even if it's not\
        allowed for the parser
        """
        self.assertFieldStrEqual(
            (hlh.host(unsafe='foo'),),
            'host: foo')

        self.assertFieldStrEqual(
            (hlh.host(unsafe='foo', port=8080),),
            'host: foo:8080')

        self.assertFieldStrEqual(
            (hlh.host(unsafe='FoO'),),
            'host: FoO')

    def test_raw_empty(self):
        """
        Should allow empty raw value
        """
        self.assertFieldRawEqual(
            [''],
            (hlh.host(),))

    def test_empty(self):
        """
        Should allow empty value
        """
        self.assertFieldStrEqual(
            (hlh.host(),),
            'host: ')

    @hlh.override_settings(HOST_UNSAFE_ALLOW=False)
    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['example.org'])
        self.assertRaisesHeaderError(['^'])
        self.assertRaisesHeaderError(['foo'])
        self.assertRaisesHeaderError(['example.org:aaaa'])
        self.assertRaisesHeaderError(['example.org:123:123'])
        self.assertRaisesHeaderError(['foo:123'])

    @hlh.override_settings(HOST_UNSAFE_ALLOW=True)
    def test_raw_bad_unsafe_values(self):
        """
        Should not allow bad raw unsafe values
        """
        self.assertRawOK(['foo'])
        self.assertRaisesHeaderError(['^='])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_hostname = hlh.host(domain='example.org')
        self.assertOK([good_hostname])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['^'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            good_hostname, good_hostname])
        self.assertRaisesInternalError([
            ('foo', None, None, None, None, None)])
        self.assertRaisesInternalError([
            ('example.org', None, None, None, None, '123')])
        self.assertRaisesInternalError([
            ('example.org', None, None, None, None, '')])
        self.assertRaisesInternalError([
            ('example.org', '127.0.0.1', None, None, None, None)])
        self.assertRaisesInternalError([
            ('example.org', '127.0.0.1', None, None, None, 8080)])
