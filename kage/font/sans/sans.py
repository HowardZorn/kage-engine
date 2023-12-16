from ...vec2 import Vec2, normalize
from ..serif import Serif
import svgwrite
import numpy as np

class Sans(Serif):
    def __init__(self, size=2) -> None:
        super().__init__(size)
        self.kKakato = 1.5
        self.kWidth = 6
    
    def draw_strokes(self, canvas: svgwrite.Drawing):
        from .sans_stroke_drawer import SansStrokeDrawer
        stroke_drawer = SansStrokeDrawer(self, canvas)
        for serif_stroke in self.serif_strokes:
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 0: # TODO:Transforms
                pass
            elif stroke.a1_100 == 1: # Linear stroke, 直線
                if stroke.a3_100 == 4 and stroke.a3_opt_2 == 0: # and serif_stroke.hane_adjustment == 0 # left hook, 左撥ね上げ
                    vec_d = Vec2(0, self.kMage) if all(stroke.vec_1 == stroke.vec_2) else normalize(stroke.vec_1 - stroke.vec_2, self.kMage)
                    vec_t = stroke.vec_2 + vec_d
                    stroke_drawer.draw_line(stroke.vec_1, vec_t, stroke.a2_100, 1)
                    stroke_drawer.draw_curve(vec_t, stroke.vec_2, stroke.vec_2 - Vec2(self.kMage * 2, self.kMage * 0.5), 1, 0, False, True)
                else: # other shapes
                    stroke_drawer.draw_line(stroke.vec_1, stroke.vec_2, stroke.a2_100, stroke.a3_100)
            elif stroke.a1_100 in [2, 12]: # 曲線（3 座標:始点, 制御点, 終点）, 二次ベジェ曲線, second order bezier curve
                if stroke.a3_100 == 4 and stroke.a3_opt_2 == 0: # and serif_stroke.hane_adjustment == 0 # left hook, 左撥ね上げ
                    vec_d = Vec2(0, -self.kMage) if stroke.vec_2.x == stroke.vec_3.x else normalize(stroke.vec_2 - stroke.vec_3, self.kMage)
                    vec_t = stroke.vec_3 + vec_d
                    stroke_drawer.draw_curve(stroke.vec_1, stroke.vec_2, vec_t, stroke.a2_100, 1)
                    stroke_drawer.draw_curve(vec_t, stroke.vec_3, stroke.vec_3 - Vec2(self.kMage * 2, self.kMage * 0.5), 1, 0, False, True)
                elif stroke.a3_100 == 5 and stroke.a3_opt == 0: # right hook, 右撥ね上げ
                    vec_t1 = stroke.vec_3 + Vec2(self.kMage, 0)
                    vec_t2 = Vec2(vec_t1.x, stroke.vec_3.y) + Vec2(self.kMage * 0.5, - self.kMage * 2)
                    stroke_drawer.draw_curve(stroke.vec_1, stroke.vec_2, stroke.vec_3, stroke.a2_100, 1)
                    stroke_drawer.draw_curve(stroke.vec_3, vec_t1, vec_t2, 1, 0, False, True)
                # elif stroke.a2_100 == 7 and stroke.a3_100 == 8: # 點, Dot; consider to move to preprocessor
                #     stroke_drawer.DrawLine(stroke.vec_1, stroke.vec_3, 1, 0)
                else: # other shapes
                    stroke_drawer.draw_curve(stroke.vec_1, stroke.vec_2, stroke.vec_3, stroke.a2_100, stroke.a3_100)
            elif stroke.a1_100 == 3: # 曲げ(3 座標:始点, 経由点, 終点), curve
                vec_d1 = Vec2(0, self.kMage) if all(stroke.vec_1 == stroke.vec_2) else normalize(stroke.vec_1 - stroke.vec_2, self.kMage)
                vec_t1 = stroke.vec_2 + vec_d1
                vec_d2 = Vec2(0, -self.kMage) if all(stroke.vec_2 == stroke.vec_3) else normalize(stroke.vec_3 - stroke.vec_2, self.kMage)
                vec_t2 = stroke.vec_2 + vec_d2
                
                stroke_drawer.draw_line(stroke.vec_1, vec_t1, stroke.a2_100, 1)
                stroke_drawer.draw_curve(vec_t1, stroke.vec_2, vec_t2, 1, 1, False, True)

                if stroke.a3_100 == 5 and stroke.a3_opt_1 == 0 and serif_stroke.mage_adjustment == 0: # right hook, 右撥ね上げ 
                    vec_t3 = stroke.vec_3 + Vec2(-self.kMage, 0)
                    vec_t4 = stroke.vec_3 + Vec2(self.kMage * 0.5, -self.kMage * 2)

                    stroke_drawer.draw_line(vec_t2, vec_t3, 1, 1, True)
                    stroke_drawer.draw_curve(vec_t3, stroke.vec_3, vec_t4, 1, 0, False, True)
                else: # other shapes
                    stroke_drawer.draw_line(vec_t2, stroke.vec_3, 1, stroke.a3_100, True)
            elif stroke.a1_100 == 4: # 乙線, OTSU curve
                rate = np.hypot(*(stroke.vec_3 - stroke.vec_2)) / 120 * 6
                if (rate > 6):
                    rate = 6
                vec_d1 = Vec2(0, self.kMage * rate) if all(stroke.vec_1 == stroke.vec_2) else normalize(stroke.vec_1 - stroke.vec_2, self.kMage * rate)
                vec_t1 = stroke.vec_2 + vec_d1
                vec_d2 = Vec2(0, -self.kMage * rate) if all(stroke.vec_2 == stroke.vec_3) else normalize(stroke.vec_3 - stroke.vec_2, self.kMage * rate)
                vec_t2 = stroke.vec_2 + vec_d2
                vec_t3 = stroke.vec_3 + Vec2(-self.kMage, 0)
                vec_t4 = stroke.vec_3 + Vec2(self.kMage * 0.5, -self.kMage * 2)
                stroke_drawer.draw_line(stroke.vec_1, vec_t1, stroke.a2_100, 1)
                stroke_drawer.draw_curve(vec_t1, stroke.vec_2, vec_t2, 1, 1, False, True)

                if stroke.a3_100 == 5 and stroke.a3_opt == 0: # right hook
                    stroke_drawer.draw_line(vec_t2, vec_t3, 1, 1, True)
                    stroke_drawer.draw_curve(vec_t3, stroke.vec_3, vec_t4, 1, 0, False, True)
                else:
                    stroke_drawer.draw_line(vec_t2, stroke.vec_3, 1, stroke.a3_100, True)
            elif stroke.a1_100 == 6: # 4 点曲線（4 座標:始点, 制御点１, ２, 終点）, triple ordered 
                if stroke.a3_100 == 4: # left hook
                    vec_d = Vec2(0, -self.kMage) if stroke.vec_3.x == stroke.vec_4.x else normalize(stroke.vec_3 - stroke.vec_4, self.kMage)
                    vec_t = stroke.vec_4 + vec_d
                    stroke_drawer.draw_bezier(stroke.vec_1, stroke.vec_2, stroke.vec_3, vec_t, stroke.a2_100, 1)
                    stroke_drawer.draw_curve(vec_t, stroke.vec_4, stroke.vec_4 - Vec2(self.kMage * 2, self.kMage * 0.5), 1, 0, False, True)
                elif stroke.a3_100 == 5 and stroke.a3_opt == 0: # right hook
                    vec_t1 = stroke.vec_4 + Vec2(-self.kMage, 0) if stroke.vec_4.x - self.kMage > stroke.vec_3.x else Vec2(stroke.vec_3.x, stroke.vec_4.y) 
                    # if else: for '戰'
                    vec_t2 = stroke.vec_4 + Vec2(self.kMage * 0.5, -self.kMage * 2)

                    stroke_drawer.draw_bezier(stroke.vec_1, stroke.vec_2, stroke.vec_3, vec_t1, stroke.a2_100, 1)
                    stroke_drawer.draw_curve(vec_t1, stroke.vec_4, vec_t2, 1, 0, False, True)
                else: # others
                    stroke_drawer.draw_bezier(stroke.vec_1, stroke.vec_2, stroke.vec_3, stroke.vec_4, stroke.a2_100, stroke.a3_100)
            elif stroke.a1_100 == 7: # 縦払い（3 座標:始点, 経由点, 制御点, 終点）, vertical slash
                stroke_drawer.draw_line(stroke.vec_1, stroke.vec_2, stroke.a2_100, 1)
                stroke_drawer.draw_curve(stroke.vec_2, stroke.vec_3, stroke.vec_4, 1, stroke.a3_100, False, True)
            else:
                pass