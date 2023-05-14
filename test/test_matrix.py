import unittest

from svgelements import *


class TestPathMatrix(unittest.TestCase):
    """Tests the functionality of the Matrix element."""

    def test_rotate_css_angles(self):
        matrix = Matrix("rotate(90, 100,100)")
        path = Path("M0,0Z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(90deg, 100,100)")
        path = Path("M0,0Z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(0.25turn, 100,100)")
        path = Path("M0,0Z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(100grad, 100,100)")
        path = Path("M0,0Z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())
        matrix = Matrix("rotate(1.5707963267948966rad, 100,100)")
        path = Path("M0,0Z")
        path *= matrix
        self.assertEqual("M 200,0 Z", path.d())

    def test_matrix_multiplication(self):
        self.assertEqual(
            Matrix("scale(0.2) translate(-5,-5)"),
            Matrix("translate(-5,-5)") * Matrix("scale(0.2)"),
        )
        self.assertEqual(
            Matrix("translate(-5,-5) scale(0.2)"),
            Matrix("scale(0.2)") * Matrix("translate(-5,-5)"),
        )

    def test_rotate_css_distance(self):
        matrix = Matrix("rotate(90deg,100cm,100cm)")
        matrix.render(ppi=DEFAULT_PPI)
        path = Path("M0,0z")
        path *= matrix
        d = Length("1cm").value(ppi=DEFAULT_PPI)
        p2 = Path("M 200,0 Z") * Matrix("scale(%f)" % d)
        p2.values[SVG_ATTR_VECTOR_EFFECT] = SVG_VALUE_NON_SCALING_STROKE
        self.assertEqual(p2, path)

    def test_skew_single_value(self):
        m0 = Matrix("skew(15deg,0deg)")
        m1 = Matrix("skewX(15deg)")
        self.assertEqual(m0, m1)
        m0 = Matrix("skew(0deg,15deg)")
        m1 = Matrix("skewY(15deg)")
        self.assertEqual(m0, m1)

    def test_scale_single_value(self):
        m0 = Matrix("scale(2,1)")
        m1 = Matrix("scaleX(2)")
        self.assertEqual(m0, m1)
        m0 = Matrix("scale(1,2)")
        m1 = Matrix("scaleY(2)")
        self.assertEqual(m0, m1)

    def test_translate_single_value(self):
        m0 = Matrix("translate(500cm,0)")
        m1 = Matrix("translateX(500cm)")
        self.assertEqual(m0, m1)
        m0 = Matrix("translate(0,500cm)")
        m1 = Matrix("translateY(500cm)")
        self.assertEqual(m0, m1)
        m0 = Matrix("translate(500cm)")
        m1 = Matrix("translateX(500cm)")
        self.assertEqual(m0, m1)

    def test_translate_css_value(self):
        m0 = Matrix("translate(50mm,5cm)")
        m1 = Matrix("translate(5cm,5cm)")
        self.assertEqual(m0, m1)

    def test_rotate_css_value(self):
        m0 = Matrix("rotate(90deg, 50cm,50cm)", ppi=DEFAULT_PPI)
        m1 = Matrix("rotate(0.25turn, 500mm,500mm)", ppi=DEFAULT_PPI)
        self.assertEqual(m0, m1)

    def test_transform_translate(self):
        matrix = Matrix("translate(5,4)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z").closed()
        path *= matrix
        self.assertEqual("M 5,4 L 5,104 L 105,104 L 105,4 L 5,4 Z", path.d())

    def test_transform_scale(self):
        matrix = Matrix("scale(2)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z").closed()
        path *= matrix
        self.assertEqual("M 0,0 L 0,200 L 200,200 L 200,0 L 0,0 Z", path.d())

    def test_transform_rotate(self):
        matrix = Matrix("rotate(360)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        self.assertAlmostEqual(path[0][1].x, 0)
        self.assertAlmostEqual(path[0][1].y, 0)

        self.assertAlmostEqual(path[1][1].x, 0)
        self.assertAlmostEqual(path[1][1].y, 100)

        self.assertAlmostEqual(path[2][1].x, 100)
        self.assertAlmostEqual(path[2][1].y, 100)
        self.assertAlmostEqual(path[3][1].x, 100)
        self.assertAlmostEqual(path[3][1].y, 0)
        self.assertAlmostEqual(path[4][1].x, 0)
        self.assertAlmostEqual(path[4][1].y, 0)

    def test_transform_value(self):
        matrix = Matrix("rotate(360,50,50)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z")
        path *= matrix
        self.assertAlmostEqual(path[0][1].x, 0)
        self.assertAlmostEqual(path[0][1].y, 0)

        self.assertAlmostEqual(path[1][1].x, 0)
        self.assertAlmostEqual(path[1][1].y, 100)

        self.assertAlmostEqual(path[2][1].x, 100)
        self.assertAlmostEqual(path[2][1].y, 100)
        self.assertAlmostEqual(path[3][1].x, 100)
        self.assertAlmostEqual(path[3][1].y, 0)
        self.assertAlmostEqual(path[4][1].x, 0)
        self.assertAlmostEqual(path[4][1].y, 0)

    def test_transform_skewx(self):
        matrix = Matrix("skewX(10,50,50)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z").closed()
        path *= matrix
        self.assertEqual(
            "M -8.81634903542,0 L 8.81634903542,100 L 108.816349035,100 L 91.1836509646,0 L -8.81634903542,0 Z",
            path.d(),
        )

    def test_transform_skewy(self):
        matrix = Matrix("skewY(10, 50,50)")
        path = Path()
        path.move((0, 0), (0, 100), (100, 100), 100 + 0j, "z").closed()
        path *= matrix
        self.assertEqual(
            "M 0,-8.81634903542 L 0,91.1836509646 L 100,108.816349035 L 100,8.81634903542 L 0,-8.81634903542 Z",
            path.d(),
        )

    def test_matrix_repr_rotate(self):
        """
        [a c e]
        [b d f]
        """
        self.assertEqual(Matrix(0, 1, -1, 0, 0, 0), Matrix.rotate(radians(90)))

    def test_matrix_repr_scale(self):
        """
        [a c e]
        [b d f]
        """
        self.assertEqual(Matrix(2, 0, 0, 2, 0, 0), Matrix.scale(2))

    def test_matrix_repr_hflip(self):
        """
        [a c e]
        [b d f]
        """
        self.assertEqual(Matrix(-1, 0, 0, 1, 0, 0), Matrix.scale(-1, 1))

    def test_matrix_repr_vflip(self):
        """
        [a c e]
        [b d f]
        """
        self.assertEqual(Matrix(1, 0, 0, -1, 0, 0), Matrix.scale(1, -1))

    def test_matrix_repr_post_cat(self):
        """
        [a c e]
        [b d f]
        """
        m = Matrix.scale(2)
        m.post_cat(Matrix.translate(-20, -20))
        self.assertEqual(Matrix(2, 0, 0, 2, -20, -20), m)

    def test_matrix_repr_pre_cat(self):
        """
        [a c e]
        [b d f]
        """
        m = Matrix.translate(-20, -20)
        m.pre_cat(Matrix.scale(2))
        self.assertEqual(Matrix(2, 0, 0, 2, -20, -20), m)

    def test_matrix_point_rotated_by_matrix(self):
        matrix = Matrix()
        matrix.post_rotate(radians(90), 100, 100)
        p = matrix.point_in_matrix_space((50, 50))
        self.assertAlmostEqual(p[0], 150)
        self.assertAlmostEqual(p[1], 50)

    def test_matrix_point_scaled_in_space(self):
        matrix = Matrix()
        matrix.post_scale(2, 2, 50, 50)

        p = matrix.point_in_matrix_space((50, 50))
        self.assertAlmostEqual(p[0], 50)
        self.assertAlmostEqual(p[1], 50)

        p = matrix.point_in_matrix_space((25, 25))
        self.assertAlmostEqual(p[0], 0)
        self.assertAlmostEqual(p[1], 0)

        matrix.post_rotate(radians(45), 50, 50)
        p = matrix.point_in_matrix_space((25, 25))
        self.assertAlmostEqual(p[0], 50)

        matrix = Matrix()
        matrix.post_scale(0.5, 0.5)
        p = matrix.point_in_matrix_space((100, 100))
        self.assertAlmostEqual(p[0], 50)
        self.assertAlmostEqual(p[1], 50)

        matrix = Matrix()
        matrix.post_scale(2, 2, 100, 100)
        p = matrix.point_in_matrix_space((50, 50))
        self.assertAlmostEqual(p[0], 0)
        self.assertAlmostEqual(p[1], 0)

    def test_matrix_cat_identity(self):
        identity = Matrix()
        from random import random

        for i in range(50):
            q = Matrix(random(), random(), random(), random(), random(), random())
            p = copy(q)
            q.post_cat(identity)
            self.assertEqual(q, p)

    def test_matrix_pre_and_post_1(self):
        from random import random

        for i in range(50):
            tx = random() * 1000 - 500
            ty = random() * 1000 - 500
            rx = random() * 2
            ry = random() * 2
            a = random() * tau
            q = Matrix()
            q.post_translate(tx, ty)
            p = Matrix()
            p.pre_translate(tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_scale(rx, ry, tx, ty)
            p = Matrix()
            p.pre_scale(rx, ry, tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_rotate(a, tx, ty)
            p = Matrix()
            p.pre_rotate(a, tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_skew_x(a, tx, ty)
            p = Matrix()
            p.pre_skew_x(a, tx, ty)
            self.assertEqual(p, q)

            q = Matrix()
            q.post_skew_y(a, tx, ty)
            p = Matrix()
            p.pre_skew_y(a, tx, ty)
            self.assertEqual(p, q)

    def test_matrix_eval_repr(self):
        self.assertTrue(Matrix("rotate(20)") == eval(repr(Matrix("rotate(20)"))))
        self.assertFalse(Matrix("rotate(20)") != eval(repr(Matrix("rotate(20)"))))

    def test_matrix_reverse_scale(self):
        m1 = Matrix("scale(2)")
        m1.inverse()
        m2 = Matrix("scale(0.5)")
        self.assertEqual(m1, m2)
        m1.inverse()
        self.assertEqual(m1, "scale(2)")

    def test_matrix_reverse_translate(self):
        m1 = Matrix("translate(20,20)")
        m1.inverse()
        self.assertEqual(m1, Matrix("translate(-20,-20)"))

    def test_matrix_reverse_rotate(self):
        m1 = Matrix("rotate(30)")
        m1.inverse()
        self.assertEqual(m1, Matrix("rotate(-30)"))

    def test_matrix_reverse_skew(self):
        m1 = Matrix("skewX(1)")
        m1.inverse()
        self.assertEqual(m1, Matrix("skewX(-1)"))

        m1 = Matrix("skewY(1)")
        m1.inverse()
        self.assertEqual(m1, Matrix("skewY(-1)"))

    def test_matrix_reverse_scale_translate(self):
        m1 = Matrix("scale(2) translate(40,40)")
        m1.inverse()
        self.assertEqual(m1, Matrix("translate(-40,-40) scale(0.5)"))

    def test_matrix_map_identity(self):
        """
        Maps one perspective the same perspective.
        """
        m1 = Matrix.map(
            Point(1, 1),
            Point(1, -1),
            Point(-1, -1),
            Point(-1, 1),
            Point(1, 1),
            Point(1, -1),
            Point(-1, -1),
            Point(-1, 1),
        )
        self.assertTrue(m1.is_identity())

        m1 = Matrix.map(
            Point(101, 101),
            Point(101, 99),
            Point(99, 99),
            Point(99, 101),
            Point(101, 101),
            Point(101, 99),
            Point(99, 99),
            Point(99, 101),
        )
        self.assertTrue(m1.is_identity())

    def test_matrix_map_scale_half(self):
        m1 = Matrix.map(
            Point(2, 2),
            Point(2, -2),
            Point(-2, -2),
            Point(-2, 2),
            Point(1, 1),
            Point(1, -1),
            Point(-1, -1),
            Point(-1, 1),
        )
        self.assertEqual(m1, Matrix.scale(0.5))

    def test_matrix_map_translate(self):
        m1 = Matrix.map(
            Point(0, 0),
            Point(0, 1),
            Point(1, 1),
            Point(1, 0),
            Point(100, 100),
            Point(100, 101),
            Point(101, 101),
            Point(101, 100),
        )
        self.assertEqual(m1, Matrix.translate(100, 100))

    def test_matrix_map_rotate(self):
        m1 = Matrix.map(
            Point(0, 0),
            Point(0, 1),
            Point(1, 1),
            Point(1, 0),
            Point(0, 1),
            Point(1, 1),
            Point(1, 0),
            Point(0, 0),
        )
        m2 = Matrix("rotate(-90deg, 0.5, 0.5)")
        self.assertEqual(m1, m2)

    def test_matrix_map_translate_scale_y(self):
        m1 = Matrix.map(
            Point(0, 0),
            Point(0, 1),
            Point(1, 1),
            Point(1, 0),
            Point(100, 100),
            Point(100, 102),
            Point(101, 102),
            Point(101, 100),
        )
        self.assertEqual(m1, Matrix.scale_y(2) * Matrix.translate(100, 100))

    def test_matrix_map_map(self):
        points = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]

        for m in (
            Matrix("skewX(10deg)"),
            Matrix("skewX(8deg)"),
            Matrix("skewX(5deg)"),
            Matrix("skewY(10deg)"),
            Matrix("skewX(8deg)"),
            Matrix("skewX(5deg)"),
            Matrix("scale(1.4235)"),
            Matrix("scale(1.4235,4.39392)"),
            Matrix("translate(100,200)"),
            Matrix("translate(-50,-20.3949)"),
        ):
            points_to = [m.point_in_matrix_space(p) for p in points]
            m1 = Matrix.map(*points, *points_to)
            self.assertEqual(m, m1)

    def test_matrix_perspective_ccw_unit_square(self):
        """
        This is the unit square ccw. So we mirror it across the x-axis and rotate it back into position.
        """
        m1 = Matrix.perspective(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1))
        m2 = Matrix.scale(-1, 1) * Matrix("rotate(-90deg)")
        self.assertEqual(m1, m2)

    def test_matrix_perspective_unit_square(self):
        """
        This is the cw unit square, which is our default perspective, meaning we have the identity matrix
        """
        m1 = Matrix.perspective(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
        m2 = Matrix()
        self.assertEqual(m1, m2)

    def test_matrix_perspective_scale_rotate(self):
        m1 = Matrix.perspective(Point(-2, -2), Point(-2, 2), Point(2, 2), Point(2, -2))
        m2 = Matrix("scale(4)") * Matrix("translate(-2,-2)")
        self.assertEqual(m1, m2)

    def test_matrix_map_map3(self):
        points = [Point(0, 0), Point(0, 1), Point(1, 0)]

        for m in (
            Matrix("skewX(10deg)"),
            Matrix("skewX(8deg)"),
            Matrix("skewX(5deg)"),
            Matrix("skewY(10deg)"),
            Matrix("skewX(8deg)"),
            Matrix("skewX(5deg)"),
            Matrix("scale(1.4235)"),
            Matrix("scale(1.4235,4.39392)"),
            Matrix("translate(100,200)"),
            Matrix("translate(-50,-20.3949)"),
        ):
            points_to = [m.point_in_matrix_space(p) for p in points]
            m1 = Matrix.map3(*points, *points_to)
            self.assertEqual(m, m1)

    def test_matrix_affine_ccw_unit_square(self):
        """
        This is the unit square ccw. So we mirror it across the x-axis and rotate it back into position.
        """
        m1 = Matrix.affine(Point(0, 0), Point(1, 0), Point(0, 1))
        m2 = Matrix.scale(-1, 1) * Matrix("rotate(-90deg)")
        self.assertEqual(m1, m2)

    def test_matrix_affine_unit_square(self):
        """
        This is the cw unit square, which is our default perspective, meaning we have the identity matrix
        """
        m1 = Matrix.affine(Point(0, 0), Point(0, 1), Point(1, 0))
        m2 = Matrix()
        self.assertEqual(m1, m2)

    def test_matrix_affine_scale_rotate(self):
        m1 = Matrix.affine(Point(-2, -2), Point(-2, 2), Point(2, -2))
        m2 = Matrix("scale(4)") * Matrix("translate(-2,-2)")
        self.assertEqual(m1, m2)
