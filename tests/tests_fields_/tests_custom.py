# -*- coding: utf-8 -*-

import functools

import http_lazy_headers as hlh

from . import utils


class CustomTestCase(utils.FieldTestCase):

    field = functools.partial(hlh.Custom, name='foo')

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['foo, bar', 'baz'],
            ('foo, bar', 'baz'))

    def test_str(self):
        self.assertFieldStrEqual(
            ('foo', 'bar', 'baz'),
            'foo: foo, bar, baz')

    def test_raw_empty(self):
        """
        Should allow empty raw value
        """
        self.assertRawOK([''])

    def test_empty(self):
        """
        Should allow empty value
        """
        self.field(values=())

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.field(values=['foo'])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError(['á'])
