import unittest

from svgelements import *


class TestPath(unittest.TestCase):
    """Tests of the SVG Path element."""

    def test_subpaths(self):
        path = Path("M0,0 50,50 100,100Z M0,100 50,50, 100,0")
        for i, p in enumerate(path.as_subpaths()):
            if i == 0:
                self.assertEqual(p.d(), "M 0,0 L 50,50 L 100,100 Z")
            elif i == 1:
                self.assertEqual(p.d(), "M 0,100 L 50,50 L 100,0")
            self.assertLessEqual(i, 1)

    def test_subpath_degenerate(self):
        path = Path("")
        for i, p in enumerate(path.as_subpaths()):
            pass

    def test_subpaths_no_move(self):
        path = Path("M0,0 50,0 50,50 0,50 Z L0,100 100,100 100,0")
        for i, p in enumerate(path.as_subpaths()):
            if i == 0:
                self.assertEqual(p.d(), "M 0,0 L 50,0 L 50,50 L 0,50 Z")
            elif i == 1:
                self.assertEqual(p.d(), "L 0,100 L 100,100 L 100,0")
            self.assertLessEqual(i, 1)
        path = Path("M0,0ZZZZZ")
        subpaths = list(path.as_subpaths())
        self.assertEqual(len(subpaths), 5)

    def test_count_subpaths(self):
        path = Path("M0,0 50,50 100,100Z M0,100 50,50, 100,0")
        self.assertEqual(path.count_subpaths(), 2)

    def test_subpath(self):
        path = Path("M0,0 50,50 100,100Z M0,100 50,50, 100,0")
        subpath = path.subpath(0)
        self.assertEqual(subpath.d(), "M 0,0 L 50,50 L 100,100 Z")
        subpath = path.subpath(1)
        self.assertEqual(subpath.d(), "M 0,100 L 50,50 L 100,0")

    def test_move_quad_smooth(self):
        path = Path()
        path.move((4, 4), (20, 20), (25, 25), 6 + 3j)
        path.quad((20, 33), (100, 100))
        path.smooth_quad((13, 45), (16, 16), (34, 56), "z").closed()
        self.assertEqual(path.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 T 13,45 T 16,16 T 34,56 T 4,4 Z")

    def test_move_cubic_smooth(self):
        path = Path()
        path.move((4, 4), (20, 20), (25, 25), 6 + 3j)
        path.cubic((20, 33), (25, 25), (100, 100))
        path.smooth_cubic((13, 45), (16, 16), (34, 56), "z").closed()
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
        #Issue 45
        p = Path("M0,0 1,1")
        p.reverse()
        self.assertEqual(p, "M1,1 0,0")

        p = Path("M0,0 M1,1")
        p.reverse()
        self.assertEqual(p, "M1,1 M0,0")

        p = Path("M1,1 L5,5M2,1 L6,5M3,1 L7,5")
        subpaths = list(p.as_subpaths())
        subpaths[1].reverse()
        self.assertEqual("M 1,1 L 5,5 M 6,5 L 2,1 M 3,1 L 7,5", str(p))
        subpaths[1].reverse()
        self.assertEqual("M 1,1 L 5,5 M 2,1 L 6,5 M 3,1 L 7,5", str(p))

        p = Path("M1,1 L5,5M2,1 L6,5ZM3,1 L7,5")
        subpaths = list(p.as_subpaths())
        subpaths[1].reverse()
        self.assertEqual("M 6,5 L 2,1 Z", str(subpaths[1]))
        self.assertEqual("M 1,1 L 5,5 M 6,5 L 2,1 Z M 3,1 L 7,5", str(p))

        p = Path("M1,1 L5,5M2,1 6,5 100,100 200,200 ZM3,1 L7,5")
        subpaths = list(p.as_subpaths())
        subpaths[1].reverse()
        self.assertEqual("M 1,1 L 5,5 M 200,200 L 100,100 L 6,5 L 2,1 Z M 3,1 L 7,5", str(p))

    def test_validation_delete(self):
        p = Path("M1,1 M2,2 M3,3 M4,4")
        del p[2]
        self.assertEqual(p, "M1,1 M2,2 M4,4")
        p = Path("M0,0 L 1,1 L 2,2 L 3,3 L 4,4z")
        del p[3]
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 4,4z")
        p = Path("M0,0 L 1,1 L 2,2 M 3,3 L 4,4z")
        del p[3]
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 4,4z")

    def test_validation_insert(self):
        p = Path("M1,1 M2,2 M4,4")
        p.insert(2, "M3,3")
        self.assertEqual(p, "M1,1 M2,2 M3,3 M4,4")
        p = Path("M0,0 L 1,1 L 2,2 L 4,4")
        p.insert(3, "L3,3")
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4")

    def test_validation_append(self):
        p = Path("M1,1 M2,2 M3,3")
        p.append("M4,4")
        self.assertEqual(p, "M1,1 M2,2 M3,3 M4,4")
        p = Path("M0,0 L 1,1 L 2,2 L 3,3")
        p.append("L4,4")
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4")
        p.append("Z")
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4 Z")

        p = Path("M1,1 M2,2")
        p.append("M3,3 M4,4")
        self.assertEqual(p, "M1,1 M2,2 M3,3 M4,4")
        p = Path("M0,0 L 1,1 L 2,2")
        p.append("L 3,3 L4,4")
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4")
        p.append("Z")
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4 Z")

    def test_validation_extend(self):
        p = Path("M1,1 M2,2")
        p.extend(Path("M3,3 M4,4"))
        self.assertEqual(p, "M1,1 M2,2 M3,3 M4,4")
        p = Path("M0,0 L 1,1 L 2,2")
        p.extend(Path("L 3,3 L4,4"))
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4")
        p.extend(Path("Z"))
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4 Z")

        p = Path("M1,1 M2,2")
        p.extend("M3,3 M4,4")
        self.assertEqual(p, "M1,1 M2,2 M3,3 M4,4")
        p = Path("M0,0 L 1,1 L 2,2")
        p.extend("L 3,3 L4,4")
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4")
        p.extend("Z")
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 L 3,3 L 4,4 Z")

    def test_validation_setitem(self):
        p = Path("M1,1 M2,2 M3,3 M4,4")
        p[2] = Line(None, (3,3))
        self.assertEqual(p, "M1,1 M2,2 L3,3 M4,4")
        p = Path("M0,0 L 1,1 L 2,2 L 3,3 L 4,4z")
        p[3] = Move(None, (3,3))
        self.assertEqual(p, "M0,0 L 1,1 L 2,2 M3,3 L 4,4z")

    def test_validation_setitem_str(self):
        p = Path("M1,1 M2,2 M3,3 M4,4")
        p[2] = "L3,3"
        self.assertEqual(p, Path("M1,1 M2,2 L3,3 M4,4"))
        p = Path("M0,0 L 1,1 L 2,2 L 3,3 L 4,4z")
        p[3] = "M3,3"
        self.assertEqual(p, Path("M0,0 L 1,1 L 2,2 M3,3 L 4,4z"))

    def test_arc_start_t(self):
        m = Path("m 0,0 a 5.01,5.01 180 0,0 0,10 z"
                 "m 0,0 a 65,65 180 0,0 65,66 z")
        for a in m:
            if isinstance(a, Arc):
                start_t = a.get_start_t()
                a_start = a.point_at_t(start_t)
                self.assertEqual(a.start, a_start)
                self.assertEqual(a.end, a.point_at_t(a.get_end_t()))

    def test_relative_roundabout(self):
        m = Path("m 0,0 a 5.01,5.01 180 0,0 0,10 z")
        self.assertEqual(m.d(), "m 0,0 a 5.01,5.01 180 0,0 0,10 z")
        m = Path("M0,0 1,1 z")
        self.assertEqual(m.d(), "M 0,0 L 1,1 z")
        self.assertEqual(m.d(relative=True), "m 0,0 l 1,1 z")
        self.assertEqual(m.d(relative=False), "M 0,0 L 1,1 Z")
        m = Path("M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 Q 180,167 13,45 T 16,16 T 34,56 T 4,4 z")
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 Q 180,167 13,45 T 16,16 T 34,56 T 4,4 z")
        self.assertEqual(m.d(smooth=False), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 Q 180,167 13,45 Q -154,-77 16,16 Q 186,109 34,56 Q -118,3 4,4 z")
        self.assertEqual(m.d(smooth=True), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 T 13,45 T 16,16 T 34,56 T 4,4 z")
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 Q 180,167 13,45 T 16,16 T 34,56 T 4,4 z")

    def test_path_z_termination(self):
        m = Path("M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 Z")
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 4,4 Z")
        m = Path("M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 T Z")
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 T 4,4 Z")
        m = Path("M 4,4 L 20,20 L 25,25 L 6,3 Q Z")
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 4,4 4,4 Z")
        m = Path("M 4,4 L 20,20 L 25,25 L 6,3 C Z")
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 C 4,4 4,4 4,4 Z")
        m = Path("M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 T z")
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 20,33 100,100 T 4,4 z")
        m = Path("m 0,0 1,1 A 5.01,5.01 180 0,0 z")
        self.assertEqual(m.d(), "m 0,0 l 1,1 A 5.01,5.01 180 0,0 0,0 z")
        m = Path("m0,0z")
        self.assertEqual(m.d(), "m 0,0 z")
        m = Path("M0,0Lz")
        self.assertEqual(m.d(), "M 0,0 L 0,0 z")

        m = Path("M 4,4 L 20,20 L 25,25 L 6,3").quad("Z").closed()
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 Q 4,4 4,4 Z")
        m = Path("M 4,4 L 20,20 L 25,25 L 6,3").cubic("Z").closed()
        self.assertEqual(m.d(), "M 4,4 L 20,20 L 25,25 L 6,3 C 4,4 4,4 4,4 Z")

    def test_path_setitem_slice(self):
        m = Path("M0,0 1,1 z")
        m[1:] = 'L2,2z'
        self.assertEqual(m.d(), "M 0,0 L 2,2 z")
        self.assertTrue(m._is_valid())
        del m[1]
        self.assertEqual(m.d(), "M 0,0 z")
        self.assertTrue(m._is_valid())

        m = Path("M0,0z")
        m[:] = 'M1,1z'
        self.assertEqual(m.d(), "M 1,1 z")
        self.assertTrue(m._is_valid())

        m = Path("M0,0z")
        del m[:]
        self.assertEqual(m, '')
        self.assertTrue(m._is_valid())

        m = Path("M0,0z")
        m[0] = "M1,1"
        self.assertEqual(m.d(), "M 1,1 z")
        self.assertTrue(m._is_valid())
        m[1] = "z"
        self.assertTrue(m._is_valid())

        m = Path("M0,0z")
        del m[1]
        self.assertEqual(m.d(), "M 0,0")
        self.assertTrue(m._is_valid())

        m = Path("M0,0 1,1 z")
        m[3:] = "M5,5z"
        self.assertEqual(m.d(), "M 0,0 L 1,1 z M 5,5 z")
        self.assertTrue(m._is_valid())

        m = Path("M0,0 1,1 z")
        m[-1:] = "M5,5z"
        self.assertEqual(m.d(), "M 0,0 L 1,1 M 5,5 z")
        self.assertTrue(m._is_valid())

        m = Path("M0,0 1,1 z")
        def m_assign():
            m[-1] = 'M5,5z'
        self.assertRaises(ValueError, m_assign)

    def test_iterative_loop_building_line(self):
        path = Path()
        path.move(0)
        path.line(*([complex(1, 1)] * 2000))

    def test_iterative_loop_building_vert(self):
        path = Path()
        path.move(0)
        path.vertical(*([5.0] * 2000))

    def test_iterative_loop_building_horiz(self):
        path = Path()
        path.move(0)
        path.horizontal(*([5.0] * 2000))

    def test_iterative_loop_building_quad(self):
        path = Path()
        path.move(0)
        path.quad(*([complex(1, 1), complex(1, 1)] * 1000))

    def test_iterative_loop_building_cubic(self):
        path = Path()
        path.move(0)
        path.cubic(*([complex(1, 1), complex(1, 1), complex(1, 1)] * 1000))

    def test_iterative_loop_building_arc(self):
        path = Path()
        path.move(0)
        q = [0, 0, 0, 0, 0, complex(1, 1)] * 2000
        path.arc(*q)

