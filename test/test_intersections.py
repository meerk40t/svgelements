import unittest
from operator import itemgetter

from svgelements import *

TOL = 1e-4  # default for tests that don't specify a `delta` or `places`


class TestElementIntersections(unittest.TestCase):

    def test_intersect(self):
        """
        test that `some_seg.intersect(another_seg)` will produce properly
        ordered tuples, i.e. the first element in each tuple refers to
        `some_seg` and the second element refers to `another_seg`.
        Also tests that the correct number of intersections is found.

        * This test adapted from svgpathtools
        """
        a = Line(0 + 200j, 300 + 200j)
        b = QuadraticBezier(40 + 150j, 70 + 200j, 210 + 300j)
        c = CubicBezier(60 + 150j, 40 + 200j, 120 + 250j, 200 + 160j)
        d = Arc(70 + 150j, 50 + 100j, 0, 0, 0, 200 + 100j)
        segdict = {'line': a, "quadratic": b, 'cubic': c, 'arc': d}

        # test each segment type against each other type
        for x, y in [(x, y) for x in segdict for y in segdict]:
            if x == y:
                continue
            x = segdict[x]
            y = segdict[y]
            xiy = sorted(x.intersect(y))
            yix = sorted(y.intersect(x), key=itemgetter(1))
            for xy, yx in zip(xiy, yix):
                self.assertAlmostEqual(xy[0], yx[1], delta=TOL)
                self.assertAlmostEqual(xy[1], yx[0], delta=TOL)
                self.assertAlmostEqual(x.point(xy[0]), y.point(yx[0]), delta=TOL)
            self.assertTrue(len(xiy) == len(yix))

        # test each segment against another segment of same type
        for x in segdict:
            count = 1
            if x == "arc":
                count = 2
            x = segdict[x]
            mid = x.point(0.5)
            y = x * Matrix(f"translate(5,0) rotate(90, {mid.x}, {mid.y})")
            xiy = sorted(x.intersect(y))
            yix = sorted(y.intersect(x), key=itemgetter(1))
            for xy, yx in zip(xiy, yix):
                self.assertAlmostEqual(xy[0], yx[1], delta=TOL)
                self.assertAlmostEqual(xy[1], yx[0], delta=TOL)
                self.assertAlmostEqual(x.point(xy[0]), y.point(yx[0]), delta=TOL)
            self.assertTrue(len(xiy) == len(yix))

            self.assertTrue(len(xiy) == count)
            self.assertTrue(len(yix) == count)
