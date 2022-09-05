import numpy as np
import svgwrite.path
from . vec2 import Vec2

def normalize(array: Vec2, magnitude = 1) -> Vec2:
    """
    Calculates a new vector with the same angle and a new magnitude.
    """
    # ret vector in polar coordinate system form
    ret = Vec2(magnitude, np.arctan2(array.y, array.x))
    ret = Vec2(ret[0] * np.cos(ret[1]), ret[0] * np.sin(ret[1]))
    return ret

def ternary_search_max(f, left, right, absolute_precision = 1E-5) -> float:
    """Find maximum of unimodal function f() within [left, right].
    To find the minimum, reverse the if/else statement or reverse the comparison.
    """
    while abs(right - left) >= absolute_precision:
        left_third = left + (right - left) / 3
        right_third = right - (right - left) / 3

        if f(left_third) < f(right_third):
            left = left_third
        else:
            right = right_third

    # Left and right are the current bounds; the maximum is between them
    return (left + right) / 2

def ternary_search_min(f, left, right, absolute_precision = 1E-5) -> float:
    return ternary_search_max(
        lambda x: -f(x),
        left, right, absolute_precision
    )


def generate_fatten_curve(vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, width) -> svgwrite.path.Path:
    is_quadratic = all(vec_s1 == vec_s2)
    if is_quadratic:
        return svgwrite.path.Path(d = f"M{vec_1.x},{vec_1.y} Q{vec_s1.x},{vec_s1.y} {vec_2.x},{vec_2.y}", stroke = 'black', stroke_width = width, fill = 'none', stroke_linejoin="bevel")
    else:
        return svgwrite.path.Path(d = f"M{vec_1.x},{vec_1.y} C{vec_s1.x},{vec_s1.y} {vec_s2.x},{vec_s2.y} {vec_2.x},{vec_2.y}", stroke = 'black', stroke_width = width, fill = 'none', stroke_linejoin="bevel")
    # TODO
