from __future__ import print_function

import unittest

from svg.elements import *


class TestPath(unittest.TestCase):

    def test_subpaths(self):
        path = Path("M0,0 50,50 100,100z M0,100 50,50, 100,0")
        for i, p in enumerate(path.as_subpaths()):
            if i == 0:
                self.assertEqual(p.d(), "M 0,0 L 50,50 L 100,100 Z")
            elif i == 1:
                self.assertEqual(p.d(), "M 0,100 L 50,50 L 100,0")
            self.assertLessEqual(i, 1)

    def test_move_quad_smooth(self):
        path = Path()
        path.move((4, 4), (20, 20), (25, 25), 6 + 3j)
        path.quad((20, 33), (100, 100))
        path.smooth_quad((13, 45), (16, 16), (34, 56), "z")
        self.assertEqual(path.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 T 13,45 T 16,16 T 34,56 T 4,4 Z")

    def test_move_cubic_smooth(self):
        path = Path()
        path.move((4, 4), (20, 20), (25, 25), 6 + 3j)
        path.cubic((20, 33), (25, 25), (100, 100))
        path.smooth_cubic((13, 45), (16, 16), (34, 56), "z")
        self.assertEqual(path.d(), "M 4,4 L 20,20 L 25,25 L 6,3 C 20,33 25,25 100,100 S 13,45 16,16 S 34,56 4,4 Z")

    def test_convex_hull(self):
        pts = (3, 4), (4, 6), (18, -2), (9, 0)
        hull = [e for e in Point.convex_hull(pts)]
        self.assertEqual([(3, 4), (9, 0), (18, -2), (4, 6)], hull)

        # bounding box and a bunch of random numbers that must be inside.
        pts = [(100, 100), (100, -100), (-100, -100), (-100, 100)]
        from random import randint
        for i in range(50):
            pts.append((randint(-99, 99), randint(-99, 99)))
        hull = [e for e in Point.convex_hull(pts)]
        for p in hull:
            self.assertEqual(abs(p[0]), 100)
            self.assertEqual(abs(p[1]), 100)

    def test_reverse_path_q(self):
        path = Path("M1,0 22,7 Q 17,17 91,2")
        path.reverse()
        self.assertEqual(path, Path("M 91,2 Q 17,17 22,7 L 1,0"))

    def test_reverse_path_multi_move(self):
        path = Path("M1,0 M2,0 M3,0")
        path.reverse()
        self.assertEqual(path, "M3,0 M2,0 M1,0")
        path = Path("M1,0z M2,0z M3,0z")
        path.reverse()
        self.assertEqual(path, "M3,0 Z M2,0 Z M1,0 Z")

    def test_reverse_path_multipath(self):
        path = Path("M1,0 22,7 Q 17,17 91,2M0,0zM20,20z")
        path.reverse()
        self.assertEqual(path, Path("M20,20zM0,0zM 91,2 Q 17,17 22,7 L 1,0"))

    def test_path_mult_sideeffect(self):
        path = Path("M1,1 10,10 Q 17,17 91,2 T 9,9 C 40,40 20,0, 9,9 S 60,50 0,0 A 25,25 -30 0,1 30,30 z")
        q = path * "scale(2)"
        self.assertEqual(path, "M1,1 10,10 Q 17,17 91,2 T 9,9 C 40,40 20,0, 9,9 S 60,50 0,0 A 25,25 -30 0,1 30,30 z")

    def test_subpath_imult_sideeffect(self):
        path = Path("M1,1 10,10 Q 17,17 91,2 T 9,9 C 40,40 20,0, 9,9 S 60,50 0,0 A 25,25 -30 0,1 30,30 zM50,50z")
        self.assertEqual(
            path,
            "M1,1 10,10 Q 17,17 91,2 T 9,9 C 40,40 20,0, 9,9 S 60,50 0,0 A 25,25 -30 0,1 30,30 zM50,50z")
        for p in path.as_subpaths():
            p *= "scale(2)"
        self.assertEqual(
            path,
            "M 2,2 L 20,20 Q 34,34 182,4 T 18,18 C 80,80 40,0 18,18 S 120,100 0,0 A 50,50 -30 0,1 60,60 ZM100,100z")

    def test_subpath_reverse(self):
        p = Path("M1,1 L5,5M2,1 L6,5M3,1 L7,5")
        subpaths = list(p.as_subpaths())
        subpaths[1].reverse()
        self.assertEqual("M 1,1 L 5,5 M 6,5 L 2,1 M 3,1 L 7,5", str(p))
        subpaths[1].reverse()
        self.assertEqual("M 1,1 L 5,5 M 2,1 L 6,5 M 3,1 L 7,5", str(p))

        p = Path("M1,1 L5,5M2,1 L6,5zM3,1 L7,5")
        subpaths = list(p.as_subpaths())
        subpaths[1].reverse()
        self.assertEqual("M 6,5 L 2,1 Z", str(subpaths[1]))
        self.assertEqual("M 1,1 L 5,5 M 6,5 L 2,1 Z M 3,1 L 7,5", str(p))

        p = Path("M1,1 L5,5M2,1 6,5 100,100 200,200 zM3,1 L7,5")
        subpaths = list(p.as_subpaths())
        subpaths[1].reverse()
        self.assertEqual("M 1,1 L 5,5 M 200,200 L 100,100 L 6,5 L 2,1 Z M 3,1 L 7,5", str(p))