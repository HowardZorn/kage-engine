import svgwrite
from .. stroke import Stroke

class Font:
    def __init__(self) -> None:
        pass
    
    def drawer(self, canvas: svgwrite.Drawing, strokes_list: list[Stroke]):
        raise NotImplementedError()
