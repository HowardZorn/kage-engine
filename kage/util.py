from . vec2 import Vec2, normalize

from typing import Callable, Tuple, List
from math import floor


def ternary_search_max(f: Callable[[float], float], left: float, right: float,
                       absolute_precision=1E-5) -> float:
    """
    Find maximum of unimodal function f() within [left, right].
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


def ternary_search_min(f: Callable[[float], float], left: float, right: float,
                       absolute_precision=1E-5) -> float:
    return ternary_search_max(
        lambda x: -f(x),
        left, right, absolute_precision
    )


def quadratic_bezier(vec_1: Vec2, vec_s1: Vec2, vec_2: Vec2, t: float) -> Vec2:
    s = 1 - t
    return s ** 2 * vec_1 + 2 * s * t * vec_s1 + t ** 2 * vec_2


def cubic_bezier(vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, t: float) -> Vec2:
    s = 1 - t
    return s ** 3 * vec_1 + 3 * s ** 2 * t * vec_s1 + 3 * s * t ** 2 * vec_s2 + t ** 3 * vec_2


def quadratic_bezier_deriv(vec_1: Vec2, vec_s1: Vec2, vec_2: Vec2, t: float) -> Vec2:
    return 2 * (t * (vec_1 - 2 * vec_s1 + vec_2) - vec_1 + vec_s1)


def cubic_bezier_deriv(vec_1: Vec2, vec_s1: Vec2, vec_s2: Vec2, vec_2: Vec2, t: float) -> Vec2:
    return 3 * 3 * (t * (t * (-vec_1 + 3 * vec_s1 - 3 * vec_s2 + vec_2) + 2 * (vec_1 - 2 * vec_s1 + vec_s2)) - vec_1 + vec_s1)


def divide_curve(dot_1: Vec2, dot_s1: Vec2, dot_2: Vec2, curve: List[Vec2]) \
        -> Tuple[int, Tuple[Vec2, Vec2, Vec2], Tuple[Vec2, Vec2, Vec2]]:
    rate = 0.5
    cut = floor(len(curve) * rate)
    cut_rate = cut / len(curve)
    dot_t1 = dot_1 + (dot_s1 - dot_1) * cut_rate
    dot_t2 = dot_s1 + (dot_2 - dot_s1) * cut_rate
    dot_t3 = dot_t1 + (dot_t2 - dot_t1) * cut_rate

    return cut, (dot_1, dot_t1, dot_t3), (dot_t3, dot_t2, dot_2)


def find_offcurve(curve: List[Vec2], dot_s: Vec2) -> Tuple[Vec2, Vec2, Vec2]:
    dot_n1 = curve[0]
    dot_n2 = curve[-1]

    area = 8

    minx = ternary_search_min(
        lambda tx:
            sum([(p[0] - quadratic_bezier(dot_n1.x, tx, dot_n2.x, i / (len(curve) - 1))) ** 2
                 for i, p in enumerate(curve)]),
        dot_s.x - area, dot_s.x + area)
    miny = ternary_search_min(
        lambda ty:
            sum([(p[0] - quadratic_bezier(dot_n1.y, ty, dot_n2.y, i / (len(curve) - 1))) ** 2
                 for i, p in enumerate(curve)]),
        dot_s.y - area, dot_s.y + area)

    return dot_n1, Vec2(minx, miny), dot_n2


def generate_flatten_curve(
    vec_1: Vec2, vec_s1: Vec2,
    vec_s2: Vec2, vec_2: Vec2,
    k_rate: float, width_func: Callable[[float], float]
) -> Tuple[List[Vec2], List[Vec2]]:
    left = []
    right = []

    is_quadratic = all(vec_s1 == vec_s2)

    dot_func, i_dot_func = \
        (lambda t: quadratic_bezier(vec_1, vec_s1, vec_2, t),
            lambda t: quadratic_bezier_deriv(vec_1, vec_s1, vec_2, t)) \
        if is_quadratic else \
        (lambda t: cubic_bezier(vec_1, vec_s1, vec_s2, vec_2, t),
            lambda t: cubic_bezier_deriv(vec_1, vec_s1, vec_s2, vec_2, t))

    for tt in range(0, 1001, k_rate):
        t = tt / 1000
        dot = dot_func(t)
        i_dot = i_dot_func(t)
        width = width_func(t)
        i_dot = Vec2(-width, 0) if all(i_dot == Vec2(0, 0)) else \
            normalize(Vec2(-i_dot.y, i_dot.x), width)  # XXX ???

        left.append(dot - i_dot)
        right.append(dot + i_dot)

    return left, right
