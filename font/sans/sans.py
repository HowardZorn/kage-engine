from kage.font.serif.serif import Serif
from kage.vec2 import Vec2
from ..serif   import Serif
from .sans_stroke_drawer import SansStrokeDrawer
from ...util import normalize
import svgwrite
import numpy as np

class Sans(Serif):
    def __init__(self, size=2) -> None:
        super().__init__(size)
        self.kKakato = 1.5
    
    def draw_stroke(self, canvas: svgwrite.Drawing):
        for serif_stroke in self.serif_strokes:
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 0:
                pass
            elif stroke.a1_100 == 1:
                if stroke.a3_100 == 4 and serif_stroke.hane_adjustment == 0 and stroke.a3_opt_2 == 0:
                    vec_d = Vec2(0, self.kMage) if all(stroke.vec_1 == stroke.vec_2) else normalize(stroke.vec_1 - stroke.vec_2, self.kMage)
                    vec_t = stroke.vec_2 + vec_d
                    SansStrokeDrawer.DrawLine(self, canvas, stroke.vec_1, vec_t, stroke.a2_100, 1)
                    SansStrokeDrawer.DrawCurve(self, canvas, vec_t, stroke.vec_2, stroke.vec_2 - Vec2(self.kMage * 2, self.kMage * 0.5), 1, 0)
                else:
                    SansStrokeDrawer.DrawLine(self, canvas, stroke.vec_1, stroke.vec_2, stroke.a2_100, stroke.a3_100)
            elif stroke.a1_100 in [2, 12]:
                if stroke.a3_100 == 4 and serif_stroke.hane_adjustment == 0 and stroke.a3_opt_2 == 0:
                    vec_d = Vec2(0, -self.kMage) if all(stroke.vec_2.x == stroke.vec_3.x) else normalize(stroke.vec_2 - stroke.vec_3, self.kMage)
                    vec_t = stroke.vec_3 + vec_d
                    SansStrokeDrawer.DrawCurve(self, canvas, stroke.vec_1, stroke.vec_2, vec_t, stroke.a2_100, 1)
                    SansStrokeDrawer.DrawCurve(self, canvas, vec_t, stroke.vec_3, stroke.vec_3 - Vec2(self.kMage * 2, self.kMage * 0.5), 1, 0)
                elif stroke.a3_100 == 5 and stroke.a3_opt == 0:
                    vec_t1 = stroke.vec_3 + Vec2(self.kMage, 0)
                    vec_t2 = Vec2(vec_t1.x, stroke.vec_3.y) + Vec2(self.kMage * 0.5, - self.kMage * 2)
                    SansStrokeDrawer.DrawCurve(self, canvas, stroke.vec_1, stroke.vec_2, stroke.vec_3, stroke.a2_100, 1)
                    SansStrokeDrawer.DrawCurve(self, canvas, stroke.vec_3, vec_t1, vec_t2, 1, 0)
                else:
                    SansStrokeDrawer.DrawCurve(self, canvas, stroke.vec_1, stroke.vec_2, stroke.vec_3, stroke.a2_100, stroke.a3_100)
            elif stroke.a1_100 == 3:
                vec_d1 = Vec2(0, self.kMage) if all(stroke.vec_1 == stroke.vec_2) else normalize(stroke.vec_1 - stroke.vec_2, self.kMage)
                vec_t1 = stroke.vec_2 + vec_d1
                vec_d2 = Vec2(0, -self.kMage) if all(stroke.vec_2 == stroke.vec_3) else normalize(stroke.vec_3 - stroke.vec_2, self.kMage)
                vec_t2 = stroke.vec_2 + vec_d2

                SansStrokeDrawer.DrawLine(self, canvas, stroke.vec_1, vec_t1, stroke.a2_100, 1)
                SansStrokeDrawer.DrawCurve(self, canvas, vec_t1, stroke.vec_2, vec_t2, 1, 1)

                if stroke.a3_100 == 5 and stroke.a3_opt_1 == 0 and serif_stroke.mage_adjustment == 0:
                    vec_t3 = stroke.vec_3 + Vec2(0, -self.kMage)
                    vec_t4 = stroke.vec_3 + Vec2(self.kMage * 0.5, -self.kMage * 2)

                    SansStrokeDrawer.DrawLine(self, canvas, vec_t2, vec_t3, 1, 1)
                    SansStrokeDrawer.DrawCurve(self, canvas, vec_t3, stroke.vec_3, vec_t4, 1, 0)
                else:
                    SansStrokeDrawer.DrawLine(self, canvas, vec_t2, stroke.vec_3, 1, stroke.a3_100)
            elif stroke.a1_100 == 4:
                rate = np.hypot(*(stroke.vec_3 - stroke.vec_2)) / 120 * 6
                if (rate > 6):
                    rate = 6
                vec_d1 = Vec2(0, self.kMage * rate) if all(stroke.vec_1 == stroke.vec_2) else normalize(stroke.vec_1 - stroke.vec_2, self.kMage * rate)
                vec_t1 = stroke.vec_2 + vec_d1
                vec_d2 = Vec2(0, -self.kMage * rate) if all(stroke.vec_2 == stroke.vec_3) else normalize(stroke.vec_3 - stroke.vec_2, self.kMage * rate)
                vec_t2 = stroke.vec_2 + vec_d2
                SansStrokeDrawer.DrawLine(self, canvas, stroke.vec_1, vec_t1, stroke.a2_100, 1)
                SansStrokeDrawer.DrawCurve(self, canvas, vec_t1, stroke.vec_2, vec_t2, 1, 1)

                if not(stroke.a3_100 == 5 and stroke.a3_opt == 0 and stroke.vec_3.x - vec_t2.x <= 0):
                    SansStrokeDrawer.DrawLine(self, canvas, vec_t2, stroke.vec_3, 6, stroke.a3_100)
                
            elif stroke.a1_100 == 6:
                if stroke.a3_100 == 5 and stroke.a3_opt == 0:
                    vec_t1 = stroke.vec_4 + Vec2(-self.kMage, 0)
                    vec_t2 = stroke.vec_4 + Vec2(self.kMage * 0.5, -self.kMage * 2)

                    SansStrokeDrawer.DrawBezier(self, canvas, stroke.vec_1, stroke.vec_2, stroke.vec_3, vec_t1, stroke.a2_100, 1)
                    SansStrokeDrawer.DrawCurve(self, canvas, vec_t1, stroke.vec_4, vec_t2, 1, 0)
                else:
                    SansStrokeDrawer.DrawBezier(self, canvas, stroke.vec_1, stroke.vec_2, stroke.vec_3, stroke.vec_4, stroke.a2_100, stroke.a3_100)
            elif stroke.a1_100 == 7:
                SansStrokeDrawer.DrawLine(self, canvas, stroke.vec_1, stroke.vec_2, stroke.a2_100, 1)
                SansStrokeDrawer.DrawCurve(self, canvas, stroke.vec_2, stroke.vec_3, stroke.vec_4, 1, stroke.a3_100)
            else:
                pass