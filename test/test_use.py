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

    def test_issue_192(self):
        """
        Rendered wrongly because the matrix from the group as well as the viewport and even the original parse routine
        is utilized twice. The use references the use object rather than the use xml. And should only have the render
        elements of where it is inserted and not of where it appeared in the tree. A Use is effectively copying and
        pasting that node into that place and only overriding x, y, length, and width.
        """

        q1 = io.StringIO(u'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns:xlink="http://www.w3.org/1999/xlink" width="109.322295pt" height="27.66092pt" viewBox="0 0 109.322295 27.66092" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="text_1">
   <g transform="translate(0 21.294961) scale(0.3 -0.3)">
    <defs>
     <path id="CMMI12-45" d="M 4448 1489 
C 4454 1508 4474 1554 4474 1579 
C 4474 1611 4448 1643 4410 1643 
C 4384 1643 4371 1637 4352 1617 
C 4339 1611 4339 1598 4282 1469 
C 3904 570 3629 185 2605 185 
L 1670 185 
C 1581 185 1568 185 1530 192 
C 1459 198 1453 211 1453 262 
C 1453 307 1466 345 1478 403 
L 1920 2176 
L 2554 2176 
C 3053 2176 3091 2066 3091 1874 
C 3091 1810 3091 1752 3046 1560 
C 3034 1534 3027 1508 3027 1489 
C 3027 1444 3059 1425 3098 1425 
C 3155 1425 3162 1469 3187 1559 
L 3552 3042 
C 3552 3073 3526 3105 3488 3105 
C 3430 3105 3424 3080 3398 2990 
C 3270 2501 3142 2361 2573 2361 
L 1965 2361 
L 2362 3930 
C 2419 4154 2432 4154 2694 4154 
L 3610 4154 
C 4397 4154 4557 3943 4557 3458 
C 4557 3451 4557 3273 4531 3062 
C 4525 3036 4518 2998 4518 2985 
C 4518 2934 4550 2915 4589 2915 
C 4634 2915 4659 2941 4672 3055 
L 4806 4174 
C 4806 4195 4819 4263 4819 4277 
C 4819 4352 4762 4352 4646 4352 
L 1523 4352 
C 1402 4352 1338 4352 1338 4229 
C 1338 4154 1382 4154 1491 4154 
C 1888 4154 1888 4114 1888 4052 
C 1888 4020 1882 3994 1862 3924 
L 998 473 
C 941 249 928 185 480 185 
C 358 185 294 185 294 70 
C 294 0 333 0 461 0 
L 3674 0 
C 3814 0 3821 6 3866 110 
L 4448 1489 
z" transform="scale(0.015625)"/>
    </defs>
    <use xlink:href="#CMMI12-45" id="use1" transform="scale(0.996264)"/>
   </g>
  </g>
 </g>
</svg>''')
        layout = SVG.parse(
            source=q1,
            reify=False,
            ppi=DEFAULT_PPI,
            width=1,
            height=1,
            color="black",
            transform=None,
            context=None
        )

        path1 = layout.get_element_by_id("use1")[0]
        path2 = Path('''M 4448 1489 
C 4454 1508 4474 1554 4474 1579 
C 4474 1611 4448 1643 4410 1643 
C 4384 1643 4371 1637 4352 1617 
C 4339 1611 4339 1598 4282 1469 
C 3904 570 3629 185 2605 185 
L 1670 185 
C 1581 185 1568 185 1530 192 
C 1459 198 1453 211 1453 262 
C 1453 307 1466 345 1478 403 
L 1920 2176 
L 2554 2176 
C 3053 2176 3091 2066 3091 1874 
C 3091 1810 3091 1752 3046 1560 
C 3034 1534 3027 1508 3027 1489 
C 3027 1444 3059 1425 3098 1425 
C 3155 1425 3162 1469 3187 1559 
L 3552 3042 
C 3552 3073 3526 3105 3488 3105 
C 3430 3105 3424 3080 3398 2990 
C 3270 2501 3142 2361 2573 2361 
L 1965 2361 
L 2362 3930 
C 2419 4154 2432 4154 2694 4154 
L 3610 4154 
C 4397 4154 4557 3943 4557 3458 
C 4557 3451 4557 3273 4531 3062 
C 4525 3036 4518 2998 4518 2985 
C 4518 2934 4550 2915 4589 2915 
C 4634 2915 4659 2941 4672 3055 
L 4806 4174 
C 4806 4195 4819 4263 4819 4277 
C 4819 4352 4762 4352 4646 4352 
L 1523 4352 
C 1402 4352 1338 4352 1338 4229 
C 1338 4154 1382 4154 1491 4154 
C 1888 4154 1888 4114 1888 4052 
C 1888 4020 1882 3994 1862 3924 
L 998 473 
C 941 249 928 185 480 185 
C 358 185 294 185 294 70 
C 294 0 333 0 461 0 
L 3674 0 
C 3814 0 3821 6 3866 110 
L 4448 1489 
z''', transform="translate(0, 0) scale(1.333333333333, 1.333333333333) translate(0 21.294961)scale(0.3 -0.3) scale(0.996264) scale(0.015625)")
        self.assertEqual(path1.values["transform"], path2.values["transform"])
        self.assertEqual(path1.transform, path2.transform)
        self.assertEqual(path1, path2)
