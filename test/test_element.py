import unittest

from svgelements import *


class TestElementElement(unittest.TestCase):
    """These tests ensure the performance of the SVGElement basecase."""

    def test_element_id(self):
        values = {'id': 'my_id', 'random': True}
        r = Rect(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = Circle(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = Ellipse(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = Polygon(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = Polyline(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = SimpleLine(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = Path(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = SVGImage(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])
        r = SVGText(values)
        self.assertEqual(values['id'], r.values['id'])
        self.assertEqual(values['random'], r.values['random'])
        self.assertRaises(KeyError, lambda: r.values['not_there'])

    def test_element_merge(self):
        values = {'id': 'my_id', 'random': True}
        r = Rect(values, random=False, tat='awesome')
        self.assertEqual(r.values['id'], values['id'])
        self.assertNotEqual(r.values['random'], values['random'])
        self.assertEqual(r.values['tat'], 'awesome')

        r = Rect(fill='red')
        self.assertEqual(r.fill, '#f00')

    def test_element_propagate(self):

        values = {'id': 'my_id', 'random': True}
        r = Rect(values, random=False, tat='awesome')
        r = Rect(r)
        self.assertEqual(r.values['id'], values['id'])
        self.assertNotEqual(r.values['random'], values['random'])
        self.assertEqual(r.values['tat'], 'awesome')

        r = Rect(fill='red')
        r = Rect(r)
        self.assertEqual(r.fill, '#f00')
        r = Rect(stroke='red')
        r = Rect(r)
        self.assertEqual(r.stroke, '#f00')

        r = Rect(width=20)
        r = Rect(r)
        self.assertEqual(r.width, 20)

        p = Path('M0,0 20,0 0,20z M20,20 40,20 20,40z', fill='red')
        p2 = Path(p.subpath(1))
        p2[0].start = None
        self.assertEqual(p2, 'M20,20 40,20 20,40z')
        self.assertEqual(p2.fill, 'red')

