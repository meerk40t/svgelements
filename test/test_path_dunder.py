import unittest

from svgelements import *


class TestPath(unittest.TestCase):
    """Tests of dunder methods of the SVG Path element."""

    def test_path_iadd_str(self):
        p1 = Path("M0,0")
        p1 += "z"
        self.assertEqual(p1, Path("M0,0z"))

        p1 = Path("M2,2z")
        p1 += "M1,1z"
        p1 += "M0,0z"
        subpaths = list(p1.as_subpaths())
        self.assertEqual(str(subpaths[0]), Path("M2,2z"))
        self.assertEqual(str(subpaths[1]), Path("M1,1z"))
        self.assertEqual(str(subpaths[2]), Path("M0,0z"))

    def test_path_add_str(self):
        p1 = Path("M0,0")
        p2 = p1 + "z"
        p1 += "z"
        self.assertEqual(p1, p2)

    def test_path_radd_str(self):
        p1 = Path("M0,0z")
        p2 = "M1,1z" + p1
        subpaths = list(p2.as_subpaths())
        self.assertEqual(str(subpaths[0]), str(Path("M1,1z")))
        self.assertEqual(str(subpaths[1]), str(Path("M0,0z")))

    def test_path_iadd_segment(self):
        p1 = Path("M0,0")
        p1 += Line((0, 0), (7, 7))
        p1 += "z"
        self.assertEqual(p1, Path("M0,0 L7,7 z"))

    def test_path_add_segment(self):
        p1 = Path("M0,0")
        p2 = p1 + Line((0, 0), (7, 7))
        p1 += "z"
        p2 += "z"
        self.assertEqual(p1, Path("M0,0 z"))
        self.assertEqual(p2, Path("M0,0 L7,7 z"))

    def test_path_radd_segment(self):
        p1 = Path("L7,7")
        p1 = Move((0, 0)) + p1
        p1 += "z"
        self.assertEqual(p1, Path("M0,0 L7,7 z"))

    def test_path_from_segment(self):
        p1 = Move(0) + Line(0, (7, 7)) + "z"
        self.assertEqual(p1, Path("M0,0 L7,7 z"))

        p1 = Move(0) + "L7,7" + "z"
        self.assertEqual(p1, Path("M0,0 L7,7 z"))

        p1 = Move(0) + "L7,7z"
        self.assertEqual(p1, Path("M0,0 L7,7 z"))

    def test_segment_mult_string(self):
        p1 = Move(0) * "translate(200,200)"
        self.assertEqual(p1, Move((200, 200)))

        p1 += "z"
        self.assertEqual(p1, Path("M200,200z"))

    def test_path_mult_string(self):
        p1 = Path(Move(0)) * "translate(200,200)"
        self.assertEqual(p1, "M200,200")

        p1 = Path(Move(0)).set('vector-effect', 'non-scaling-stroke') * "scale(0.5) translateX(200)"
        self.assertEqual(p1, "M100,0")
        self.assertNotEqual(p1, "M200,0")

        p1 = Path(Move(0)).set('vector-effect', 'non-scaling-stroke') * "translateX(200) scale(0.5)"
        self.assertEqual(p1, "M200,0")
        self.assertNotEqual(p1, "M100,0")

    def test_path_equals_string(self):
        self.assertEqual(Path("M55,55z"), "M55,55z")
        self.assertEqual(Path("M55 55z"), "M   55,   55z")
        self.assertTrue(Move(0) * "translate(55,55)" + "z" == "m 55, 55Z")
        self.assertTrue(Move(0) * "rotate(0.50turn,100,0)" + "z" == "M200,0z")
        self.assertFalse(Path(Move(0)) == "M0,0z")
        self.assertEqual(Path("M50,50 100,100 0,100 z").set('vector-effect', 'non-scaling-stroke') * "scale(0.1)",
                         "M5,5 L10,10 0,10z")
        self.assertNotEqual(Path("M50,50 100,100 0,100 z") * "scale(0.11)", "M5,5 L10,10 0,10z")
        self.assertEqual(
            Path("M0,0 h10 v10 h-10 v-10z").set('vector-effect', 'non-scaling-stroke') * "scale(0.2) translate(-5,-5)",
            "M -1,-1, L1,-1, 1,1, -1,1, -1,-1 Z"
        )

    def test_path_mult_matrix(self):
        p = Path("L20,20 40,40") * Matrix("Rotate(20)")
        self.assertEqual(p, "L11.953449549205,25.634255282232 23.906899098410,51.268510564463")
        p.reify()
        p += "L 100, 100"
        p += Close()
        self.assertEqual(p, Path("L11.953449549205,25.634255282232 23.906899098410,51.268510564463 100,100 z"))

    def test_partial_path(self):
        p1 = Path("M0,0")
        p2 = Path("L7,7")
        p3 = Path("Z")
        q = p1 + p2 + p3
        m = Path("M0,0 7,7z")
        self.assertEqual(q, m)

