import io
import unittest

from svgelements import *


class TestElementUse(unittest.TestCase):

    def test_issue_156(self):
        q1 = io.StringIO(u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="1920"
   height="1080"
   viewBox="0 0 507.99999 285.75001"
   version="1.1"
   id="svg10274"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs id="defs10271" />
  <g
     inkscape:label="Layer"
     inkscape:groupmode="layer"
     id="layer1">
    <rect
       style="fill:#ff0000;fill-rule:evenodd;stroke-width:0.2;stroke-linecap:round"
       id="rect2728"
       width="486.83334"
       height="21.166666"
       x="10.583323"
       y="-42.333332" />
    <use
       x="0"
       y="0"
       xlink:href="#rect2728"
       id="use2810"
       transform="translate(0,74.083333)"
       width="100%"
       height="100%" />
  </g>
</svg>''')
        layout = SVG.parse(
            source=q1,
            reify=True,
            ppi=DEFAULT_PPI,
            width=1,
            height=1,
            color="black",
            transform=None,
            context=None
        )

        template1 = layout.get_element_by_id("rect2728")
        rect_before_use = template1.bbox()

        q2 = io.StringIO(u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg
           width="1920"
           height="1080"
           viewBox="0 0 507.99999 285.75001"
           version="1.1"
           id="svg10274"
           xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
           xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
           xmlns:xlink="http://www.w3.org/1999/xlink"
           xmlns="http://www.w3.org/2000/svg"
           xmlns:svg="http://www.w3.org/2000/svg">
          <defs id="defs10271" />
          <g
             inkscape:label="Layer"
             inkscape:groupmode="layer"
             id="layer1">
            <use
               x="0"
               y="0"
               xlink:href="#rect2728"
               id="use2810"
               transform="translate(0,74.083333)"
               width="100%"
               height="100%" />
            <rect
               style="fill:#ff0000;fill-rule:evenodd;stroke-width:0.2;stroke-linecap:round"
               id="rect2728"
               width="486.83334"
               height="21.166666"
               x="10.583323"
               y="-42.333332" />
          </g>
        </svg>''')
        layout = SVG.parse(
            source=q2,
            reify=True,
            ppi=DEFAULT_PPI,
            width=1,
            height=1,
            color="black",
            transform=None,
            context=None
        )

        template2 = layout.get_element_by_id("rect2728")
        use_before_rect = template2.bbox()
        self.assertEqual(use_before_rect, rect_before_use)