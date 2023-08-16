import io
import unittest

from svgelements import *


class TestParser(unittest.TestCase):

    def test_svg_examples(self):
        """Examples from the SVG spec"""
        path1 = Path('M 100 100 L 300 100 L 200 300 z')
        self.assertEqual(path1, Path(Move(100 + 100j),
                                     Line(100 + 100j, 300 + 100j),
                                     Line(300 + 100j, 200 + 300j),
                                     Close(200 + 300j, 100 + 100j)))  # CHANGED. Closed object
        self.assertTrue(path1.closed)

        # for Z command behavior when there is multiple subpaths
        path1 = Path('M 0 0 L 50 20 M 100 100 L 300 100 L 200 300 z')
        self.assertEqual(path1, Path(
            Move(0j),
            Line(0 + 0j, 50 + 20j),
            Move(50 + 20j, 100+100j),  # CHANGED. Move knows start position.
            Line(100 + 100j, 300 + 100j),
            Line(300 + 100j, 200 + 300j),
            Close(200 + 300j, 100 + 100j)))  # CHANGED. Closed object

        path1 = Path('M 100 100 L 200 200')
        path2 = Path('M100 100L200 200')
        self.assertEqual(path1, path2)

        path1 = Path('M 100 200 L 200 100 L -100 -200')
        path2 = Path('M 100 200 L 200 100 -100 -200')
        self.assertEqual(path1, path2)

        path1 = Path("""M100,200 C100,100 250,100 250,200
                              S400,300 400,200""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              CubicBezier(100 + 200j, 100 + 100j, 250 + 100j, 250 + 200j),
                              CubicBezier(250 + 200j, 250 + 300j, 400 + 300j, 400 + 200j)))

        path1 = Path('M100,200 C100,100 400,100 400,200')
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              CubicBezier(100 + 200j, 100 + 100j, 400 + 100j, 400 + 200j)))

        path1 = Path('M100,500 C25,400 475,400 400,500')
        self.assertEqual(path1,
                         Path(Move(100 + 500j),
                              CubicBezier(100 + 500j, 25 + 400j, 475 + 400j, 400 + 500j)))

        path1 = Path('M100,800 C175,700 325,700 400,800')
        self.assertEqual(path1,
                         Path(Move(100+800j),
                              CubicBezier(100 + 800j, 175 + 700j, 325 + 700j, 400 + 800j)))

        path1 = Path('M600,200 C675,100 975,100 900,200')
        self.assertEqual(path1,
                         Path(Move(600 + 200j),
                              CubicBezier(600 + 200j, 675 + 100j, 975 + 100j, 900 + 200j)))

        path1 = Path('M600,500 C600,350 900,650 900,500')
        self.assertEqual(path1,
                         Path(Move(600 + 500j),
                              CubicBezier(600 + 500j, 600 + 350j, 900 + 650j, 900 + 500j)))

        path1 = Path("""M600,800 C625,700 725,700 750,800
                              S875,900 900,800""")
        self.assertEqual(path1,
                         Path(Move(600 + 800j),
                              CubicBezier(600 + 800j, 625 + 700j, 725 + 700j, 750 + 800j),
                              CubicBezier(750 + 800j, 775 + 900j, 875 + 900j, 900 + 800j)))

        path1 = Path('M200,300 Q400,50 600,300 T1000,300')
        self.assertEqual(path1,
                         Path(Move(200 + 300j),
                              QuadraticBezier(200 + 300j, 400 + 50j, 600 + 300j),
                              QuadraticBezier(600 + 300j, 800 + 550j, 1000 + 300j)))

        path1 = Path('M300,200 h-150 a150,150 0 1,0 150,-150 z')
        self.assertEqual(path1,
                         Path(Move(300 + 200j),
                              Line(300 + 200j, 150 + 200j),
                              Arc(150 + 200j, 150 + 150j, 0, 1, 0, 300 + 50j),
                              Close(300 + 50j, 300 + 200j)))   # CHANGED. Closed object

        path1 = Path('M275,175 v-150 a150,150 0 0,0 -150,150 z')
        self.assertEqual(path1,
                         Path(Move(275 + 175j),
                              Line(275 + 175j, 275 + 25j),
                              Arc(275 + 25j, 150 + 150j, 0, 0, 0, 125 + 175j),
                              Close(125 + 175j, 275 + 175j)))   # CHANGED. Closed object

        path1 = Path('M275,175 v-150 a150,150 0 0,0 -150,150 L 275,175 z')
        self.assertEqual(path1,
                         Path(Move(275 + 175j),
                              Line(275 + 175j, 275 + 25j),
                              Arc(275 + 25j, 150 + 150j, 0, 0, 0, 125 + 175j),
                              Line(125 + 175j, 275 + 175j),
                              Close(275 + 175j, 275 + 175j)))   # CHANGED. Closed object

        path1 = Path("""M600,350 l 50,-25
                              a25,25 -30 0,1 50,-25 l 50,-25
                              a25,50 -30 0,1 50,-25 l 50,-25
                              a25,75 -30 0,1 50,-25 l 50,-25
                              a25,100 -30 0,1 50,-25 l 50,-25""")
        self.assertEqual(path1,
                         Path(Move(600 + 350j),
                              Line(600 + 350j, 650 + 325j),
                              Arc(650 + 325j, 25 + 25j, -30, 0, 1, 700 + 300j),
                              Line(700 + 300j, 750 + 275j),
                              Arc(750 + 275j, 25 + 50j, -30, 0, 1, 800 + 250j),
                              Line(800 + 250j, 850 + 225j),
                              Arc(850 + 225j, 25 + 75j, -30, 0, 1, 900 + 200j),
                              Line(900 + 200j, 950 + 175j),
                              Arc(950 + 175j, 25 + 100j, -30, 0, 1, 1000 + 150j),
                              Line(1000 + 150j, 1050 + 125j)))

    def test_wc3_examples12(self):
        """
        W3C_SVG_11_TestSuite Paths
        Test using multiple coord sets to build a polybeizer, and implicit values for initial S.
        """
        parse_path = Path

        path12 = parse_path(
            """M  100 100    C  100 20   200 20   200 100   S   300 180   300 100"""
        )
        self.assertEqual(
            path12,
            Path(
                Move(end=(100 + 100j)),
                CubicBezier(
                    start=(100 + 100j),
                    control1=(100 + 20j),
                    control2=(200 + 20j),
                    end=(200 + 100j),
                ),
                CubicBezier(
                    start=(200 + 100j),
                    control1=(200 + 180j),
                    control2=(300 + 180j),
                    end=(300 + 100j),
                ),
            ),
        )

        path12 = parse_path(
            """M  100 250    S  200 200   200 250     300 300   300 250"""
        )
        self.assertEqual(
            path12,
            Path(
                Move(end=(100 + 250j)),
                CubicBezier(
                    start=(100 + 250j),
                    control1=(100 + 250j),
                    control2=(200 + 200j),
                    end=(200 + 250j),
                ),
                CubicBezier(
                    start=(200 + 250j),
                    control1=(200 + 300j),
                    control2=(300 + 300j),
                    end=(300 + 250j),
                ),
            ),
        )

    def test_wc3_examples13(self):
        """
        W3C_SVG_11_TestSuite Paths
        Test multiple coordinates for V and H.
        """
        parse_path = Path
        path13 = parse_path(
            """   M  240.00000  56.00000    H  270.00000         300.00000 320.00000 400.00000   """
        )
        self.assertEqual(
            path13,
            Path(
                Move(end=(240 + 56j)),
                Line(start=(240 + 56j), end=(270 + 56j)),
                Line(start=(270 + 56j), end=(300 + 56j)),
                Line(start=(300 + 56j), end=(320 + 56j)),
                Line(start=(320 + 56j), end=(400 + 56j)),
            ),
        )

        path13 = parse_path(
            """   M  240.00000  156.00000    V  180.00000         200.00000 260.00000 300.00000   """
        )
        self.assertEqual(
            path13,
            Path(
                Move(end=(240 + 156j)),
                Line(start=(240 + 156j), end=(240 + 180j)),
                Line(start=(240 + 180j), end=(240 + 200j)),
                Line(start=(240 + 200j), end=(240 + 260j)),
                Line(start=(240 + 260j), end=(240 + 300j)),
            ),
        )

    def test_wc3_examples14(self):
        """
        W3C_SVG_11_TestSuite Paths
        Test implicit values for moveto. If the first command is 'm' it should be taken as an absolute moveto,
        plus implicit lineto.
        """
        parse_path = Path
        path14 = parse_path(
            """   m   62.00000  56.00000    51.96152   90.00000   -103.92304         0.00000    51.96152  -90.00000   z    m    0.00000   15.00000   38.97114   67.50000   -77.91228         0.00000   38.97114  -67.50000   z  """
        )
        self.assertEqual(
            path14,
            Path(
                Move(end=(62 + 56j)),
                Line(start=(62 + 56j), end=(113.96152000000001 + 146j)),
                Line(
                    start=(113.96152000000001 + 146j), end=(10.038480000000007 + 146j)
                ),
                Line(start=(10.038480000000007 + 146j), end=(62.00000000000001 + 56j)),
                Close(start=(62.00000000000001 + 56j), end=(62 + 56j)),
                Move(start=Point(62,56), end=(62 + 71j)),
                Line(start=(62 + 71j), end=(100.97113999999999 + 138.5j)),
                Line(
                    start=(100.97113999999999 + 138.5j),
                    end=(23.058859999999996 + 138.5j),
                ),
                Line(
                    start=(23.058859999999996 + 138.5j), end=(62.029999999999994 + 71j)
                ),
                Close(start=(62.029999999999994 + 71j), end=(62 + 71j)),
            ),
        )
        path14 = parse_path(
            """   M  177.00000   56.00000    228.96152         146.00000   125.03848  146.00000    177.00000   56.00000   Z    M  177.00000  71.00000   215.97114         138.50000   138.02886  138.50000   177.00000  71.00000   Z  """
        )

        self.assertEqual(
            path14,
            Path(
                Move(end=(177 + 56j)),
                Line(start=(177 + 56j), end=(228.96152 + 146j)),
                Line(start=(228.96152 + 146j), end=(125.03848 + 146j)),
                Line(start=(125.03848 + 146j), end=(177 + 56j)),
                Close(start=(177 + 56j), end=(177 + 56j)),
                Move(start=Point(177,56), end=(177 + 71j)),
                Line(start=(177 + 71j), end=(215.97114 + 138.5j)),
                Line(start=(215.97114 + 138.5j), end=(138.02886 + 138.5j)),
                Line(start=(138.02886 + 138.5j), end=(177 + 71j)),
                Close(start=(177 + 71j), end=(177 + 71j)),
            ),
        )

    def test_wc3_examples15(self):
        """
        W3C_SVG_11_TestSuite Paths
        'M' or 'm' command with more than one pair of coordinates are absolute
        if the moveto was specified with 'M' and relative if the moveto was
        specified with 'm'.
        """
        parse_path = Path
        path15 = parse_path("""M100,120 L160,220 L40,220 z""")
        self.assertEqual(
            path15,
            Path(
                Move(end=(100 + 120j)),
                Line(start=(100 + 120j), end=(160 + 220j)),
                Line(start=(160 + 220j), end=(40 + 220j)),
                Close(start=(40 + 220j), end=(100 + 120j)),
            ),
        )
        path15 = parse_path("""M350,120 L410,220 L290,220 z""")
        self.assertEqual(
            path15,
            Path(
                Move(end=(350 + 120j)),
                Line(start=(350 + 120j), end=(410 + 220j)),
                Line(start=(410 + 220j), end=(290 + 220j)),
                Close(start=(290 + 220j), end=(350 + 120j)),
            ),
        )
        path15 = parse_path("""M100,120 160,220 40,220 z""")
        self.assertEqual(
            path15,
            Path(
                Move(end=(100 + 120j)),
                Line(start=(100 + 120j), end=(160 + 220j)),
                Line(start=(160 + 220j), end=(40 + 220j)),
                Close(start=(40 + 220j), end=(100 + 120j)),
            ),
        )
        path15 = parse_path("""m350,120 60,100 -120,0 z""")
        self.assertEqual(
            path15,
            Path(
                Move(end=(350 + 120j)),
                Line(start=(350 + 120j), end=(410 + 220j)),
                Line(start=(410 + 220j), end=(290 + 220j)),
                Close(start=(290 + 220j), end=(350 + 120j)),
            ),
        )

    def test_wc3_examples17(self):
        """
        W3C_SVG_11_TestSuite Paths
        Test that the 'z' and 'Z' command have the same effect.
        """
        parse_path = Path
        path17 = parse_path("""M 50 50 L 50 150 L 150 150 L 150 50 z""")
        self.assertEqual(
            path17,
            Path(
                Move(end=(50 + 50j)),
                Line(start=(50 + 50j), end=(50 + 150j)),
                Line(start=(50 + 150j), end=(150 + 150j)),
                Line(start=(150 + 150j), end=(150 + 50j)),
                Close(start=(150 + 50j), end=(50 + 50j)),
            ),
        )
        path17 = parse_path("""M 50 50 L 50 150 L 150 150 L 150 50 Z""")
        self.assertEqual(
            path17,
            Path(
                Move(end=(50 + 50j)),
                Line(start=(50 + 50j), end=(50 + 150j)),
                Line(start=(50 + 150j), end=(150 + 150j)),
                Line(start=(150 + 150j), end=(150 + 50j)),
                Close(start=(150 + 50j), end=(50 + 50j)),
            ),
        )
        path17 = parse_path("""M 250 50 L 250 150 L 350 150 L 350 50 Z""")
        self.assertEqual(
            path17,
            Path(
                Move(end=(250 + 50j)),
                Line(start=(250 + 50j), end=(250 + 150j)),
                Line(start=(250 + 150j), end=(350 + 150j)),
                Line(start=(350 + 150j), end=(350 + 50j)),
                Close(start=(350 + 50j), end=(250 + 50j)),
            ),
        )

        path17 = parse_path("""M 250 50 L 250 150 L 350 150 L 350 50 z""")
        self.assertEqual(
            path17,
            Path(
                Move(end=(250 + 50j)),
                Line(start=(250 + 50j), end=(250 + 150j)),
                Line(start=(250 + 150j), end=(350 + 150j)),
                Line(start=(350 + 150j), end=(350 + 50j)),
                Close(start=(350 + 50j), end=(250 + 50j)),
            ),
        )

    def test_wc3_examples18(self):
        """
        W3C_SVG_11_TestSuite Paths
        The 'path' element's 'd' attribute ignores additional whitespace, newline characters, and commas,
        and BNF processing consumes as much content as possible, stopping as soon as a character that doesn't
        satisfy the production is encountered.
        """
        parse_path = Path
        path18a = parse_path("""M 20 40 H 40""")
        path18b = parse_path(
            """M 20 40
                 H 40"""
        )
        self.assertEqual(path18a, path18b)
        path18a = parse_path("""M 20 60 H 40""")
        path18b = parse_path(
            """
                  M
                  20
                  60
                  H
                  40
                  """
        )
        self.assertEqual(path18a, path18b)
        path18a = parse_path("""M 20 80 H40""")
        path18b = parse_path("""M       20,80          H    40""")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("""M 20 100 H 40#90""")
        path18b = parse_path("""M 20 100 H 40""")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("""M 20 120 H 40.5 0.6""")
        path18b = parse_path("""M 20 120 H 40.5.6""")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("""M 20 140 h 10 -20""")
        path18b = parse_path("""M 20 140 h 10-20""")
        self.assertEqual(path18a, path18b)
        path18a = parse_path("""M 20 160 H 40""")
        path18b = parse_path("""M 20 160 H 40#90""")
        self.assertEqual(path18a, path18b)

    def test_wc3_examples19(self):
        """
        W3C_SVG_11_TestSuite Paths
        Test that additional parameters to pathdata commands are treated as additional calls to the most recent command.
        """
        parse_path = Path
        path19a = parse_path("""M20 20 H40 H60""")
        path19b = parse_path("""M20 20 H40 60""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M20 40 h20 h20""")
        path19b = parse_path("""M20 40 h20 20""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M120 20 V40 V60""")
        path19b = parse_path("""M120 20 V40 60""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M140 20 v20 v20""")
        path19b = parse_path("""M140 20 v20 20""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M220 20 L 240 20 L260 20""")
        path19b = parse_path("""M220 20 L 240 20 260 20 """)
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M220 40 l 20 0 l 20 0""")
        path19b = parse_path("""M220 40 l 20 0 20 0""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M50 150 C50 50 200 50 200 150 C200 50 350 50 350 150""")
        path19b = parse_path("""M50 150 C50 50 200 50 200 150 200 50 350 50 350 150""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path(
            """M50, 200 c0,-100 150,-100 150,0 c0,-100 150,-100 150,0"""
        )
        path19b = parse_path(
            """M50, 200 c0,-100 150,-100 150,0 0,-100 150,-100 150,0"""
        )
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M50 250 S125 200 200 250 S275, 200 350 250""")
        path19b = parse_path("""M50 250 S125 200 200 250 275, 200 350 250""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M50 275 s75 -50 150 0 s75, -50 150 0""")
        path19b = parse_path("""M50 275 s75 -50 150 0 75, -50 150 0""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M50 300 Q 125 275 200 300 Q 275 325 350 300""")
        path19b = parse_path("""M50 300 Q 125 275 200 300 275 325 350 300""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M50 325 q 75 -25 150 0 q 75 25 150 0""")
        path19b = parse_path("""M50 325 q 75 -25 150 0 75 25 150 0""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M425 25 T 425 75 T 425 125""")
        path19b = parse_path("""M425 25 T 425 75 425 125""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M450 25 t 0 50 t 0 50""")
        path19b = parse_path("""M450 25 t 0 50 0 50""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M400,200 A25 25 0 0 0 425 150 A25 25 0 0 0 400 200""")
        path19b = parse_path("""M400,200 A25 25 0 0 0 425 150 25 25 0 0 0 400 200""")
        self.assertEqual(path19a, path19b)
        path19a = parse_path("""M400,300 a25 25 0 0 0 25 -50 a25 25 0 0 0 -25 50""")
        path19b = parse_path("""M400,300 a25 25 0 0 0 25 -50 25 25 0 0 0 -25 50""")
        self.assertEqual(path19a, path19b)

    def test_wc3_examples20(self):
        """
        W3C_SVG_11_TestSuite Paths
        Tests parsing of the elliptical arc path syntax.
        """
        parse_path = Path
        path20a = parse_path("""M120,120 h25 a25,25 0 1,0 -25,25 z""")
        path20b = parse_path("""M120,120 h25 a25,25 0 10 -25,25z""")
        self.assertEqual(path20a, path20b)
        path20a = parse_path("""M200,120 h-25 a25,25 0 1,1 25,25 z""")
        path20b = parse_path("""M200,120 h-25 a25,25 0 1125,25 z""")
        self.assertEqual(path20a, path20b)
        path20a = parse_path("""M280,120 h25 a25,25 0 1,0 -25,25 z""")
        self.assertRaises(Exception, 'parse_path("""M280,120 h25 a25,25 0 6 0 -25,25 z""")')
        path20a = parse_path("""M360,120 h-25 a25,25 0 1,1 25,25 z""")
        self.assertRaises(Exception, 'parse_path("""M360,120 h-25 a25,25 0 1 -1 25,25 z""")')
        path20a = parse_path("""M120,200 h25 a25,25 0 1,1 -25,-25 z""")
        path20b = parse_path("""M120,200 h25 a25,25 0 1 1-25,-25 z""")
        self.assertEqual(path20a, path20b)
        path20a = parse_path("""M200,200 h-25 a25,25 0 1,0 25,-25 z""")
        self.assertRaises(Exception, 'parse_path("""M200,200 h-25 a25,2501 025,-25 z""")')
        path20a = parse_path("""M280,200 h25 a25,25 0 1,1 -25,-25 z""")
        self.assertRaises(Exception, 'parse_path("""M280,200 h25 a25 25 0 1 7 -25 -25 z""")')
        path20a = parse_path("""M360,200 h-25 a25,25 0 1,0 25,-25 z""")
        self.assertRaises(Exception, 'parse_path("""M360,200 h-25 a25,25 0 -1 0 25,-25 z""")')

    def test_others(self):
        # Other paths that need testing:

        # Relative moveto:
        path1 = Path('M 0 0 L 50 20 m 50 80 L 300 100 L 200 300 z')
        self.assertEqual(path1, Path(
            Move(0j),
            Line(0 + 0j, 50 + 20j),
            Move(50 + 20j, 100 + 100j),  # CHANGED. Path saves the start point if it knows it.
            Line(100 + 100j, 300 + 100j),
            Line(300 + 100j, 200 + 300j),
            Close(200 + 300j, 100 + 100j)))  # CHANGED. This is a Close object now.

        # Initial smooth and relative CubicBezier
        path1 = Path("""M100,200 s 150,-100 150,0""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              CubicBezier(100 + 200j, 100 + 200j, 250 + 100j, 250 + 200j)))

        # Initial smooth and relative QuadraticBezier
        path1 = Path("""M100,200 t 150,0""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              QuadraticBezier(100 + 200j, 100 + 200j, 250 + 200j)))

        # Relative QuadraticBezier
        path1 = Path("""M100,200 q 0,0 150,0""")
        self.assertEqual(path1,
                         Path(Move(100 + 200j),
                              QuadraticBezier(100 + 200j, 100 + 200j, 250 + 200j)))

    def test_negative(self):
        """You don't need spaces before a minus-sign"""
        path1 = Path('M100,200c10-5,20-10,30-20')
        path2 = Path('M 100 200 c 10 -5 20 -10 30 -20')
        self.assertEqual(path1, path2)

    def test_numbers(self):
        """Exponents and other number format cases"""
        # It can be e or E, the plus is optional, and a minimum of +/-3.4e38 must be supported.
        path1 = Path('M-3.4e38 3.4E+38L-3.4E-38,3.4e-38')
        path2 = Path(Move(-3.4e+38 +  3.4e+38j), Line(-3.4e+38 + 3.4e+38j, -3.4e-38 + 3.4e-38j))
        self.assertEqual(path1, path2)

    def test_errors(self):
        self.assertRaises(ValueError, Path, 'M 100 100 L 200 200 Z 100 200')

    def test_non_path(self):
        # It's possible in SVG to create paths that has zero length,
        # we need to handle that.

        path = Path("M10.236,100.184")
        self.assertEqual(path.d(), 'M 10.236,100.184')

    def test_issue_47(self):
        arc_path_declared = Path(Move(0 + 25j), Arc(0 + 25j, 25 + 25j, 0.0, 0, 0, 0 - 25j))
        arc_path_parsed = Path('M 0 25 A25,25 0.0 0 0 0,-25')
        arc_path_parsed_scaled = Path('M 0 25 A1,1 0.0 0 0 0,-25')
        self.assertEqual(arc_path_declared, arc_path_parsed)
        self.assertEqual(arc_path_parsed_scaled, arc_path_declared)

    def test_svg_parse(self):
        s = io.StringIO(u'''<svg><path d="M0,0 L1,0 z"/></svg>''')
        svg = SVG.parse(s)
        for e in svg.elements():
            if isinstance(e, Path):
                self.assertEqual(e, "M0,0 L1,0 z")

    def test_svg_parse_group(self):
        s = io.StringIO(u'''<svg>
                        <g transform="scale(10,10)" vector-effect="non-scaling-stroke">
                        <path d="M0,0 L1,0 z"/>
                        </g>
                        </svg>''')
        svg = SVG.parse(s)
        for e in svg.elements():
            if isinstance(e, Path):
                self.assertEqual(e, "M0,0 L10,0 z")

    def test_svg_parse_group_2(self):
        s = io.StringIO(u'''<svg><g><path d="M0,0 L1,0 z"/><path d="M0,0 L1,0 z"/></g></svg>''')
        svg = SVG.parse(s)
        for e in svg.elements():
            if isinstance(e, Path):
                self.assertEqual(e, "M0,0 L1,0 z")

    def test_solo_move(self):
        move_only = Path("M0,0")
        self.assertEqual(move_only.point(0), 0 + 0j)
        self.assertEqual(move_only.point(0.5), 0 + 0j)
        self.assertEqual(move_only.point(1), 0 + 0j)
        self.assertEqual(move_only.length(), 0)

        move_onlyz = Path("M0,0Z")
        self.assertEqual(move_onlyz.point(0), 0 + 0j)
        self.assertEqual(move_onlyz.point(0.5), 0 + 0j)
        self.assertEqual(move_onlyz.point(1), 0 + 0j)
        self.assertEqual(move_onlyz.length(), 0)

        move_2_places = Path("M0,0M1,1")
        self.assertEqual(move_2_places.point(0), 0 + 0j)
        self.assertEqual(move_2_places.point(0.49), 0 + 0j)
        self.assertEqual(move_2_places.point(0.51), 1 + 1j)
        self.assertEqual(move_2_places.point(1), 1 + 1j)
        self.assertEqual(move_2_places.length(), 0)

    def test_fill_opacity_fill_none(self):
        s = io.StringIO(u'''<svg><path d="M0,0 H10 V10 H0 z" fill-opacity="1" fill="none" /></svg>''')
        svg = SVG.parse(s)
        for e in svg.elements():
            if isinstance(e, Path):
                self.assertEqual(e, "M0,0 H10 V10 H0 z")
                self.assertEqual(e.fill, "none" )


class TestParseDisplay(unittest.TestCase):
    """
    Tests for the parsing of displayed objects within an svg for conforming to the spec. Anything with a viewbox that
    has a zero width or zero height is not rendered. Any svg with a zero height or zero width is not rendered. Anything
    with a display="none" is not rendered whether this property comes from class, style, or direct attribute. Items with
    visibility="hidden" are rendered and returned but should be hidden by the end user.
    """

    def test_svgfile(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g style="display:inline">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertTrue(isinstance(q[-1], SimpleLine))

    def test_svgfile_no_root_issue175(self):
        """
        SVG files loaded without a valid root element crash. Issue 175.
        """
        q = io.StringIO(u'''<g/>''')
        m = SVG.parse(q)
        self.assertTrue(isinstance(m, Group))
        q = io.StringIO(u'''<path d="M0,0z"/>''')
        m = SVG.parse(q)
        self.assertTrue(isinstance(m, Path))
        q = io.StringIO(u'''<g><path d="M0,0z"/></g>''')
        m = SVG.parse(q)
        self.assertTrue(isinstance(m, Group))
        self.assertTrue(isinstance(m[0], Path))

    def test_svgfile_0_width(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g style="display:inline">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_0_height(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g style="display:inline">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_viewbox_0_height(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 0" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g style="display:inline">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_viewbox_0_width(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 0 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g style="display:inline">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertFalse(isinstance(q[-1], SimpleLine))

    def test_svgfile_display_none_inline(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g style="display:none">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')

        m = SVG.parse(q)
        e = list(m.elements())
        self.assertFalse(isinstance(e[-1], SimpleLine))

        q.seek(0)
        m = SVG.parse(q, parse_display_none=True)
        e = list(m.elements())
        self.assertTrue(isinstance(e[-1], SimpleLine))

    def test_svgfile_display_none_attribute(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g display="none">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        e = list(m.elements())
        self.assertFalse(isinstance(e[-1], SimpleLine))

        q.seek(0)
        m = SVG.parse(q, parse_display_none=True)
        e = list(m.elements())
        self.assertTrue(isinstance(e[-1], SimpleLine))

    def test_svgfile_display_mixed(self):
        """
        All children of a display="none" are excluded, even if they override that display.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g display="none">
                        <line display="show" x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        e = list(m.elements())
        self.assertFalse(isinstance(e[-1], SimpleLine))

        q.seek(0)
        m = SVG.parse(q, parse_display_none=True)
        e = list(m.elements())
        self.assertTrue(isinstance(e[-1], SimpleLine))

    def test_svgfile_display_none_class(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <style type="text/css">\n
                        .hide { \n
                             display:none;\n
                        }\n
                        </style>\n
                        <g class="hide">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        e = list(m.elements())
        self.assertFalse(isinstance(e[-1], SimpleLine))

        q.seek(0)
        m = SVG.parse(q, parse_display_none=True)
        e = list(m.elements())
        self.assertTrue(isinstance(e[-1], SimpleLine))

    def test_svgfile_display_None_class(self):
        """
        display:None is css and not svg it is case insensitive
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <style type="text/css">\n
                        .hide { \n
                             display:None;\n
                        }\n
                        </style>\n
                        <g class="hide">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        e = list(m.elements())
        self.assertFalse(isinstance(e[-1], SimpleLine))

        q.seek(0)
        m = SVG.parse(q, parse_display_none=True)
        e = list(m.elements())
        self.assertTrue(isinstance(e[-1], SimpleLine))

    def test_svgfile_visibility_hidden(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <g style="visibility:hidden">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        e = list(m.elements())
        self.assertTrue(isinstance(e[-1], SimpleLine))  # Hidden elements still exist.

        q.seek(0)
        m = SVG.parse(q, parse_display_none=True)
        e = list(m.elements())
        self.assertTrue(isinstance(e[-1], SimpleLine))  # forcing none does not affect


class TestParseDefUse(unittest.TestCase):
    """
    Tests for Def and Use within an svg file. These must work with the definitions used within the SVG spec. This means
    that use objects must be replaced with their pure tree forms as if they are children of the use flag in question.
    """

    def test_struct_use_01(self):
        """
        The purpose of this test is to validate proper handling of
        the use element. In particular, the test checks the proper inheritance
        of properties through the shadow tree (rather than through the document
        tree).
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="100%" height="100%" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <defs>
                            <g fill="red" stroke="yellow" stroke-width="3">
                                <rect id="usedRect" width="20" height="20"/>
                                <circle id="usedCircle" cx="10" cy="10" r="10"/>
                                <ellipse id="usedEllipse" cx="10" cy="10" rx="10" ry="10"/>
                                <line id="usedLine" x1="0" y1="10" x2="20" y2="10"/>
                                <path id="usedPath" d="M 0 0 L 20 0 L 20 20 L 0 20 Z"/>
                                <polygon id="usedPolygon" points="0,0 20,0 20,20 0,20 0 0"/>
                                <polyline id="usedPolyline" points="0,0 20,0 20,20"/>
                                <g id="usedG">
                                    <rect width="10" height="20"/>
                                    <rect id="half_green" x="10" width="10" height="20" fill="rgb(0,128,0)"/>
                                </g>
                                <use id="usedUse" xlink:href="#usedRect"/>
                                <text id="usedText">Text</text>
                            </g>
                        </defs>
                        <g transform="translate(150, 25)">
                            <use xlink:href="#usedRect" fill="#0F0"/>
                            <use y="30" xlink:href="#usedCircle" fill="#0F0"/>
                            <use y="60" xlink:href="#usedEllipse" fill="#0F0"/>
                            <use y="90" xlink:href="#usedLine" stroke="#0F0" stroke-width="2"/>
                            <use y="120" xlink:href="#usedPolyline" stroke="#0F0" stroke-width="2" fill="none"/>
                            <use y="150" xlink:href="#usedPolygon" fill="#0F0"/>
                            <use y="180" xlink:href="#usedPath" fill="#0F0"/>
                            <use x="180" y="0" xlink:href="#usedG" fill="#0F0"/>
                            <use x="180" y="30" xlink:href="#usedUse" fill="#0F0"/>
                            <use y="260" xlink:href="#usedText" fill="#0F0"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        for element in q:
            try:
                ident = element.id
                fill = element.fill
                stroke = element.stroke
                if ident == "half_green":
                    self.assertEqual('#008000', fill)  # Half green rectangle within used group.
                elif ident == "usedLine":
                    self.assertEqual('#0F0', stroke)
                elif ident == "usedPolyline":
                    self.assertEqual('#0F0', stroke)
                else:
                    self.assertEqual('#0F0', fill)  # Remaining are filled green.

            except AttributeError:
                pass

    def test_struct_defs_ignored(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                            <defs>
                                <g>
                                    <rect x="100" y="100" width="100" height="100" />
                                    <circle cx="100" cy="100" r="100" />
                                </g>
                            </defs>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertEqual(len(q), 1)

    def test_struct_use_unlinked(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <use href="garbage_address"/>
                        </svg>''')
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertEqual(len(q), 2)

    def test_parse_conditional_issue_114(self):
        import io
        from svgelements import SVG, Path

        svg_str = io.StringIO("""<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
         width="500" height="500" viewBox="0 0 500 500" preserveAspectRatio="xMidYMid meet">
         <path d="M50 150 C50 50 200 50 200 150 C200 50 350 50 350 150 z"/>
         <path d="M350 250 C50 50 200 50 200 150 C200 50 350 50 350 150 z"/> 
        </svg>""")

        for s in SVG.parse(svg_str).elements(conditional=lambda el: isinstance(el, Path)):
            self.assertEqual(type(s), Path)

    def test_style_concat_issue_180(self):
        """
        Test to verify that a CSS stylesheet variable that does not end with a `;` is properly combined with the
        per attribute and inherited values.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <style type="text/css" >
                          <![CDATA[
                            line {
                               stroke: #006600
                            }
                          ]]>
                        </style>
                        <g style="stroke:red">
                        <line x1="0.0" x2="0.0" y1="0.0" y2="100" style="stroke:blue"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q)
        line = list(m.elements(conditional=lambda el: isinstance(el, Shape)))[0]
        self.assertIsInstance(line, SimpleLine)
        self.assertEqual(line.stroke, "blue")

    def test_font_bolder_parsing(self):
        """
        Test to verify that a CSS stylesheet variable that does not end with a `;` is properly combined with the
        per attribute and inherited values.
        """
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="3.0cm" height="3.0cm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <text font-weight="bolder"> Bolder would crash. </text>
                        </svg>''')
        m = SVG.parse(q)
        line = list(m.elements(conditional=lambda el: isinstance(el, Text)))[0]
        self.assertIsInstance(line, Text)
        self.assertEqual(line.font_weight, "bolder")

    def test_parse_error_issue_217_stop(self):
        block = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                        xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <path d="M10,10 L20,20 L NaN NaN"/>
                        <path d="M20,10 L20,20"/>
                        </svg>''')

        m = SVG.parse(block, on_error="stop")
        q = list(m.elements())
        self.assertEqual(2, len(q))
        self.assertTrue(isinstance(q[-1], Path))
        self.assertEqual("M 10,10 L 20,20", q[-1].d())

    def test_parse_error_issue_217_raises(self):
        block = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                                xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                                <path d="M10,10 L20,20 L NaN NaN"/>
                                <path d="M20,10 L20,20"/>
                                </svg>''')
        self.assertRaises(ValueError, lambda: SVG.parse(block, on_error="raise"))

    def test_parse_error_issue_217_ignore(self):
        block = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" 
                                xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
                                <path d="M10,10 L20,20 L NaN NaN"/>
                                <path d="M20,10 L20,20"/>
                                </svg>''')

        m = SVG.parse(block)
        q = list(m.elements())
        self.assertEqual(3, len(q))
