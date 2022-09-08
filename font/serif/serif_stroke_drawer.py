from ...vec2 import Vec2
from ...util import normalize
from . serif import Serif
import svgwrite
import svgwrite.path
import numpy as np

class SerifStrokeDrawer:
    @staticmethod
    def __DrawCurveU(font: Serif, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, opt1: int, hane_adjustment, opt3: int, opt4: int):
        pass
    # TODO

    @staticmethod
    def DrawBezier(font: Serif, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, opt1: int, hane_adjustment, opt3: int, opt4: int):
        SerifStrokeDrawer.__DrawCurveU(font, canvas, vec_1, vec_s1, vec_s2, vec_2, a1, a2, opt1, hane_adjustment, opt3, opt4)

    @staticmethod
    def DrawCurve(font: Serif, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s: Vec2, vec_2: Vec2, a1: int, a2: int, opt1: int, hane_adjustment, opt3: int, opt4: int):
        SerifStrokeDrawer.__DrawCurveU(font, canvas, vec_1, vec_s, vec_s, vec_2, a1, a2, opt1, hane_adjustment, opt3, opt4)
    
    @staticmethod
    def DrawLine(font: Serif, canvas: svgwrite.Drawing, vec_1: Vec2, vec_2: Vec2, a1: int, a2: int, opt1: int, uroko_adjustment, kakato_adjustment):
        pass
    # TODO