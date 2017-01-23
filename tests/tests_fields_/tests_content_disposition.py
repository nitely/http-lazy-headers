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

        self.assertFieldRawEqual(
            ['attachment'],
            (('attachment', hlh.ParamsCI([])),))

        self.assertFieldRawEqual(
            ['attachment; filename="\\\"quoting\\\" tested.html"'],
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

        self.assertFieldRawEqual(
            ['attachment; filename*=iso-8859-1\'\'foo-%c3%a4-%e2%82%ac.html'],
            (('attachment', hlh.ParamsCI([
                ('filename*', ('iso-8859-1', None, 'foo-Ã¤-â\x82¬.html'))])),))

        self.assertFieldRawEqual(
            ['attachment; filename*=utf-8\'\'foo-%E4.html'],
            (('attachment', hlh.ParamsCI([
                ('filename*', ('utf-8', None, 'foo-�.html'))])),))

        # todo: fixme, should raise
        self.assertFieldRawEqual(
            ['attachment; filename*="UTF-8\'\'foo-%c3%a4.html"'],
            (('attachment', hlh.ParamsCI([
                ('filename*', ('UTF-8', None, 'foo-ä.html'))])),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename', 'EURO rates'),
                ('filename*', ('utf-8', 'en', '€ rates'))])),),
            'content-disposition: attachment; '
            'filename="EURO rates"; '
            'filename*=utf-8\'en\'%E2%82%AC%20rates')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename', 'example.html')])),),
            'content-disposition: attachment; filename=example.html')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([])),),
            'content-disposition: attachment')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename', '"quoting" tested.html')])),),
            'content-disposition: attachment; filename="\\\"quoting\\\" tested.html"')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename', 'Here\'s a semicolon;.html')])),),
            'content-disposition: attachment; filename="Here\'s a semicolon;.html"')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('foo', 'bar'),
                ('filename', 'foo.html')])),),
            'content-disposition: attachment; foo=bar; filename=foo.html')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename', 'foo-%41.html')])),),
            'content-disposition: attachment; filename=foo-%41.html')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename', 'foo-50%.html')])),),
            'content-disposition: attachment; filename=foo-50%.html')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename*', ('iso-8859-1', None, 'foo-ä.html'))])),),
            'content-disposition: attachment; filename*=iso-8859-1\'\'foo-%E4.html')

        self.assertFieldStrEqual(
            (('attachment', hlh.ParamsCI([
                ('filename*', ('UTF-8', None, 'A-%41.html'))])),),
            'content-disposition: attachment; filename*=UTF-8\'\'A-%2541.html')

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
        self.assertRaisesHeaderError(['"inline"'])
        self.assertRaisesHeaderError(['attachment; filename=foo,bar.html'])
        self.assertRaisesHeaderError(['attachment; filename=foo.html ;'])
        self.assertRaisesHeaderError(['attachment; ;filename=foo'])
        self.assertRaisesHeaderError(['attachment; ;filename=foo'])
        self.assertRaisesHeaderError(['attachment; filename=foo bar.html'])
        self.assertRaisesHeaderError(['attachment; filename=foo[1](2).html'])
        self.assertRaisesHeaderError(['attachment; filename=foo-ä.html'])
        self.assertRaisesHeaderError(['attachment; filename=foo-Ã¤.html'])
        self.assertRaisesHeaderError(['filename=foo.html'])
        self.assertRaisesHeaderError(['x=y; filename=foo.html'])
        self.assertRaisesHeaderError(['"foo; filename=bar;baz"; filename=qux'])
        self.assertRaisesHeaderError(['filename=foo.html, filename=bar.html'])
        self.assertRaisesHeaderError(['; filename=foo.html'])
        self.assertRaisesHeaderError([': inline; attachment; filename=foo.html'])
        self.assertRaisesHeaderError(['attachment; inline; filename=foo.html'])
        self.assertRaisesHeaderError(['attachment; filename="foo.html".txt'])
        self.assertRaisesHeaderError(['attachment; filename="bar'])
        self.assertRaisesHeaderError(['attachment; filename=foo"bar;baz"qux'])
        self.assertRaisesHeaderError([
            'attachment; filename=foo.html, attachment; filename=bar.html'])
        self.assertRaisesHeaderError(['attachment; foo=foo filename=bar'])
        self.assertRaisesHeaderError(['attachment; filename=bar foo=foo '])
        self.assertRaisesHeaderError(['attachment filename=bar'])
        self.assertRaisesHeaderError(['filename=foo.html; attachment'])
        self.assertRaisesHeaderError([
            'attachment; filename *=UTF-8\'\'foo-%c3%a4.html'])
        self.assertRaisesHeaderError([
            'attachment; filename*="foo%20bar.html"'])
        self.assertRaisesHeaderError([
            'attachment; filename*=UTF-8\'foo-%c3%a4.html'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_disposition = ('attachment', hlh.ParamsCI([
            ('filename', 'example.html')]))
        self.assertOK([good_disposition])
        self.assertRaisesInternalError([1])
        self.assertRaisesInternalError(['foo'])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            good_disposition, good_disposition])
        self.assertRaisesInternalError([
            ('', hlh.ParamsCI([
                ('filename', 'example.html')]))])
        self.assertRaisesInternalError([
            ('^=', hlh.ParamsCI([
                ('filename', 'example.html')]))])
        self.assertRaisesInternalError([
            ('foo=bar', hlh.ParamsCI([
                ('filename', 'example.html')]))])
        self.assertRaisesInternalError([
            (None, hlh.ParamsCI([
                ('filename', 'example.html')]))])
        self.assertRaisesInternalError([
            (1, hlh.ParamsCI([
                ('filename', 'example.html')]))])
        self.assertRaisesInternalError([
            ('attachment', None)])
        self.assertRaisesInternalError([
            ('attachment', 'foo')])
