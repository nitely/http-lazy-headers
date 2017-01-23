# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AllowTest(utils.FieldTestCase):

    field = hlh.Allow

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['GET, POST', 'PATCH'],
            (hlh.Methods.get,
             hlh.Methods.post,
             hlh.Methods.patch))

    def test_str(self):
        self.assertFieldStrEqual(
            (hlh.Methods.head,
             hlh.Methods.get,
             hlh.Methods.put,
             hlh.Methods.post,
             hlh.Methods.delete,
             hlh.Methods.options,
             hlh.Methods.trace,
             hlh.Methods.connect,
             hlh.Methods.patch,
             'fooBar'),
            'allow: HEAD, GET, PUT, POST, '
            'DELETE, OPTIONS, TRACE, CONNECT, '
            'PATCH, fooBar')

    def test_raw_empty(self):
        """
        Should allow empty raw value
        """
        self.assertFieldRawEqual(
            [''],
            ())

    def test_empty(self):
        """
        Should allow empty value
        """
        self.assertFieldStrEqual(
            (),
            'allow: ')

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK([hlh.Methods.get])
        self.assertRaisesHeaderError([';'])
        self.assertRaisesHeaderError(['GET;'])
        self.assertRaisesHeaderError(['GET='])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([hlh.Methods.get])
        self.assertRaisesInternalError([','])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([';'])
        self.assertRaisesInternalError(['('])
        self.assertRaisesInternalError([None])
