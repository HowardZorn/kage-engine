from ...stroke import Stroke

class SerifStroke:
    def __init__(self, stroke: Stroke) -> None:
        self.stroke = stroke
        self.kirikuchi_adjustment = self.stroke.a2_opt_1
        self.tate_adjustment = self.stroke.a2_opt_2 + self.stroke.a2_opt_3 * 10
        self.hane_adjustment = self.stroke.a3_opt_1
        self.uroko_adjustment = self.stroke.a3_opt
        self.kakato_adjustment = self.stroke.a3_opt
        self.mage_adjustment = self.stroke.a3_opt_2

    def __repr__(self) -> str:
        return '[' + repr(self.stroke) + ',' + ','.join([str(int(i)) for i in [self.kirikuchi_adjustment, self.tate_adjustment, self.hane_adjustment, self.uroko_adjustment, self.kakato_adjustment, self.mage_adjustment]]) + ']\n'
