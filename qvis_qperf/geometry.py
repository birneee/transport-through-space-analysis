from typing import Optional


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2


class Interception:
    point: Point
    positive: Optional[bool]

    def __init__(self, point: Point, positive: Optional[bool] = None):
        self.point = point
        self.positive = positive


def ccw(a: Point, b: Point, c: Point) -> bool:
    return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)


def do_segments_intersect(l1: Line, l2: Line) -> bool:
    return ccw(l1.p1, l2.p1, l2.p2) != ccw(l1.p2, l2.p1, l2.p2) \
           and ccw(l1.p1, l1.p2, l2.p1) != ccw(l1.p1, l1.p2, l2.p2)


def det(x1, y1, x2, y2):
    return x1 * y2 - y1 * x2


def line_intersection(l1: Line, l2: Line) -> Optional[Interception]:
    """intersection of infinite length lines"""
    xd1 = l1.p1.x - l1.p2.x
    xd2 = l2.p1.x - l2.p2.x
    yd1 = l1.p1.y - l1.p2.y
    yd2 = l2.p1.y - l2.p2.y
    div = det(xd1, xd2, yd1, yd2)
    if div == 0:
        return None
    d1 = det(l1.p1.x, l1.p1.y, l1.p2.x, l1.p2.y)
    d2 = det(l2.p1.x, l2.p1.y, l2.p2.x, l2.p2.y)
    x = det(d1, d2, xd1, xd2) / div
    y = det(d1, d2, yd1, yd2) / div
    return Interception(Point(x, y), positive=div < 0)


def segments_intersection(l1: Line, l2: Line) -> Optional[Interception]:
    if not do_segments_intersect(l1, l2):
        return
    return line_intersection(l1, l2)
