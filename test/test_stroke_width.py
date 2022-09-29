import io
import unittest

from svgelements import *


class TestStrokeWidth(unittest.TestCase):
    """Tests the functionality of the Stroke-Width values"""

    def test_viewport_scaling_stroke(self):
        """
        See Issue #199

        The stroke width of both objects here is the same and there is no scaling on the path itself. However, the
        viewport is scaled and applies that scaling to the overall result. Given that these two objects should have
        if drawn in a static fashion the same size stroke. They should not scale based on the viewport since that
        governs a sort of zoom and pan functionality which can be taken as equal to stroke but not in regard to
        vector-effect="non-scaling-stroke".
        """
        q = io.StringIO(
            """<svg version="1.1" xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:ev="http://www.w3.org/2001/xml-events"
            width="335.0mm" height="215.0mm" viewBox="0 0 1266 8130">
            <path d="M 288.706174886,349.064235392 A 113.386,75.5906 0 0,1 175.320348114,424.654786573 A 113.386,75.5906 0 0,1 61.9345213427,349.064235392 A 113.386,75.5906 0 0,1 175.320348114,273.473684211 A 113.386,75.5906 0 0,1 288.706174886,349.064235392 Z" type="elem ellipse" id="meerk40t:15"
            vector-effect="non-scaling-stroke"
            fill-rule="evenodd" stroke="#ff0000" stroke-width="18.897637795275593px" fill="none" />
            <path d="M 302.362204724,151.181102362 A 113.386,75.5906 0 0,1 188.976377953,226.771653543 A 113.386,75.5906 0 0,1 75.5905511811,151.181102362 A 113.386,75.5906 0 0,1 188.976377953,75.5905511811 A 113.386,75.5906 0 0,1 302.362204724,151.181102362 Z" type="elem ellipse" id="meerk40t:18"
            fill-rule="evenodd" stroke="#0000ff" stroke-width="18.897637795275593px" fill="none" />
            </svg>
            """
        )
        m = SVG.parse(q)
        q = list(m.elements())
        self.assertAlmostEqual(q[1].stroke_width, q[2].stroke_width)
