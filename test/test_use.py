import io
import unittest

from svgelements import *


class TestElementUse(unittest.TestCase):

    def test_use_bbox_method(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0, 0, 100, 100" height="100" width="100"
                             xmlns:xlink="http://www.w3.org/1999/xlink">
                            <use x="0" y="0" xlink:href="#rect1234"/>
                            <use x="20" y="20" xlink:href="#rect1234"/>
                            <defs>
                                <rect id="rect1234" x="0" y="20" width="50" height="50"/>
                            </defs>
                        </svg>''')
        svg = SVG.parse(q)
        use = list(svg.select(lambda e: isinstance(e, Use)))
        self.assertEqual(2, len(use))
        self.assertEqual((0.0, 20.0, (0.0 + 50.0), (20.0 + 50.0)), use[0].bbox())
        self.assertEqual((20.0 + 0.0, 20.0 + 20.0, (20.0 + 50.0), (20.0 + 20.0 + 50.0)), use[1].bbox())

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
z''', transform="translate(0, 0) scale(1.333333333333, 1.333333333333) translate(0 21.294961) scale(0.3 -0.3) scale(0.996264) scale(0.015625)")
        self.assertEqual(path1.values["transform"], path2.values["transform"])
        self.assertEqual(path1.transform, path2.transform)
        self.assertEqual(path1, path2)

    def test_issue_170(self):
        """
        Rendered wrongly since the x and y values do not get applied correctly to the use in question.
        """

        q1 = io.StringIO(u'''<?xml version='1.0' encoding='UTF-8'?>
<!-- This file was generated by dvisvgm 2.11.1 -->
<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='30.033152pt' height='6.789661pt' viewBox='85.143591 -71.954169 30.033152 6.789661'>
<defs>
<path id='g4-65' d='M5.378384 0L5.427878-.239223L5.114414-.26397C4.858693-.288717 4.825697-.404204 4.784452-.742415L4.174022-5.708346H3.588339L2.202498-3.274875C1.781796-2.540709 1.097124-1.3116 .791909-.816656C.52794-.387706 .387706-.296966 .131985-.272219L-.140234-.239223L-.189728 0H1.666309L1.715803-.239223L1.262105-.280468C1.097124-.296966 1.080626-.412453 1.154868-.585683C1.427087-1.113622 1.699305-1.649811 2.00452-2.202498H3.852309L4.042037-.602181C4.066784-.362958 4.000792-.296966 3.835811-.280468L3.398611-.239223L3.349116 0H5.378384ZM3.811063-2.515962H2.169501C2.606701-3.332618 3.060399-4.141026 3.505848-4.941184H3.522346L3.811063-2.515962Z'/>
<use id='g6-65' xlink:href='#g3-65' transform='scale(1.166668)'/>
<path id='g3-65' d='M5.361886 0V-.239223C4.883441-.280468 4.792701-.305215 4.644218-.734166L2.895418-5.708346H2.284988L1.418837-3.266626C1.163117-2.548958 .816656-1.559071 .52794-.808407C.354709-.362958 .280468-.26397-.239223-.239223V0H1.57557V-.239223L1.146619-.280468C.899147-.305215 .8744-.387706 .940392-.61043C1.080626-1.105373 1.253856-1.616815 1.443585-2.202498H3.291373L3.84406-.626928C3.92655-.387706 3.885305-.296966 3.621335-.272219L3.250128-.239223V0H5.361886ZM3.192384-2.515962H1.550822C1.814792-3.340867 2.103509-4.149275 2.350981-4.875191H2.375728L3.192384-2.515962Z'/>
</defs>
<g id='page1'>
<use x='85.143591' y='-65.164508' xlink:href='#g4-65'/>
<use x='90.669586' y='-65.164508' xlink:href='#g6-65'/>
<use x='96.801578' y='-65.164508' xlink:href='#g6-65'/>
<use x='102.93357' y='-65.164508' xlink:href='#g6-65'/>
<use x='109.065562' y='-65.164508' xlink:href='#g6-65'/>
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
        elements = list(layout.elements(lambda e: isinstance(e, Path)))
        for i in range(2, len(elements)):
            self.assertEqual(elements[i-1].d(transformed=False), elements[i].d(transformed=False))
            self.assertNotEqual(elements[i - 1].transform, elements[i].transform)
            self.assertNotEqual(elements[i-1], elements[i])
