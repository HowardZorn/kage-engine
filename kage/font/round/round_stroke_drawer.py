from ...vec2 import Vec2, normalize
from ..sans import Sans
import svgwrite
import svgwrite.path
import numpy as np

def if_in_merge_range(vec_1: Vec2, vec_2: Vec2, merge_range: float) -> bool:
    return np.hypot(*(vec_1 - vec_2)) < merge_range

def generate_d(vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, is_quadratic: bool = False, append_last: bool = False, is_smooth: bool = False) -> str:
    ret = str()
    if not append_last:
        ret += f"M{vec_1} "
    
    if is_quadratic:
        if is_smooth:
            ret += f"T{vec_2}"
        else:
            ret += f"Q{vec_s1} {vec_2}"
    else:
        if is_smooth:
            ret += f"S{vec_s2} {vec_2}"
        else:
            ret += f"C{vec_s1} {vec_s2} {vec_2}"
    return ret

class RoundStrokeDrawer:
    def __init__(self, font: Sans, canvas: svgwrite.Drawing) -> None:
        self.font = font
        self.canvas = canvas
        self.last_point = Vec2(np.inf, np.inf)

    def __draw_curve_universal(self, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, is_quadratic: bool = False, is_smooth: bool = False, append_last: bool = False):
        delta1 = 0
        if (temp := a1 % 10) == 0:
            pass
        # elif temp == 2:
        #     delta1 = font.kWidth
        # elif temp == 3:
        #     delta1 = font.kWidth * font.kKakato
        # elif temp == 7: # New
        #     delta1 = -self.font.kWidth
        if delta1 != 0:
            vec_d1 = Vec2(0, delta1) if all(vec_1 == vec_s1) else normalize(vec_1 - vec_s1, delta1)
            vec_1 += vec_d1

        delta2 = 0
        if (temp := a2 % 10) == 0:
            pass
        # elif temp == 2:
        #     delta2 = self.font.kWidth
        # elif temp == 3:
        #     delta2 = self.font.kWidth * self.font.kKakato
        # elif temp == 7: # New
        #     delta2 = -self.font.kWidth * self.font.kKakato
        if delta2 != 0:
            vec_d2 = Vec2(0, delta2) if all(vec_2 == vec_s2) else normalize(vec_2 - vec_s2, delta2)
            vec_2 += vec_d2

        if not append_last:
            append_last = if_in_merge_range(vec_1, self.last_point, self.font.kWidth)
                
        if not append_last:
            self.canvas.add(svgwrite.path.Path(d = generate_d(vec_1, vec_s1, vec_s2, vec_2, is_quadratic, append_last, is_smooth), stroke = 'black', stroke_width = self.font.kWidth * 2, fill = 'none', stroke_linejoin="round", stroke_linecap="round"))
        else:
            self.canvas.elements[-1].push(generate_d(vec_1, vec_s1, vec_s2, vec_2, is_quadratic, append_last, is_smooth))
        
        self.last_point = vec_2

    def draw_bezier(self, vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, a1: int, a2: int, is_smooth: bool = False, append_last: bool = False):
        RoundStrokeDrawer.__draw_curve_universal(self, vec_1, vec_s1, vec_s2, vec_2, a1, a2, False, is_smooth, append_last)

    def draw_curve(self, vec_1: Vec2, vec_s: Vec2, vec_2: Vec2, a1: int, a2: int, is_smooth: bool = False, append_last: bool = False):
        RoundStrokeDrawer.__draw_curve_universal(self, vec_1, vec_s, vec_s, vec_2, a1, a2, True, is_smooth, append_last)
    
    def draw_line(self, vec_1: Vec2, vec_2: Vec2, a1: int, a2: int, append_last: bool = False):
        if not append_last:
            append_last = if_in_merge_range(vec_1, self.last_point, self.font.kWidth)

        if not append_last:
            self.canvas.add(svgwrite.path.Path(d = f'M{vec_1.x},{vec_1.y} L{vec_2.x},{vec_2.y}', stroke = 'black', stroke_width = self.font.kWidth * 2, fill = 'none', stroke_linejoin="round", stroke_linecap="round"))
        else:
            self.canvas.elements[-1].push(f'L{vec_2.x},{vec_2.y}')

        self.last_point = vec_2
