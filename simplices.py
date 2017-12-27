class Point:
    # static variable for master list of all points encountered so far
    master_pts = dict()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        if (x, y) in master_pts:
            return master_pts[(x, y)]
        else:
            master_pts[(x, y)] = self


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.m = (p2.y - p1.y) / (p2.x - p1.x)
        self.b = p1.y - self.m * p1.x

    def point_above(self, point):
        return (self.m * point.x + self.b - point.y) >= 0


class Triangle:
    def __init__(self, points, polygon=None):
        self.points = points
        self.polygon = polygon

    def contains(self, point):
        line1 = Line(self.points[0], self.points[1])
        line2 = Line(self.points[1], self.points[2])
        line3 = Line(self.points[2], self.points[0])

        one_above = line1.point_above(point) ^ line2.point_above(point) ^ line3.point_above(point)
        one_below = (not line1.point_above(point)) ^ (not line2.point_above(point)) ^ (not line3.point_above(point))

        return one_above or one_below

    def copy(self):
        return Triangle(self.points, self.polygon)

