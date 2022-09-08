from ...vec2 import Vec2
from ..sans import Sans
from ...util import normalize
import svgwrite
import svgwrite.path
import numpy as np

def generate_d(vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, is_quadratic: bool = False, append_last: bool = False, is_smooth: bool = False) -> str:
    ret = ""
    if not append_last:
        ret += f"M{vec_1.x},{vec_1.y} "
    
    if is_quadratic:
        if is_smooth:
            ret += f"T{vec_2.x},{vec_2.y}"
        else:
            ret += f"Q{vec_s1.x},{vec_s1.y} {vec_2.x},{vec_2.y}"
    else:
        if is_smooth:
            ret += f"S{vec_s2.x},{vec_s2.y} {vec_2.x},{vec_2.y}"
        else:
            ret += f"C{vec_s1.x},{vec_s1.y} {vec_s2.x},{vec_s2.y} {vec_2.x},{vec_2.y}"
    return ret

class SansStrokeDrawer:
    @staticmethod
    def __DrawCurveU(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, is_quadratic: bool = False, is_smooth: bool = False, append_last: bool = False):
        delta1 = 0
        if a1 % 10 == 0:
            pass
        # elif a1 % 10 == 2:
        #     delta1 = font.kWidth
        # elif a1 % 10 == 3:
        #     delta1 = font.kWidth * font.kKakato
        # elif a1 % 10 == 7: # New
        #     print('triggered')
        #     delta1 = -font.kWidth
        if delta1 != 0:
            vec_d1 = Vec2(0, delta1) if all(vec_1 == vec_s1) else normalize(vec_1 - vec_s1, delta1)
            vec_1 += vec_d1
        delta2 = 0
        
        if a2 % 10 == 0:
            pass
        # elif a2 % 10 == 2:
        #     delta2 = font.kWidth
        # elif a2 % 10 == 3:
        #     delta2 = font.kWidth * font.kKakato
        elif a2 % 10 == 7: # New
            delta2 = -font.kWidth * font.kKakato
        if delta2 != 0:
            vec_d2 = Vec2(0, delta2) if all(vec_2 == vec_s2) else normalize(vec_2 - vec_s2, delta2)
            vec_2 += vec_d2
        if not append_last:
            canvas.add(svgwrite.path.Path(d = generate_d(vec_1, vec_s1, vec_s2, vec_2, is_quadratic, append_last, is_smooth), stroke = 'black', stroke_width = font.kWidth * 2, fill = 'none', stroke_linejoin="bevel"))
        else:
            canvas.elements[-1].push(generate_d(vec_1, vec_s1, vec_s2, vec_2, is_quadratic, append_last, is_smooth))

    @staticmethod
    def DrawBezier(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, is_smooth: bool = False, append_last: bool = False):
        SansStrokeDrawer.__DrawCurveU(font, canvas, vec_1, vec_s1, vec_s2, vec_2, a1, a2, False, is_smooth, append_last)

    @staticmethod
    def DrawCurve(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_s: Vec2, vec_2: Vec2, a1: int, a2: int, is_smooth: bool = False, append_last: bool = False):
        SansStrokeDrawer.__DrawCurveU(font, canvas, vec_1, vec_s, vec_s, vec_2, a1, a2, True, is_smooth, append_last)
    
    @staticmethod
    def DrawLine(font: Sans, canvas: svgwrite.Drawing, vec_1: Vec2, vec_2: Vec2, a1: int, a2: int, append_last: bool = False):
        if vec_1.x == vec_2.x and vec_1.y > vec_2.y or vec_1.x > vec_2.x:
            vec_1, vec_2 = vec_2, vec_1
            a1, a2 = a2, a1
            exchanged = True
        else:
            exchanged = False
        
        norm = normalize(vec_1 - vec_2, font.kWidth)

        if a1 % 10 == 2:
            vec_1 += norm
        elif a1 % 10 == 3:
            vec_1 += norm * font.kKakato
        
        if a2 % 10 == 2:
            vec_2 -= norm
        elif a2 % 10 == 3:
            vec_2 -= norm * font.kKakato
        
        if exchanged:
            vec_1, vec_2 = vec_2, vec_1
            a1, a2 = a2, a1

        if not append_last:
            canvas.add(svgwrite.path.Path(d = f'M{vec_1.x},{vec_1.y} L{vec_2.x},{vec_2.y}', stroke = 'black', stroke_width = font.kWidth * 2, fill = 'none', stroke_linejoin="bevel"))
        else:
            canvas.elements[-1].push(f'L{vec_2.x},{vec_2.y}')
