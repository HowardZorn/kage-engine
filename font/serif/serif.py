from ...vec2   import Vec2
from ...stroke import Stroke
from ...util   import normalize
from ..font    import Font
from . serif_stroke import SerifStroke
from . serif_stroke_drawer import SerifStrokeDrawer

import svgwrite
import numpy as np
from argparse import Namespace

class Serif(Font):
    def __init__(self, size = 2) -> None:
        if size == 1:
            self.kMinWidthY = 1.2
            self.kMinWidthU = 2 #
            self.kMinWidthT = 3.6
            self.kWidth = 3
            self.kKakato = 1.8
            self.kL2RDfatten = 1.1
            self.kMage = 6
            self.kUseCurve = False
            self.kAdjustKakatoL = [8, 5, 3, 1, 0]
            self.kAdjustKakatoR = [4, 3, 2, 1]
            self.kAdjustKakatoRangeX = 12
            self.kAdjustKakatoRangeY = [1, 11, 14, 18]
            self.kAdjustKakatoStep = 3
            self.kAdjustUrokoX = [14, 12, 9, 7]
            self.kAdjustUrokoY = [7, 6, 5, 4]
            self.kAdjustUrokoLength = [13, 21, 30]
            self.kAdjustUrokoLengthStep = 3
            self.kAdjustUrokoLine = [13, 15, 18]
            self.kAdjustUroko2Step = 3 #
            self.kAdjustUroko2Length = 40 #
            self.kAdjustTateStep = 4 #
            self.kAdjustMageStep = 5 #
        else:
            self.kMinWidthY = 2
            self.kMinWidthU = 2 #
            self.kMinWidthT = 6
            self.kWidth = 5
            self.kKakato = 3
            self.kL2RDfatten = 1.1
            self.kMage = 10
            self.kUseCurve = False
            self.kAdjustKakatoL = [14, 9, 5, 2, 0]
            self.kAdjustKakatoR = [8, 6, 4, 2]
            self.kAdjustKakatoRangeX = 20
            self.kAdjustKakatoRangeY = [1, 19, 24, 30]
            self.kAdjustKakatoStep = 3
            self.kAdjustUrokoX = [24, 20, 16, 12]
            self.kAdjustUrokoY = [12, 11, 9, 8]
            self.kAdjustUrokoLength = [22, 36, 50]
            self.kAdjustUrokoLengthStep = 3
            self.kAdjustUrokoLine = [22, 26, 30]
            self.kAdjustUroko2Step = 3 #
            self.kAdjustUroko2Length = 40 #
            self.kAdjustTateStep = 4 #
            self.kAdjustMageStep = 5 #

    def drawer(self, canvas: svgwrite.Drawing, strokes_list: list[Stroke]):
        self.serif_strokes = [SerifStroke(i) for i in strokes_list]
        self.adjust_stroke()
        self.draw_stroke()

    def adjust_stroke(self):
        self.adjust_hane()      # ハネ
        self.adjust_mage()      # 折れのカーブ, 曲げ
        self.adjust_tate()      # 縦画
        self.adjust_kakato()    # カカト
        self.adjust_uroko()     # ウロコ, horizontal strokes' terminal (triangle)
        self.adjust_uroko2()    # ウロコ
        self.adjust_kirikuchi() # 払い, 

    def adjust_hane(self):
        vert_segments = [
            Namespace(
                **{
                    'stroke': stroke.stroke,
                    'x': stroke.stroke.vec_1.x,
                    'y1': stroke.stroke.vec_1.y,
                    'y2': stroke.stroke.vec_2.y,
                }
            )
            for stroke in self.serif_strokes
            if stroke.stroke.a1_100 == 1 and stroke.stroke.a1_opt == 0 and stroke.stroke.vec_1.x == stroke.stroke.vec_2.x
        ]

        for serif_stroke in self.serif_strokes:
            stroke = serif_stroke.stroke
            if (stroke.a1_100 == 1 or stroke.a1_100 == 2 or stroke.a1_100 == 6) and stroke.a1_opt == 0 and stroke.a3_100 == 4 and stroke.a3_opt == 0:
                lp = Vec2(np.nan, np.nan)
                if stroke.a1_100 == 1:
                    lp = stroke.vec_2
                elif stroke.a1_100 == 2:
                    lp = stroke.vec_3
                else:
                    lp = stroke.vec_4
                mn = np.inf
                if lp.x + 18 < 100:
                    mn = lp.x + 18
                for c in vert_segments:
                    x = c.x
                    y1 = c.y1
                    y2 = c.y2
                    if (stroke != c.stroke
                        and lp.x - x < 100 and x < lp.x
                        and y1 <= lp.y and y2 >= lp.y):
                        mn = np.min([mn, lp.x - x])
                if not np.isinf(mn):
                    serif_stroke.hane_adjustment += 7 - np.floor(mn / 15)
        
    def adjust_mage(self):
        hori_segments = []
        for serif_stroke in self.serif_strokes:
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 1 and stroke.a1_opt == 0 and stroke.vec_1.y == stroke.vec_2.y:
                hori_segments.append(
                    Namespace(**{
                        'stroke': stroke,
                        'serif_stroke': serif_stroke,
                        'is_target': False,
                        'y': stroke.vec_2.y,
                        'x1': stroke.vec_1.x,
                        'x2': stroke.vec_2.x,
                    })
                )
            elif stroke.a1_100 == 3 and stroke.a1_opt == 0 and stroke.vec_2.y == stroke.vec_3.y:
                hori_segments.append(
                    Namespace(**{
                        'stroke': stroke,
                        'serif_stroke': serif_stroke,
                        'is_target': True,
                        'y': stroke.vec_2.y,
                        'x1': stroke.vec_2.x,
                        'x2': stroke.vec_3.x,
                    })
                )

        for hori_segment in hori_segments:
            stroke = hori_segment.stroke
            serif_stroke = hori_segment.serif_stroke
            is_target = hori_segment.is_target
            y = hori_segment.y
            x1 = hori_segment.x1
            x2 = hori_segment.x2

            if is_target:
                for another_hori_segment in hori_segments:
                    stroke2 = another_hori_segment.stroke
                    other_y = another_hori_segment.y
                    other_x1 = another_hori_segment.x1
                    other_x2 = another_hori_segment.x2
                    if stroke != stroke2 and not (x1 + 1 > other_x2 or x2 - 1 < other_x1) \
                    and np.round(np.abs(y - other_y), 5) < self.kMinWidthT * self.kAdjustMageStep:
                        serif_stroke.mage_adjustment += self.kAdjustMageStep - np.floor(np.abs(y- other_y) / self.kMinWidthT)
                        if serif_stroke.mage_adjustment > self.kAdjustMageStep:
                            serif_stroke.mage_adjustment = self.kAdjustMageStep

    def adjust_tate(self):
        vert_segments = [
            Namespace(
                **{
                    'stroke': stroke.stroke,
                    'serif_stroke': stroke,
                    'x': stroke.stroke.vec_1.x,
                    'y1': stroke.stroke.vec_1.y,
                    'y2': stroke.stroke.vec_2.y,
                }
            )
            for stroke in self.serif_strokes
            if (stroke.stroke.a1_100 == 1 or stroke.stroke.a1_100 == 3 or stroke.stroke.a1_100 == 7) and stroke.stroke.a1_opt == 0 and stroke.stroke.vec_1.x == stroke.stroke.vec_2.x
        ]

        for vert_segment in vert_segments:
            serif_stroke = vert_segment.serif_stroke
            stroke = vert_segment.stroke
            x = vert_segment.x
            y1 = vert_segment.y1
            y2 = vert_segment.y2
            for another_vert_segment in vert_segments:
                stroke2 = another_vert_segment.stroke
                other_x = another_vert_segment.x
                other_y1 = another_vert_segment.y1
                other_y2 = another_vert_segment.y2
                if stroke != stroke2 and not   (y1 + 1 > other_y2 or y2 - 1 < other_y1) \
                    and np.round(np.abs(x - other_x), 5) < self.kMinWidthT * self.kAdjustTateStep:
                    serif_stroke.tate_adjustment += self.kAdjustTateStep - np.floor(np.abs(x - other_x) / self.kMinWidthT)
                    if serif_stroke.tate_adjustment > self.kAdjustTateStep or serif_stroke.tate_adjustment == self.kAdjustTateStep and (stroke.a2_opt_1 != 0 or stroke.a2_100 != 0):
                        serif_stroke.tate_adjustment = self.kAdjustTateStep

    def adjust_kakato(self):
        def loop1(serif_stroke: SerifStroke):
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 1 and stroke.a1_opt == 0 \
                and (stroke.a3_100 == 13 or stroke.a3_100 == 23) and stroke.a3_opt == 0:
                def loop2(k):
                    if any([
                        stroke != serif_stroke.stroke and serif_stroke.stroke.is_cross_box(Vec2(stroke.vec_2.x - self.kAdjustKakatoRangeX / 2, stroke.vec_2.y + self.kAdjustKakatoRangeY[k]), Vec2(stroke.vec_2.x + self.kAdjustKakatoRangeX / 2, stroke.vec_2.y + self.kAdjustKakatoRangeY[k + 1]))
                        for serif_stroke in self.serif_strokes
                    ])\
                    or np.round(stroke.vec_2.y + self.kAdjustKakatoRangeY[k + 1], 5) > 200 \
                    or np.round(stroke.vec_2.y - stroke.vec_1.y) < self.kAdjustKakatoRangeY[k + 1]: # for thin box
                        serif_stroke.kakato_adjustment = 3 - k
                        return 'break'

                for k_ in range(self.kAdjustKakatoStep):
                    state = loop2(k_)
                    if state == 'break':
                        break
        
        for serif_stroke in self.serif_strokes:
            loop1(serif_stroke)

    def adjust_uroko(self):
        def loop3(serif_stroke: SerifStroke):
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 1 and stroke.a1_opt == 0 and stroke.a3_100 == 0 and stroke.a3_opt == 0: # no operation for TATE
                def loop4(k):
                    a = Vec2(1,0) \
                        if stroke.vec_1.y == stroke.vec_2.y \
                        else \
                            normalize(Vec2(stroke.vec_1.x - stroke.vec_2.x, stroke.vec_1.y - stroke.vec_2.y)) \
                            if stroke.vec_2.x - stroke.vec_1.x < 0 \
                            else \
                            normalize(Vec2(stroke.vec_2.x - stroke.vec_1.x, stroke.vec_2.y - stroke.vec_1.y))
                    cosrad = a[0]
                    sinrad = a[1]
                    tx = stroke.vec_2.x - self.kAdjustUrokoLine[k] * cosrad - 0.5 * sinrad # typo? (sinrad should be -sinrad ?)
                    ty = stroke.vec_2.y - self.kAdjustUrokoLine[k] * sinrad - 0.5 * cosrad
                    tlen = stroke.vec_2.x - stroke.vec_1.x if (stroke.vec_1.y == stroke.vec_2.y) else np.hypot(stroke.vec_2.y - stroke.vec_1.y, stroke.vec_2.x - stroke.vec_1.x)
                    if np.round(tlen, 5) < self.kAdjustUrokoLength[k] or any([
                        stroke != serif_stroke.stroke and serif_stroke.stroke.is_cross(Vec2(tx, ty), stroke.vec_2)
                        for serif_stroke in self.serif_strokes
                    ]):
                        serif_stroke.uroko_adjustment = self.kAdjustUrokoLengthStep - k
                        return 'break'
                for k_ in range(self.kAdjustUrokoLengthStep):
                    state = loop4(k_)
                    if state == 'break':
                        break
        
        for serif_stroke in self.serif_strokes:
            loop3(serif_stroke)

    def adjust_uroko2(self):
        hori_segments = []
        for serif_stroke in self.serif_strokes:
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 1 and stroke.a1_opt == 0 and stroke.vec_1.y == stroke.vec_2.y:
                hori_segments.append(
                    Namespace(**{
                        'stroke': stroke,
                        'serif_stroke': serif_stroke,
                        'is_target': stroke.a3_100 == 0 and stroke.a3_opt == 0 and serif_stroke.uroko_adjustment == 0,
                        'y': stroke.vec_1.y,
                        'x1': stroke.vec_1.x,
                        'x2': stroke.vec_2.x,
                    })
                )
            elif stroke.a1_100 == 3 and stroke.a1_100 == 0 and stroke.vec_2.y == stroke.vec_3.y:
                hori_segments.append(
                    Namespace(**{
                        'stroke': stroke,
                        'serif_stroke': serif_stroke,
                        'is_target': False,
                        'y': stroke.vec_2.y,
                        'x1': stroke.vec_2.x,
                        'x2': stroke.vec_3.x,
                    })
                )
        
        for hori_segment in hori_segments:
            serif_stroke = hori_segment.serif_stroke
            stroke = hori_segment.stroke
            is_target = hori_segment.is_target
            y = hori_segment.y
            x1 = hori_segment.x1
            x2 = hori_segment.x2
            if is_target:
                pressure = 0
                for another_hori_segment in hori_segments:
                    stroke2 = another_hori_segment.stroke
                    other_y = another_hori_segment.y
                    other_x1 = another_hori_segment.x1
                    other_x2 = another_hori_segment.x2
                    if stroke != stroke2 and not (x1 + 1 > other_x2 or x2 - 1 < other_x1) \
                    and np.round(np.abs(y - other_y)) < self.kAdjustUroko2Length:
                        pressure += np.power((self.kAdjustUroko2Length - np.abs(y - other_y)), 1.1)
                serif_stroke.uroko_adjustment = np.min([np.floor(pressure / self.kAdjustUroko2Length), self.kAdjustUroko2Step])

    def adjust_kirikuchi(self):
        hori_segments = []
        for serif_stroke in self.serif_strokes:
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 1 and stroke.a1_opt == 0 and stroke.vec_1.y == stroke.vec_2.y:
                hori_segments.append(
                    Namespace(**{
                        'y': stroke.vec_1.y,
                        'x1': stroke.vec_1.x,
                        'x2': stroke.vec_2.x,
                    })
                )
        
        def loop5(serif_stroke: SerifStroke):
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 2 and stroke.a1_opt == 0 \
            and stroke.a2_100 == 32 and stroke.a2_opt == 0 \
            and stroke.vec_1.x > stroke.vec_2.x and stroke.vec_1.y < stroke.vec_2.y and any([
                hori_segment.x1 < stroke.vec_1.x and hori_segment.x2 > stroke.vec_1.x and hori_segment.y == stroke.vec_1.y
                for hori_segment in hori_segments
            ]):
                serif_stroke.kirikuchi_adjustment = 1
        
        for serif_stroke in self.serif_strokes:
            loop5(serif_stroke)

    def draw_stroke(self):
        for serif_stroke in self.serif_strokes:
            stroke = serif_stroke.stroke
            if stroke.a1_100 == 0:
                pass # I don't know...
            elif stroke.a1_100 == 1:
                if stroke.a3_100 == 4:
                    m = Vec2(0, self.kMage) if stroke.vec_1 == stroke.vec_2 else normalize(stroke.vec_1 - stroke.vec_2, self.kMage)
                    t1 = stroke.vec_2 + m
                    # TODO