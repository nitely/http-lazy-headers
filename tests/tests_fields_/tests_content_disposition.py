# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ContentDispositionTest(utils.FieldTestCase):

    field = hlh.ContentDisposition

    def test_raw_values(self):
        # Test from: http://greenbytes.de/tech/tc2231/#c-d-inline

        self.assertFieldRawEqual(
            ['attachment; filename="EURO rates"; '
             'filename*=utf-8\'en\'%e2%82%ac%20rates'],
            (('attachment', hlh.ParamsCI([
                ('filename', 'EURO rates'),
                ('filename*', ('utf-8', 'en', '€ rates'))])),))

        self.assertFieldRawEqual(
            ['Attachment; filename=example.html'],
            (('attachment', hlh.ParamsCI([
                ('filename', 'example.html')])),))

        #self.assertFieldRawEqual(
        #    ['INLINE; FILENAME= "an example.html"'],
        #    (('inline', hlh.ParamsCI([
        #        ('filename', 'an example.html')])),))

        self.assertFieldRawEqual(
            ['attachment'],
            (('attachment', hlh.ParamsCI([])),))

        self.assertFieldRawEqual(
            ['attachment; filename="\"quoting\" tested.html"'],
            (('attachment', hlh.ParamsCI([
                ('filename', '"quoting" tested.html')])),))

        self.assertFieldRawEqual(
            ['attachment; filename="Here\'s a semicolon;.html"'],
            (('attachment', hlh.ParamsCI([
                ('filename', 'Here\'s a semicolon;.html')])),))

        self.assertFieldRawEqual(
            ['attachment; foo="bar"; filename="foo.html"'],
            (('attachment', hlh.ParamsCI([
                ('foo', 'bar'),
                ('filename', 'foo.html')])),))

        self.assertFieldRawEqual(
            ['attachment; FILENAME="foo.html"'],
            (('attachment', hlh.ParamsCI([
                ('filename', 'foo.html')])),))

        self.assertFieldRawEqual(
            ['attachment; FILENAME="foo.html"'],
            (('attachment', hlh.ParamsCI([
                ('filename', 'foo.html')])),))

        self.assertFieldRawEqual(
            ['attachment; filename="foo-%41.html"'],
            (('attachment', hlh.ParamsCI([
                ('filename', 'foo-%41.html')])),))

        self.assertFieldRawEqual(
            ['attachment; filename="50%.html"'],
            (('attachment', hlh.ParamsCI([
                ('filename', '50%.html')])),))

        self.assertFieldRawEqual(
            ['attachment; filename*=iso-8859-1\'\'foo-%E4.html'],
            (('attachment', hlh.ParamsCI([
                ('filename*', ('iso-8859-1', None, 'foo-ä.html'))])),))

        self.assertFieldRawEqual(
            ['attachment; filename*=UTF-8\'\'A-%2541.html'],
            (('attachment', hlh.ParamsCI([
                ('filename*', ('UTF-8', None, 'A-%41.html'))])),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename', 'EURO rates'),
                ('filename*', ('utf-8', 'en', '€ rates'))])),),
            'content-disposition: attachment;'
            'filename="EURO rates";'
            'filename*=utf-8\'en\'%E2%82%AC%20rates')

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
        self.assertRawOK([
            'attachment; filename="EURO rates"; '
            'filename*=utf-8\'en\'%e2%82%ac%20rates'])
        self.assertRaisesHeaderError(['attachment; filename="/foo.html"'])
        self.assertRaisesHeaderError(['attachment; filename="\\foo.html"'])
        self.assertRaisesHeaderError([
            'attachment; filename*=UTF-8\'\'%5cfoo.html'])  # \foo
        self.assertRaisesHeaderError([
            'attachment; filename*=\'\'foo-%c3%a4-%e2%82%ac.html'])
