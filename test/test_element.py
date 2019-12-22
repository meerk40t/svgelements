from __future__ import print_function

import unittest
from random import random

from svg.elements import *


class TestElementElement(unittest.TestCase):

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
