from __future__ import print_function

import io
import unittest

from svgelements import *


class TestElementViewbox(unittest.TestCase):

    def test_viewbox_incomplete_transform(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg/>')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 1000)
        self.assertEqual(m.height, 1000)
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg/>')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 500)

        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg height="200"/>')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 1000)
        self.assertEqual(m.height, 200)
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg height="200"/>')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 200)

        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="200"/>')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 1000)
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="200"/>')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 500)

        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="200" height="200"/>')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg width="200" height="200"/>')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)

        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg viewbox="0, 0, 100, 100"/>')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 1000)
        self.assertEqual(m.height, 1000)
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg viewbox="0, 0, 100, 100"/>')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 500)

        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg viewbox="0, 0, 100, 100" height="100"/>')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 1000)
        self.assertEqual(m.height, 100)
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg viewbox="0, 0, 100, 100" height="100"/>')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 100)

        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg viewbox="0, 0, 100, 100" height="200" width="200"/>')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)

    def test_viewbox_simple(self):
        r = Rect(0, 0, 100, 100)
        v = Viewbox({'viewBox': '0 0 100 100'})
        self.assertEqual(v.transform(r), '')

    def test_viewbox_scale(self):
        r = Rect(0, 0, 200, 200)
        v = Viewbox('0 0 100 100')
        self.assertEqual(v.transform(r), 'scale(2, 2)')

    def test_viewbox_translate(self):
        r = Rect(0, 0, 100, 100)
        v = Viewbox(Viewbox('-50 -50 100 100'))
        self.assertEqual(v.transform(r), 'translate(50, 50)')

    def test_viewbox_parse_empty(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg>'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertEqual(len(q), 1)
        self.assertEqual(None, m.viewbox)

    def test_viewbox_parse_100(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg viewBox="0 0 100 100">'
                        '</svg>')
        m = SVG.parse(q, width=100, height=100)
        q = list(m.elements())
        self.assertEqual(len(q), 1)
        self.assertEqual(Matrix(m.viewbox_transform), Matrix.identity())

    def test_viewbox_parse_translate(self):
        q = io.StringIO('<?xml version="1.0" encoding="utf-8" ?>\n'
                        '<svg viewBox="-1 -1 100 100" width="100" height="100">'
                        '</svg>')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertEqual(len(q), 1)
        self.assertEqual(Matrix(m.viewbox_transform), Matrix.translate(1, 1))
