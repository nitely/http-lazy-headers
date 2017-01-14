# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class HostTest(utils.FieldTestCase):

    field = hlh.Host

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['example.org'],
            (('example.org', None, None, None, None, None),))

        self.assertFieldRawEqual(
            ['example.org:8080'],
            (('example.org', None, None, None, None, 8080),))

        # Empty port
        self.assertFieldRawEqual(
            ['example.org:'],
            (('example.org', None, None, None, None, None),))

        self.assertFieldRawEqual(
            ['eXaMplE.org'],
            (('example.org', None, None, None, None, None),))

        self.assertFieldRawEqual(
            ['xn--www.alliancefranaise.nu-dbc'],
            (('www.alliancefrançaise.nu', None, None, None, None, None),))

        self.assertFieldRawEqual(
            ['[::1]'],
            ((None, None, '::1', None, None, None),))

        self.assertFieldRawEqual(
            ['[::1]:8080'],
            ((None, None, '::1', None, None, 8080),))

        self.assertFieldRawEqual(
            ['[2001:db8:a0b:12f0::1]'],
            ((None, None, '2001:db8:a0b:12f0::1', None, None, None),))

        self.assertFieldRawEqual(
            ['127.0.0.1'],
            ((None, '127.0.0.1', None, None, None, None),))

        self.assertFieldRawEqual(
            ['127.0.0.1:8080'],
            ((None, '127.0.0.1', None, None, None, 8080),))

        self.assertFieldRawEqual(
            ['127.0.0.1:8080'],
            ((None, '127.0.0.1', None, None, None, 8080),))

        self.assertFieldRawEqual(
            ['[v0.01:77:00:00:00:01]'],
            ((None, None, None, 'v0.01:77:00:00:00:01', None, None),))

        self.assertFieldRawEqual(
            ['[v0.01:77:00:00:00:01]:8080'],
            ((None, None, None, 'v0.01:77:00:00:00:01', None, 8080),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('example.org', None, None, None, None, None),),
            'host: example.org')

        self.assertFieldStrEqual(
            (('example.org', None, None, None, None, 8080),),
            'host: example.org:8080')

        self.assertFieldStrEqual(
            (('www.Alliancefrançaise.nu', None, None, None, None, None),),
            'host: xn--www.alliancefranaise.nu-dbc')

        self.assertFieldStrEqual(
            (('xn--www.Alliancefranaise.nu-dbc', None, None, None, None, None),),
            'host: xn--www.Alliancefranaise.nu-dbc')

        self.assertFieldStrEqual(
            ((None, None, '::1', None, None, None),),
            'host: [::1]')

        self.assertFieldStrEqual(
            ((None, None, '::1', None, None, 8080),),
            'host: [::1]:8080')

        self.assertFieldStrEqual(
            ((None, '127.0.0.1', None, None, None, None),),
            'host: 127.0.0.1')

        self.assertFieldStrEqual(
            ((None, '127.0.0.1', None, None, None, 8080),),
            'host: 127.0.0.1:8080')

        self.assertFieldStrEqual(
            ((None, None, None, 'v0.01:77:00:00:00:01', None, None),),
            'host: [v0.01:77:00:00:00:01]')

        self.assertFieldStrEqual(
            ((None, None, None, 'v0.01:77:00:00:00:01', None, 8080),),
            'host: [v0.01:77:00:00:00:01]:8080')

    @hlh.override_settings(HOST_UNSAFE_ALLOW=True)
    def test_raw_unsafe_hostname(self):
        """
        Should parse an unsafe host
        """
        self.assertFieldRawEqual(
            ['foo'],
            ((None, None, None, None, 'foo', None),))

        self.assertFieldRawEqual(
            ['foo:8080'],
            ((None, None, None, None, 'foo', 8080),))

        self.assertFieldRawEqual(
            ['FoO'],
            ((None, None, None, None, 'foo', None),))

    @hlh.override_settings(HOST_UNSAFE_ALLOW=False)
    def test_unsafe_hostname(self):
        """
        Should allow unsafe even if it's not\
        allowed for the parser
        """
        self.assertFieldStrEqual(
            ((None, None, None, None, 'foo', None),),
            'host: foo')

        self.assertFieldStrEqual(
            ((None, None, None, None, 'foo', 8080),),
            'host: foo:8080')

        self.assertFieldStrEqual(
            ((None, None, None, None, 'FoO', None),),
            'host: FoO')

    def test_raw_empty(self):
        """
        Should allow empty raw value
        """
        self.assertFieldRawEqual(
            [''],
            ((None, None, None, None, None, None),))

    def test_empty(self):
        """
        Should allow empty value
        """
        self.assertFieldStrEqual(
            ((None, None, None, None, None, None),),
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
        good_hostname = ('example.org', None, None, None, None, None)
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
