# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AcceptTest(utils.FieldTestCase):

    field = hlh.Accept

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['text/html, foo/bar;baz=qux', '*/*;q=0.5'],
            ((('foo', 'bar'),
              hlh.ParamsCI([
                  ('baz', 'qux'),
                  (hlh.Attributes.q, 1)])),
             ((hlh.MediaType.text, hlh.MediaType.html),
              hlh.ParamsCI([(hlh.Attributes.q, 1)])),
             ((hlh.MediaType.star, hlh.MediaType.star),
              hlh.ParamsCI([(hlh.Attributes.q, 0.5)]))))

        self.assertFieldRawEqual(
            ["audio/*; q=0.2, audio/basic"],
            (((hlh.MediaType.audio, 'basic'),
              hlh.ParamsCI(((hlh.Attributes.q, 1),))),
             ((hlh.MediaType.audio, hlh.MediaType.star),
              hlh.ParamsCI(((hlh.Attributes.q, 0.2),)))))

        self.assertFieldRawEqual(
            ["text/plain; q=0.5, text/html, text/x-dvi; q=0.8, text/x-c"],
            (((hlh.MediaType.text, hlh.MediaType.html),
              hlh.ParamsCI(((hlh.Attributes.q, 1),))),
             ((hlh.MediaType.text, 'x-c'),
              hlh.ParamsCI(((hlh.Attributes.q, 1),))),
             ((hlh.MediaType.text, 'x-dvi'),
              hlh.ParamsCI(((hlh.Attributes.q, 0.8),))),
             ((hlh.MediaType.text, hlh.MediaType.plain),
              hlh.ParamsCI(((hlh.Attributes.q, 0.5),)))))

        self.assertFieldRawEqual(
            ["text/plain; charset=utf-8"],
            (((hlh.MediaType.text, hlh.MediaType.plain),
              hlh.ParamsCI((
                  (hlh.Attributes.charset, hlh.Charsets.utf_8.lower()),
                  (hlh.Attributes.q, 1)))),))

        self.assertFieldRawEqual(
            ["text/plain; charset=utf-8; q=0.5"],
            (((hlh.MediaType.text, hlh.MediaType.plain),
              hlh.ParamsCI((
                  (hlh.Attributes.charset, hlh.Charsets.utf_8.lower()),
                  (hlh.Attributes.q, 0.5)))),))

    def test_str(self):
        self.assertFieldStrEqual(
            (
                (('foo', 'bar'), hlh.ParamsCI([('baz', 'qux')])),
                (('*', '*'), hlh.ParamsCI([('q', 0.5)]))),
            'accept: foo/bar;baz=qux, */*;q=0.5')
