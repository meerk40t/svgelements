import io
import unittest

from svgelements import *


class TestElementUse(unittest.TestCase):

    def test_issue_156(self):
        q1 = io.StringIO(u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="1920"
   height="1080"
   viewBox="0 0 507.99999 285.75001"
   version="1.1"
   id="svg10274"
   inkscape:version="1.1.1 (3bf5ae0d25, 2021-09-20)"
   sodipodi:docname="test.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview10276"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:document-units="mm"
     showgrid="true"
     inkscape:zoom="0.36168631"
     inkscape:cx="836.3601"
     inkscape:cy="504.58089"
     inkscape:window-width="1920"
     inkscape:window-height="1001"
     inkscape:window-x="-9"
     inkscape:window-y="-9"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1"
     units="px">
    <inkscape:grid
       type="xygrid"
       id="grid1868" />
  </sodipodi:namedview>
  <defs
     id="defs10271" />
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

        template = layout.get_element_by_id("rect2728")
        rect_before_use = template.bbox()

        q2 = io.StringIO(u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!-- Created with Inkscape (http://www.inkscape.org/) -->

        <svg
           width="1920"
           height="1080"
           viewBox="0 0 507.99999 285.75001"
           version="1.1"
           id="svg10274"
           inkscape:version="1.1.1 (3bf5ae0d25, 2021-09-20)"
           sodipodi:docname="test.svg"
           xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
           xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
           xmlns:xlink="http://www.w3.org/1999/xlink"
           xmlns="http://www.w3.org/2000/svg"
           xmlns:svg="http://www.w3.org/2000/svg">
          <sodipodi:namedview
             id="namedview10276"
             pagecolor="#ffffff"
             bordercolor="#666666"
             borderopacity="1.0"
             inkscape:pageshadow="2"
             inkscape:pageopacity="0.0"
             inkscape:pagecheckerboard="0"
             inkscape:document-units="mm"
             showgrid="true"
             inkscape:zoom="0.36168631"
             inkscape:cx="836.3601"
             inkscape:cy="504.58089"
             inkscape:window-width="1920"
             inkscape:window-height="1001"
             inkscape:window-x="-9"
             inkscape:window-y="-9"
             inkscape:window-maximized="1"
             inkscape:current-layer="layer1"
             units="px">
            <inkscape:grid
               type="xygrid"
               id="grid1868" />
          </sodipodi:namedview>
          <defs
             id="defs10271" />
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

        template = layout.get_element_by_id("rect2728")
        use_before_rect = template.bbox()
        self.assertEqual(use_before_rect, rect_before_use)