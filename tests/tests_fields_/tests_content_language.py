# -*- coding: utf-8 -*-

import http_lazy_headers as hlh

from . import utils


class ContentLanguageTest(utils.FieldTestCase):

    field = hlh.ContentLanguage

    def test_raw_values(self):
        self.assertFieldRawEqual(
            ['mi, da', 'en'],
            (('mi', (), None, None, (), (), (), None),
             ('da', (), None, None, (), (), (), None),
             ('en', (), None, None, (), (), (), None)))

        self.assertFieldRawEqual(
            ['en'],
            (('en', (), None, None, (), (), (), None),))

        self.assertFieldRawEqual(
            ['EN'],
            (('en', (), None, None, (), (), (), None),))

    def test_str(self):
        self.assertFieldStrEqual(
            (('mi', (), None, None, (), (), (), None),
             ('da', (), None, None, (), (), (), None),
             ('en', (), None, None, (), (), (), None)),
            'content-language: mi, da, en')

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
        self.assertRawOK(['en-US'])
        self.assertRaisesHeaderError([';'])
        self.assertRaisesHeaderError([';=;;q=0'])
        self.assertRaisesHeaderError(['en-US;'])

    def test_bad_values(self):
        """
        Should not allow bad values
        """
        self.assertOK([
            ('en', (), None, 'us', (), (), (), None)])
        self.assertOK([
            (None, (), None, None, (), (), (), 'i-klingon')])
        self.assertRaisesInternalError([''])
        self.assertRaisesInternalError([None])
        self.assertRaisesInternalError([
            (None, (), None, None, (), (), (), None)])
        self.assertRaisesInternalError([
            ('', (), None, None, (), (), (), None)])
        self.assertRaisesInternalError([
            ('es', (), None, None, (), (), (), 'i-klingon')])
