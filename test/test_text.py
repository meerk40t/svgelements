import io
import time
import unittest

from svgelements import *


class TestElementText(unittest.TestCase):
    def test_issue_157(self):
        q = io.StringIO(
            """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
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
        """
        )
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertIsNotNone(q[1].id)  # Group
        self.assertIsNotNone(q[2].id)  # Text
        self.assertIsNotNone(q[3].id)  # TSpan

    def test_shorthand_fontproperty_1(self):
        font = "12pt/14pt sans-serif"

        q = io.StringIO(
            f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg>
            <text
               font="{font}"
               id="textobject">Shorthand</text>
        </svg>
        """
        )
        m = SVG.parse(q)
        text_object = list(m.elements())[1]
        self.assertEqual(text_object.font_style, "normal")
        self.assertEqual(text_object.font_variant, 'normal')
        self.assertEqual(text_object.font_weight, 400)  # Normal
        self.assertEqual(text_object.font_stretch, "normal")
        self.assertEqual(text_object.font_size, "12pt")
        self.assertEqual(text_object.line_height, "14pt")
        self.assertEqual(text_object.font_family, "sans-serif")
        self.assertEqual(text_object.family_name, None)
        self.assertEqual(text_object.generic_family, "sans-serif")

    def test_shorthand_fontproperty_2(self):
        font = "80% sans-serif"

        q = io.StringIO(
            f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg>
            <text
               font="{font}"
               id="textobject">Shorthand</text>
        </svg>
        """
        )
        m = SVG.parse(q)
        text_object = list(m.elements())[1]
        self.assertEqual(text_object.font_style, 'normal')
        self.assertEqual(text_object.font_variant, 'normal')
        self.assertEqual(text_object.font_weight, 400)  # Normal
        self.assertEqual(text_object.font_stretch, "normal")
        self.assertEqual(text_object.font_size, "80%")
        self.assertEqual(text_object.line_height, "normal")
        self.assertEqual(text_object.font_family, "sans-serif")
        self.assertEqual(text_object.family_name, None)
        self.assertEqual(text_object.generic_family, "sans-serif")

    def test_shorthand_fontproperty_3(self):
        font = 'x-large/110% "new century schoolbook", serif'

        q = io.StringIO(
            f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg>
            <text
               font="{font}"
               id="textobject">Shorthand</text>
        </svg>
        """
        )
        m = SVG.parse(q)
        text_object = list(m.elements())[1]
        self.assertEqual(text_object.font_style, "normal")
        self.assertEqual(text_object.font_variant, 'normal')
        self.assertEqual(text_object.font_weight, 400)  # Normal
        self.assertEqual(text_object.font_stretch, "normal")
        self.assertEqual(text_object.font_size, "x-large")
        self.assertEqual(text_object.line_height, "110%")
        self.assertEqual(text_object.font_family, '"new century schoolbook", serif')
        self.assertEqual(text_object.family_name, 'new century schoolbook')
        self.assertEqual(text_object.generic_family, "serif")

    def test_shorthand_fontproperty_4(self):
        font = "bold italic large Palatino, serif"

        q = io.StringIO(
            f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg>
            <text
               font="{font}"
               id="textobject">Shorthand</text>
        </svg>
        """
        )
        m = SVG.parse(q)
        text_object = list(m.elements())[1]

        self.assertEqual(text_object.font_style, "italic")
        self.assertEqual(text_object.font_variant, 'normal')
        self.assertEqual(text_object.font_weight, "bold")  # Normal
        self.assertEqual(text_object.font_stretch, "normal")
        self.assertEqual(text_object.font_size, "large")
        self.assertEqual(text_object.line_height, "normal")
        self.assertEqual(text_object.font_family, 'Palatino, serif')
        self.assertEqual(text_object.family_name, "Palatino")
        self.assertEqual(text_object.generic_family, "serif")

    def test_shorthand_fontproperty_5(self):
        font = "normal small-caps 120%/120% fantasy"

        q = io.StringIO(
            f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg>
            <text
               font="{font}"
               id="textobject">Shorthand</text>
        </svg>
        """
        )
        m = SVG.parse(q)
        text_object = list(m.elements())[1]
        self.assertEqual(text_object.font_style, "normal")
        self.assertEqual(text_object.font_variant, 'small-caps')
        self.assertEqual(text_object.font_weight, 400)  # Normal
        self.assertEqual(text_object.font_stretch, "normal")
        self.assertEqual(text_object.font_size, "120%")
        self.assertEqual(text_object.line_height, "120%")
        self.assertEqual(text_object.font_family, 'fantasy')
        self.assertEqual(text_object.family_name, None)
        self.assertEqual(text_object.generic_family, "fantasy")

    def test_shorthand_fontproperty_6(self):
        font = ('condensed oblique 12pt "Helvetica Neue", serif;',)

        q = io.StringIO(
            f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg>
            <text
               font="{font}"
               id="textobject">Shorthand</text>
        </svg>
        """
        )
        m = SVG.parse(q)
        text_object = list(m.elements())[1]
        self.assertEqual(text_object.font_style, 'oblique')
        self.assertEqual(text_object.font_variant, 'normal')
        self.assertEqual(text_object.font_weight, 400)  # Normal
        self.assertEqual(text_object.font_stretch, "condensed")
        self.assertEqual(text_object.font_size, "12pt")
        self.assertEqual(text_object.line_height, "normal")
        self.assertEqual(text_object.font_family, '"Helvetica Neue", serif')
        self.assertEqual(text_object.family_name, "Helvetica Neue")
        self.assertEqual(text_object.generic_family, "serif")

    def test_issue_154(self):
        font = "normal " * 12
        q = io.StringIO(
            f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg>
    <text
       font="{font}"
       id="textobject">reDoS</text>
</svg>
        """
        )
        t = time.time()
        m = SVG.parse(q)
        q = list(m.elements())
        t2 = time.time()
        print(f"{t} {t2} d:{t2-t}")
        self.assertFalse(time.time() - t < 1000)
