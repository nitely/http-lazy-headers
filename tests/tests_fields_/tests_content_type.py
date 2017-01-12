# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ContentTypeTest(utils.FieldTestCase):

    field = hlh.ContentType

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['text/html; charset=ISO-8859-4'],
            (((hlh.MediaType.text, hlh.MediaType.html),
              hlh.ParamsCI([
                  (hlh.Attributes.charset, hlh.Charsets.iso_8859_4)])),))

    def test_str(self):
        self.assertFieldStrEqual(
            (((hlh.MediaType.text, hlh.MediaType.html),
              hlh.ParamsCI([
                  (hlh.Attributes.charset, hlh.Charsets.iso_8859_4)])),),
            'content-type: text/html; charset=ISO-8859-4')

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
        self.assertRawOK(['text/html; charset=ISO-8859-4'])
        self.assertRaisesHeaderError(['^'])
        self.assertRaisesHeaderError([';charset=utf-8'])
        self.assertRaisesHeaderError(['text/html;charset='])
        self.assertRaisesHeaderError(['/html;charset=utf-8'])
        self.assertRaisesHeaderError(['text/;charset=utf-8'])
        self.assertRaisesHeaderError(['text/html;'])
        self.assertRaisesHeaderError(['/'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([
            ((hlh.MediaType.text, hlh.MediaType.html),
             hlh.ParamsCI([
                 (hlh.Attributes.charset, hlh.Charsets.iso_8859_4)]))])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError(['^'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            ((hlh.MediaType.text, hlh.MediaType.html), None)])
        self.assertRaisesInternalError([
            (None, hlh.ParamsCI())])
        self.assertRaisesInternalError([
            ((';', ';'), hlh.ParamsCI())])
        self.assertRaisesInternalError([
            ((1, 1), hlh.ParamsCI())])
        self.assertRaisesInternalError([
            ((None, None), hlh.ParamsCI())])
