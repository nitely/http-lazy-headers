# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AcceptTest(utils.FieldTestCase):

    field = hlh.Accept

    def test_raw_values(self):
        """
        Should parse raw mimes and params
        """
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
        """
        Should format pyObj mimes and params
        """
        self.assertFieldStrEqual(
            ((('foo', 'bar'),
              hlh.ParamsCI([('baz', 'qux')])),
             ((hlh.MediaType.star, hlh.MediaType.star),
              hlh.ParamsCI([(hlh.Attributes.q, 0.5)]))),
            'accept: foo/bar; baz=qux, */*; q=0.5')

        self.assertFieldStrEqual(
            (((hlh.MediaType.text, hlh.MediaType.plain),
              hlh.ParamsCI((
                  (hlh.Attributes.charset, hlh.Charsets.utf_8.lower()),
                  (hlh.Attributes.q, 0.5)))),),
            'accept: text/plain; charset=utf-8; q=0.5')

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
            'accept: ')

    def test_raw_bad_with_param(self):
        """
        Should not allow empty value and non-empty params
        """
        self.assertRaisesHeaderError(['q=1'])

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['text/plain'])
        self.assertRawOK(['text/plain;q=0'])
        self.assertRaisesHeaderError(['text'])
        self.assertRaisesHeaderError([';/;'])
        self.assertRaisesHeaderError(['/'])
        self.assertRaisesHeaderError(['text/;'])
        self.assertRaisesHeaderError([';/plain'])
        self.assertRaisesHeaderError(['text/plain;'])
        self.assertRaisesHeaderError(['text/plain;='])
        self.assertRaisesHeaderError(['text/plain;q='])
        self.assertRaisesHeaderError(['text/plain;q'])
        self.assertRaisesHeaderError(['text/plain;q=a'])
        self.assertRaisesHeaderError(['text/plain;q=5'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([(('text', 'plain'), hlh.ParamsCI())])
        self.assertOK([(('text', 'plain'), hlh.ParamsCI([('q', 1)]))])
        self.assertRaisesInternalError([(('text', ''), hlh.ParamsCI())])
        self.assertRaisesInternalError([(('', 'plain'), hlh.ParamsCI())])
        self.assertRaisesInternalError([(('', ''), hlh.ParamsCI())])
        self.assertRaisesInternalError([((';', ';'), hlh.ParamsCI())])
        self.assertRaisesInternalError([(('text', ';'), hlh.ParamsCI())])
        self.assertRaisesInternalError([((';', 'plain'), hlh.ParamsCI())])
        self.assertRaisesInternalError([(
            ('text', 'plain'),
            hlh.ParamsCI([('', '')]))])
        self.assertRaisesInternalError([(
            ('text', 'plain'),
            hlh.ParamsCI([('q', 'a')]))])
        self.assertRaisesInternalError([(
            ('text', 'plain'),
            hlh.ParamsCI([('q', '5')]))])
