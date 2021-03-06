# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class TETest(utils.FieldTestCase):

    field = hlh.TE

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['gzip, deflate;q=0.5', 'compress'],
            ((hlh.Encodings.gzip, hlh.ParamsCI()),
             (hlh.Encodings.compress, hlh.ParamsCI()),
             (hlh.Encodings.deflate, hlh.ParamsCI([
                 (hlh.Attributes.q, 0.5)]))))

        self.assertFieldRawEqual(
            ['GziP'],
            ((hlh.Encodings.gzip, hlh.ParamsCI()),))

        self.assertFieldRawEqual(
            ['foo'],
            (('foo', hlh.ParamsCI()),))

        self.assertFieldRawEqual(
            ['trailers'],
            (('trailers', hlh.ParamsCI()),))

        # Transfer-extension (not "trailers")
        self.assertFieldRawEqual(
            ['trailers;q=1'],
            (('trailers', hlh.ParamsCI([
                (hlh.Attributes.q, 1)])),))

    def test_str(self):
        self.assertFieldStrEqual(
            ((hlh.Encodings.gzip, hlh.ParamsCI()),
             (hlh.Encodings.compress, hlh.ParamsCI([
                 (hlh.Attributes.q, 1)])),
             (hlh.Encodings.deflate, hlh.ParamsCI([
                 (hlh.Attributes.q, 0.5)]))),
            'te: gzip, compress; q=1, deflate; q=0.5')

        self.assertFieldStrEqual(
            (('trailers', hlh.ParamsCI()),),
            'te: trailers')

        # Transfer-extension (not "trailers")
        self.assertFieldStrEqual(
            (('trailers', hlh.ParamsCI([
                (hlh.Attributes.q, 1)])),),
            'te: trailers; q=1')

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
            'te: ')

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['gzip'])
        self.assertRaisesHeaderError(['=^'])
        self.assertRaisesHeaderError(['gzip;'])
        self.assertRaisesHeaderError(['gzip;q='])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_te = ('gzip', hlh.ParamsCI())
        self.assertOK([good_te])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([(1, hlh.ParamsCI())])
        self.assertRaisesInternalError([(None, hlh.ParamsCI())])
        self.assertRaisesInternalError([('', hlh.ParamsCI())])
        self.assertRaisesInternalError([('gzip', None)])
