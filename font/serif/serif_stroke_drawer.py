from ...vec2 import Vec2
from ...util import normalize
from . serif import Serif
import svgwrite
import svgwrite.path
import numpy as np

class SerifStrokeDrawer:
    def __init__(self, font: Serif, canvas: svgwrite.Drawing) -> None:
        self.font = font
        self.canvas = canvas
        
    def __DrawCurveU(self, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, opt1, hane_adjustment, opt3, opt4):
        kMinWidthT = self.font.kMinWidthT - opt1 / 2

        if (a1 % 100) in [0,7,27]:
            delta1 = -1 * self.font.kMinWidthY * 0.5
        elif (a1 % 100) in [1, 2, 6, 22, 32]:
            delta1 = 0
        elif (a1 % 100) in [12]:
            delta1 = self.font.kMinWidthY
        else:
            return

        if delta1 != 0:
            vec_d = Vec2(0, delta1) if all(vec_1 == vec_s1) else normalize(vec_1 - vec_s1, delta1)
            vec_1 += vec_d

        cornerOffset = 0
        if ((a1 == 22 or a1 == 27) and a2 == 7 and kMinWidthT > 6):
            contourLength = np.hypot(*(vec_s1 - vec_1)) + np.hypot(*(vec_s2 - vec_1)) + np.hypot(*(vec_2 - vec_s2))
            if (contourLength < 100):
                cornerOffset = (kMinWidthT - 6) * ((100 - contourLength) / 100)
                vec_1.x += cornerOffset

        if a2 % 100 in [0,1,7,9,15,14,17,5]:
            delta2 = 0
        elif a2 % 100 == 8:
            delta2 = -1 * kMinWidthT * 0.5
        else:
            delta2 = delta1

        if delta2 != 0:
            vec_d = Vec2(0, -delta2) if all(vec_2 == vec_s2) else normalize(vec_2 - vec_s2, delta2)
            vec_2 += vec_d
        
        is_quadratic = all(vec_s1 == vec_s2)
        
        hosomi = 0.5
        if np.hypot(*(vec_2 - vec_1)) < 50:
            hosomi = 0.4 * (1 - np.hypot(*(vec_2 - vec_1))) / 50
            
        
    # TODO

    def DrawBezier(self, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, opt1, hane_adjustment, opt3, opt4):
        SerifStrokeDrawer.__DrawCurveU(self, vec_1, vec_s1, vec_s2, vec_2, a1, a2, opt1, hane_adjustment, opt3, opt4)

    def DrawCurve(self, vec_1: Vec2, vec_s: Vec2, vec_2: Vec2, a1: int, a2: int, opt1, hane_adjustment, opt3, opt4):
        SerifStrokeDrawer.__DrawCurveU(self, vec_1, vec_s, vec_s, vec_2, a1, a2, opt1, hane_adjustment, opt3, opt4)
    
    def DrawLine(self, vec_1: Vec2, vec_2: Vec2, a1: int, a2: int, opt1, uroko_adjustment, kakato_adjustment):
        pass
    # TODO