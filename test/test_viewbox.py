import io
import unittest

from svgelements import *


class TestElementViewbox(unittest.TestCase):

    def test_viewbox_creation(self):
        """Test various ways of creating a viewbox are equal."""
        v1 = Viewbox('0 0 100 100', 'xMid')
        v2 = Viewbox(viewBox="0 0 100 100", preserve_aspect_ratio="xMid")
        v3 = Viewbox(x=0, y=0, width=100, height=100, preserveAspectRatio="xMid")
        v4 = Viewbox(v1)
        v5 = Viewbox({"x":0, "y":0, "width":100, "height":100, "preserveAspectRatio":"xMid"})
        self.assertEqual(v1, v2)
        self.assertEqual(v1, v3)
        self.assertEqual(v1, v4)
        self.assertEqual(v1, v5)
        self.assertEqual(v2, v3)
        self.assertEqual(v2, v4)
        self.assertEqual(v2, v5)
        self.assertEqual(v3, v4)
        self.assertEqual(v3, v5)
        self.assertEqual(v4, v5)

    def test_viewbox_incomplete_none(self):
        """
        Test viewboxes based on incomplete information.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg/>''')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 1000)
        self.assertEqual(m.height, 1000)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg/>''')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 500)

    def test_viewbox_incomplete_height(self):
        """
        Test viewboxes based on incomplete information, only height.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg height="200"/>''')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 1000)
        self.assertEqual(m.height, 200)
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg height="200"/>''')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 200)

    def test_viewbox_incomplete_width(self):
        """
        Test viewboxes based on incomplete information, only width.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="200"/>''')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 1000)
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="200"/>''')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 500)

    def test_viewbox_incomplete_dims(self):
        """
        Test viewboxes based on incomplete information, only dims.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="200" height="200"/>''')
        m = SVG.parse(q)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="200" height="200"/>''')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(m.viewbox_transform, '')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)

    def test_viewbox_incomplete_viewbox(self):
        """
        Test viewboxes based on incomplete information, only viewbox.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(1)')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 100)
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100"/>''')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(5)')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 500)

    def test_viewbox_incomplete_height_viewbox(self):
        """
        Test viewboxes based on incomplete information, only height and viewbox.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100" height="100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), '')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 100)
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100" height="100"/>''')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(1) translateX(200)')
        self.assertEqual(m.width, 500)
        self.assertEqual(m.height, 100)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100" height="200" width="200"/>''')
        m = SVG.parse(q, width=500, height=500)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(2)')
        self.assertEqual(m.width, 200)
        self.assertEqual(m.height, 200)

    def test_viewbox_aspect_ratio_xMinMax(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="xMid" viewBox="0 0 100 100" height="100" width="300"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'translateX(100)')
        self.assertEqual(m.width, 300)
        self.assertEqual(m.height, 100)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="xMin" viewBox="0 0 100 100" height="100" width="300"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'translateX(0)')
        self.assertEqual(m.width, 300)
        self.assertEqual(m.height, 100)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="xMax" viewBox="0 0 100 100" height="100" width="300"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'translateX(200)')
        self.assertEqual(m.width, 300)
        self.assertEqual(m.height, 100)

    def test_viewbox_aspect_ratio_xMinMaxSlice(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="xMid slice" viewBox="0 0 100 100" height="100" width="300"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(3)')
        self.assertEqual(m.width, 300)
        self.assertEqual(m.height, 100)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="xMin slice" viewBox="0 0 100 100" height="100" width="300"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(3)')
        self.assertEqual(m.width, 300)
        self.assertEqual(m.height, 100)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="xMax slice" viewBox="0 0 100 100" height="100" width="300"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(3)')
        self.assertEqual(m.width, 300)
        self.assertEqual(m.height, 100)

    def test_viewbox_aspect_ratio_yMinMax(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="yMid" viewBox="0 0 100 100" height="300" width="100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'translateY(100)')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 300)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="yMin" viewBox="0 0 100 100" height="300" width="100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'translateY(0)')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 300)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="yMax" viewBox="0 0 100 100" height="300" width="100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'translateY(200)')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 300)

    def test_viewbox_aspect_ratio_yMinMaxSlice(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="yMid slice" viewBox="0 0 100 100" height="300" width="100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(3)')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 300)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="yMin slice" viewBox="0 0 100 100" height="300" width="100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(3)')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 300)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg preserveAspectRatio="yMax slice" viewBox="0 0 100 100" height="300" width="100"/>''')
        m = SVG.parse(q)
        self.assertEqual(Matrix(m.viewbox_transform), 'scale(3)')
        self.assertEqual(m.width, 100)
        self.assertEqual(m.height, 300)

    def test_viewbox_simple(self):
        r = Rect(0, 0, 100, 100)
        v = Viewbox({'viewBox': '0 0 100 100'})
        self.assertEqual(v.transform(r), '')

    def test_viewbox_issue_228(self):
        self.assertIn(
            SVG(viewBox="0 0 10 10", width="10mm", height="10mm").string_xml(),
            (
                """<svg viewBox="0 0 10 10" width="10mm" height="10mm" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events" />""",
                """<svg height="10mm" version="1.1" viewBox="0 0 10 10" width="10mm" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink" />""",  # Python 3.6
            ),
        )

    def test_issue_228b(self):
        svg = SVG(viewBox="0 0 10 10", width="10mm", height="10mm")
        svg.append(Rect(x="1mm", y="1mm", width="5mm", height="5mm", rx="0.5mm", stroke="red"))
        svg.append(Circle(cx="5mm", cy="5mm", r="0.5mm", stroke="blue"))
        svg.append(Ellipse(cx="5mm", cy="5mm", rx="0.5mm", ry="0.8mm", stroke="lime"))
        svg.append(SimpleLine(x1="5mm", y1="5em", x2="10%", y2="15%", stroke="gray"))
        svg.append(Polygon(5, 10, 20, 30, 40, 7))
        svg.append(Path("M10,10z", stroke="yellow"))
        print(svg.string_xml())

    def test_issue_228c(self):
        rect = Rect(x="1mm", y="1mm", width="5mm", height="5mm", rx="0.5mm", stroke="red")
        print(rect.length())

    def test_viewbox_scale(self):
        r = Rect(0, 0, 200, 200)
        v = Viewbox('0 0 100 100')
        self.assertEqual(v.transform(r), 'scale(2, 2)')

    def test_viewbox_translate(self):
        r = Rect(0, 0, 100, 100)
        v = Viewbox(Viewbox('-50 -50 100 100'))
        self.assertEqual(v.transform(r), 'translate(50, 50)')

    def test_viewbox_parse_empty(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertEqual(len(q), 1)
        self.assertEqual(None, m.viewbox)

    def test_viewbox_parse_100(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0 0 100 100">
                        </svg>''')
        m = SVG.parse(q, width=100, height=100)
        q = list(m.elements())
        self.assertEqual(len(q), 1)
        self.assertEqual(Matrix(m.viewbox_transform), Matrix.identity())

    def test_viewbox_parse_translate(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="-1 -1 100 100" width="100" height="100">
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertEqual(len(q), 1)
        self.assertEqual(Matrix(m.viewbox_transform), Matrix.translate(1, 1))
