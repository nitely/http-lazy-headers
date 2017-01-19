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
