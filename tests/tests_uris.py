# -*- coding: utf-8 -*-

import unittest

from http_lazy_headers.shared.common import uris


class URITestCase(unittest.TestCase):

    def test_absolute_uri(self):
        # http://example.org/
        # http://example.org?
        # http://example.org#
        # http://example.org:80, http://example.org:
        # http://user:@example.org
        # http://user:pass@example.org
        pass

    def test_rel_uri(self):
        # ./this:that, a path-noscheme uri
        pass

    def test_remove_dot_segments(self):
        """
        Should remove dot segments from paths
        """
        self.assertEqual(
            uris.remove_dot_segments('/a/b/c/./../../g'),
            '/a/g')
        self.assertEqual(
            uris.remove_dot_segments('mid/content=5/../6'),
            'mid/6')

        self.assertEqual(
            uris.remove_dot_segments('../'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('./'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('/./'),
            '/')
        self.assertEqual(
            uris.remove_dot_segments('/.'),
            '/')
        self.assertEqual(
            uris.remove_dot_segments('/../'),
            '/')
        self.assertEqual(
            uris.remove_dot_segments('/..'),
            '/')
        self.assertEqual(
            uris.remove_dot_segments('.'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('..'),
            '')

        self.assertEqual(
            uris.remove_dot_segments('../bar'),
            'bar')
        self.assertEqual(
            uris.remove_dot_segments('./bar'),
            'bar')
        self.assertEqual(
            uris.remove_dot_segments('../bar/'),
            'bar/')
        self.assertEqual(
            uris.remove_dot_segments('./bar/'),
            'bar/')
        self.assertEqual(
            uris.remove_dot_segments('.././bar'),
            'bar')
        self.assertEqual(
            uris.remove_dot_segments('./../bar'),
            'bar')
        self.assertEqual(
            uris.remove_dot_segments('./.././bar'),
            'bar')
        self.assertEqual(
            uris.remove_dot_segments('.././../bar'),
            'bar')
        self.assertEqual(
            uris.remove_dot_segments('../../bar'),
            'bar')
        self.assertEqual(
            uris.remove_dot_segments('././bar'),
            'bar')

        self.assertEqual(
            uris.remove_dot_segments('bar/..'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('bar/.'),
            'bar/')
        self.assertEqual(
            uris.remove_dot_segments('/bar/..'),
            '/')
        self.assertEqual(
            uris.remove_dot_segments('/bar/.'),
            '/bar/')
        self.assertEqual(
            uris.remove_dot_segments('bar/../'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('bar/./'),
            'bar/')
        self.assertEqual(
            uris.remove_dot_segments('bar/../.'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('bar/./..'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('bar/./../.'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('bar/.././..'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('bar/../..'),
            '')
        self.assertEqual(
            uris.remove_dot_segments('bar/./.'),
            'bar/')
        self.assertEqual(
            uris.remove_dot_segments('bar/././'),
            'bar/')
        self.assertEqual(
            uris.remove_dot_segments('/foo/bar/..'),
            '/foo/')

        self.assertEqual(
            uris.remove_dot_segments('/foo/./bar'),
            '/foo/bar')
        self.assertEqual(
            uris.remove_dot_segments('/foo/../bar'),
            '/bar')
        self.assertEqual(
            uris.remove_dot_segments('/foo/../bar/'),
            '/bar/')
        self.assertEqual(
            uris.remove_dot_segments('/foo/../bar/..'),
            '/')

        self.assertEqual(
            uris.remove_dot_segments('g.'),
            'g.')
        self.assertEqual(
            uris.remove_dot_segments('.g'),
            '.g')
        self.assertEqual(
            uris.remove_dot_segments('g..'),
            'g..')
        self.assertEqual(
            uris.remove_dot_segments('..g'),
            '..g')
        self.assertEqual(
            uris.remove_dot_segments('/b/c/./../g'),
            '/b/g')
        self.assertEqual(
            uris.remove_dot_segments('/b/c/./g/.'),
            '/b/c/g/')
        self.assertEqual(
            uris.remove_dot_segments('/b/c/g/./h'),
            '/b/c/g/h')
        self.assertEqual(
            uris.remove_dot_segments('/b/c/g/../h'),
            '/b/c/h')
        self.assertEqual(
            uris.remove_dot_segments('/b/c/g;x=1/./y'),
            '/b/c/g;x=1/y')
        self.assertEqual(
            uris.remove_dot_segments('/b/c/g;x=1/../y'),
            '/b/c/y')
