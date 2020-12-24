from __future__ import print_function

import io
import unittest

from svgelements import *


class TestDescriptiveElements(unittest.TestCase):

    def test_descriptive_element(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>\n
                        <svg>
                        <title>Who?</title>
                        <desc>My Friend.</desc>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertEqual(len(q), 3)
        self.assertEqual(q[1].title, "Who?")
        self.assertEqual(q[2].desc, "My Friend.")

