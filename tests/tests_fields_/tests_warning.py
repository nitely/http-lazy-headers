# -*- coding: utf-8 -*-

import datetime

import http_lazy_headers as hlh

from . import utils


class WarningTest(utils.FieldTestCase):

    field = hlh.Warning
    date = datetime.datetime(
        year=2012,
        month=8,
        day=25,
        hour=23,
        minute=34,
        second=45)

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['112 - "network down" "Sat, 25 Aug '
             '2012 23:34:45 GMT", 112 - "err"',
             '112 - "foo"'],
            ((112, (hlh.host(), '-'), 'network down', self.date),
             (112, (hlh.host(), '-'), 'err', None),
             (112, (hlh.host(), '-'), 'foo', None)))

        self.assertFieldRawEqual(
            ['112 - ""'],
            ((112, (hlh.host(), '-'), '', None),))

        self.assertFieldRawEqual(
            ['112 example.org "foo"'],
            ((112,
              (hlh.host(domain='example.org'), None),
              'foo',
              None),))

    def test_str(self):
        self.assertFieldStrEqual(
            ((112, (hlh.host(), '-'), 'network down', self.date),
             (112, (hlh.host(), '-'), 'err', None),
             (112, (hlh.host(), '-'), 'foo', None)),
            'warning: 112 - "network down" '
            '"Sat, 25 Aug 2012 23:34:45 GMT", '
            '112 - "err", 112 - "foo"')

        self.assertFieldStrEqual(
            ((112,
              (hlh.host(domain='example.org'), None),
              'network down',
              None),),
            'warning: 112 example.org "network down"')

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
        self.assertRawOK(['112 - "foo"'])
        self.assertRawOK([
            '112 - "foo" "Sat, 25 Aug 2012 23:34:45 GMT"'])
        self.assertRaisesHeaderError(['321 - "foo"'])
        self.assertRaisesHeaderError(['112 - '])
        self.assertRaisesHeaderError(['112 "foo"'])
        self.assertRaisesHeaderError(['112 "-" "foo"'])
        self.assertRaisesHeaderError(['112 - foo'])
        self.assertRaisesHeaderError(['foo - foo'])
        self.assertRaisesHeaderError([
            '112 - "foo" Sat, 25 Aug 2012 23:34:45 GMT'])
        self.assertRaisesHeaderError([
            '112 - "foo" "Mon, 25 Aug 2012 23:34:45 GMT"'])
        self.assertRaisesHeaderError([
            '112 - "foo" "bar"'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_warning = (
            112, (hlh.host(), '-'), 'network down', self.date)
        self.assertOK([good_warning])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            ('foo', (hlh.host(), '-'), 'network down', self.date)])
        self.assertRaisesInternalError([
            (None, (hlh.host(), '-'), 'network down', self.date)])
        self.assertRaisesInternalError([
            (112, None, 'network down', self.date)])
        self.assertRaisesInternalError([
            (112, (hlh.host(), '^='), 'network down', self.date)])
        self.assertRaisesInternalError([
            (112,
             (hlh.host(domain='example.org'), '-'),
             'network down',
             self.date)])
        self.assertRaisesInternalError([
            (112, (hlh.host(domain='^='), None), 'network down', self.date)])
        self.assertRaisesInternalError([
            (112, (hlh.host(), '-'), '', self.date)])
        self.assertRaisesInternalError([
            (112, (hlh.host(), '-'), None, self.date)])
        self.assertRaisesInternalError([
            (112, (hlh.host(), '-'), None, 'foo')])
