class Point:
    # static variable for master list of all points encountered so far
    #master_pts = dict()
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #if (x, y) in self.master_pts:
        #    self = self.master_pts[(x, y)]
        #else:
        #    self.master_pts[(x, y)] = self


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        if p2.x - p1.x == 0:
            print("Please don't use vertical lines in polygons! We're "
                  + "working on a fix but for now this breaks"
                  + " the implementation.")
            exit(1)

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

        onetrue = lambda x, y, z: (int(x) + int(y) + int(z)) == 1

        one_above = onetrue(line1.point_above(point), line2.point_above(point), line3.point_above(point))
        one_below = onetrue((not line1.point_above(point)), (not line2.point_above(point)), (not line3.point_above(point)))

        return one_above or one_below

    def overlaps(self, tri):
        lines = []
        lines.append((self.points[2], Line(self.points[0], self.points[1])))
        lines.append((self.points[0], Line(self.points[1], self.points[2])))
        lines.append((self.points[1], Line(self.points[2], self.points[0])))

        for v, line in lines:
            all_below = True
            all_above = True
            for p in tri.points:
                above = line.point_above(p)
                all_below = all_below and (not above)
                all_above = all_above and above

            if all_above and not line.point_above(v):
                return False
            elif all_below and line.point_above(v):
                return False

        return True

    def copy(self):
        return Triangle(self.points, self.polygon)

