# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class AcceptLanguageTest(utils.FieldTestCase):

    field = hlh.AcceptLanguage

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['da, en-gb;q=0.8', 'en;q=0.7'],
            ((('da', (), None, None, (), (), (), None), 1),
             (('en', (), None, 'gb', (), (), (), None), 0.8),
             (('en', (), None, None, (), (), (), None), 0.7)))

        self.assertFieldRawEqual(
            ['en-US, en; q=0.5, fr'],
            ((('en', (), None, 'us', (), (), (), None), 1),
             (('fr', (), None, None, (), (), (), None), 1),
             (('en', (), None, None, (), (), (), None), 0.5)))

    def test_str(self):
        self.assertFieldStrEqual(
            ((('da', (), None, None, (), (), (), None), None),
             (('en', (), None, 'gb', (), (), (), None), 0.8),
             (('en', (), None, None, (), (), (), None), 0.7)),
            'accept-language: da, en-gb; q=0.8, en; q=0.7')

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

    def test_raw_bad_with_param(self):
        """
        Should not allow empty value and non-empty params
        """
        self.assertRaisesHeaderError(['q=1'])

    def test_raw_bad_values(self):
        """
        Should not allow bad raw values
        """
        self.assertRawOK(['en-US'])
        self.assertRawOK(['en-US;q=1'])
        self.assertRaisesHeaderError([';'])
        self.assertRaisesHeaderError([';=;;q=0'])
        self.assertRaisesHeaderError(['en-US;'])
        self.assertRaisesHeaderError(['en-US;q'])
        self.assertRaisesHeaderError(['en-US;q='])
        self.assertRaisesHeaderError(['en-US;q=1.1'])
        self.assertRaisesHeaderError(['en-US;q=a'])
        self.assertRaisesHeaderError(['en-US;bad=1'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        good_language = ('en', (), None, 'us', (), (), (), None)
        self.assertOK([(good_language, None)])
        self.assertOK([(good_language, 1)])
        self.assertOK([(good_language, 0.5)])
        self.assertRaisesInternalError([('', 1)])
        self.assertRaisesInternalError([(good_language, '')])
        self.assertRaisesInternalError([(good_language, 'a')])
        self.assertRaisesInternalError([(good_language, 5)])
        self.assertRaisesInternalError([
            (good_language, good_language, good_language)])
        self.assertRaisesInternalError([(None, 5)])
        self.assertRaisesInternalError([(None, None)])
        self.assertRaisesInternalError([
            ((None, (), None, None, (), (), (), None), 1)])
        self.assertRaisesInternalError([
            (('', (), None, None, (), (), (), None), 1)])
        self.assertRaisesInternalError([
            (('es', (), None, None, (), (), (), 'i-klingon'), 1)])
