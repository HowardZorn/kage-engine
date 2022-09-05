from ...vec2 import Vec2
from ..sans import Sans
from ...util import generate_fatten_curve, normalize
import svgwrite
import svgwrite.path
import numpy as np

class SansStrokeDrawer:
    @staticmethod
    def __DrawCurveU(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, _ta: int, _ta2: int):
        a1, a2 = 0, 0
        delta1 = 0
        if a1 % 10 == 2:
            delta1 = font.kWidth
        elif a1 % 10 == 3:
            delta1 = font.kWidth * font.kKakato
        if delta1 != 0:
            vec_d1 = Vec2(0, delta1) if vec_1 == vec_s1 else normalize(vec_1 - vec_s1, delta1)
            vec_1 += vec_d1
        delta2 = 0
        if a2 % 10 == 2:
            delta2 = font.kWidth
        elif a2 % 10 == 3:
            delta2 = font.kWidth * font.kKakato
        if delta2 != 0:
            vec_d2 = Vec2(0, delta2) if vec_2 == vec_s2 else normalize(vec_2 - vec_s2, delta2)
            vec_2 += vec_d2
        canvas.add(generate_fatten_curve(vec_1, vec_s1, vec_s2, vec_2, font.kWidth * 2))

    @staticmethod
    def DrawBezier(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int):
        SansStrokeDrawer.__DrawCurveU(font, canvas, vec_1, vec_s1, vec_s2, vec_2, a1, a2)

    @staticmethod
    def DrawCurve(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s: Vec2, vec_2: Vec2, a1: int, a2: int):
        SansStrokeDrawer.__DrawCurveU(font, canvas, vec_1, vec_s, vec_s, vec_2, a1, a2)
    
    @staticmethod
    def DrawLine(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_2: Vec2, a1: int, a2: int):
        if vec_1.x == vec_2.x and vec_1.y > vec_2.y or vec_1.x > vec_2.x:
            vec_1, vec_2 = vec_2, vec_1
            a1, a2 = a2, a1
        
        norm = normalize(vec_1 - vec_2, font.kWidth)

        if a1 % 10 == 2:
            vec_1 += norm
        elif a1 % 10 == 3:
            vec_1 += norm * font.kKakato
        
        if a2 % 10 == 2:
            vec_2 -= norm
        elif a2 % 10 == 3:
            vec_2 -= norm * font.kKakato

        canvas.add(svgwrite.path.Path(d = f'M{vec_1.x},{vec_1.y} L{vec_2.x},{vec_2.y}', stroke = 'black', stroke_width = font.kWidth * 2, fill = 'none', stroke_linejoin="bevel"))
