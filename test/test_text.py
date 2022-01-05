import io
import unittest

from svgelements import *


class TestElementText(unittest.TestCase):

    def test_issue_157(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg>
  <g id="layer1">
    <text
       style="font-size:18px;line-height:1.25;font-family:sans-serif;stroke-width:0.264583"
       id="textobject"><tspan
         id="tspanobject"
         x="0"
         y="0">Test</tspan></text>
  </g>
</svg>
        ''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertIsNotNone(q[1].id) # Group
        self.assertIsNotNone(q[2].id) # Text
        self.assertIsNotNone(q[3].id) # TSpan
