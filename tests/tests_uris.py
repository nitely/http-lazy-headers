# -*- coding: utf-8 -*-

import unittest

from http_lazy_headers.shared.common import uris
from http_lazy_headers.shared.common import hosts


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
        self.assertSequenceEqual(
            uris.remove_dot_segments('/a/b/c/./../../g'),
            ['', 'a', 'g'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('mid/content=5/../6'),
            ['mid', '6'])

        self.assertSequenceEqual(
            uris.remove_dot_segments('../'),
            [])
        self.assertSequenceEqual(
            uris.remove_dot_segments('./'),
            [])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/./'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/./'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/.'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/../'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('././'),
            [])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('.'),
            [])
        self.assertSequenceEqual(
            uris.remove_dot_segments('..'),
            [])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/../../'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/../..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('../../'),
            [])
        self.assertSequenceEqual(
            uris.remove_dot_segments('./././././'),
            [])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/./././././'),
            ['', ''])

        self.assertSequenceEqual(
            uris.remove_dot_segments('//'),
            ['', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('///'),
            ['', '', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('//../'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('////../'),
            ['', '', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('///../'),
            ['', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('//../'),
            ['', ''])

        # The minimal amount of slashes left is always one
        self.assertSequenceEqual(
            uris.remove_dot_segments('//../../../../../'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('///../../../../../'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('//..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('///..'),
            ['', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('//../../../../..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('///../../../../..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/..//'),
            ['', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/..///'),
            ['', '', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('..//'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('../..//'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('..///'),
            ['', '', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('../..///'),
            ['', '', ''])

        self.assertSequenceEqual(
            uris.remove_dot_segments('.//'),
            ['', ''])

        self.assertSequenceEqual(
            uris.remove_dot_segments('../bar'),
            ['bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('./bar'),
            ['bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('../bar/'),
            ['bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('./bar/'),
            ['bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('.././bar'),
            ['bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('./../bar'),
            ['bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('./.././bar'),
            ['bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('.././../bar'),
            ['bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('../../bar'),
            ['bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('././bar'),
            ['bar'])

        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/.'),
            ['bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/bar/..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/bar/.'),
            ['', 'bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/../'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/./'),
            ['bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/../.'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/./..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/./../.'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/.././..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/../..'),
            ['', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/./.'),
            ['bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('bar/././'),
            ['bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/foo/bar/..'),
            ['', 'foo', ''])

        self.assertSequenceEqual(
            uris.remove_dot_segments('/foo/./bar'),
            ['', 'foo', 'bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/foo/../bar'),
            ['', 'bar'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/foo/../bar/'),
            ['', 'bar', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/foo/../bar/..'),
            ['', ''])

        self.assertSequenceEqual(
            uris.remove_dot_segments('g.'),
            ['g.'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('.g'),
            ['.g'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('g..'),
            ['g..'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('..g'),
            ['..g'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/b/c/./../g'),
            ['', 'b', 'g'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/b/c/./g/.'),
            ['', 'b', 'c', 'g', ''])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/b/c/g/./h'),
            ['', 'b', 'c', 'g', 'h'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/b/c/g/../h'),
            ['', 'b', 'c', 'h'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/b/c/g;x=1/./y'),
            ['', 'b', 'c', 'g;x=1', 'y'])
        self.assertSequenceEqual(
            uris.remove_dot_segments('/b/c/g;x=1/../y'),
            ['', 'b', 'c', 'y'])

    def test_resolve_relative_reference(self):
        """
        Should resolve relative references
        """
        abs_url = uris.uri(
            schema='http',
            host=hosts.host(unsafe='a'),
            path='b/c/d;p'.split('/'),
            query={'q': ()})

        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path=['g'])),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/g'.split('/')))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path='./g'.split('/'))),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/g'.split('/')))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path='g/'.split('/'))),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/g/'.split('/')))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path='/g'.split('/'))),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path=['g']))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(host=hosts.host(unsafe='g'))),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='g')))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(query={'y': ()})),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/d;p'.split('/'),
                query={'y': ()}))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path=['g'], query={'y': ()})),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/g'.split('/'),
                query={'y': ()}))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(fragment='s')),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/d;p'.split('/'),
                query={'q': ()},
                fragment='s'))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path=['g'], fragment='s')),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/g'.split('/'),
                fragment='s'))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path=['g'], query={'y': ()}, fragment='s')),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/g'.split('/'),
                query={'y': ()},
                fragment='s'))
        self.assertSequenceEqual(
            uris.resolve_relative_reference(
                abs_url, uris.uri(path=';x'.split('/'))),
            uris.uri(
                schema='http',
                host=hosts.host(unsafe='a'),
                path='b/c/;x'.split('/')))
