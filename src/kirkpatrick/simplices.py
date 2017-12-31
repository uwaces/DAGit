# A vertex is a point (x, y) and a list of triangles of which the vertex is a vertex
# the id is to be set as unique to the vertex and the removed variable marks weather the 
# vertex was removed or not.


class Vertex:
    def __init__(self, x, y, hull_member=False):
        self.x = x
        self.y = y
        self.triangles = set()
        self.hull_member = hull_member

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def addTriangle(self, tri):
        if tri not in self.triangles:
            self.triangles.add(tri)

    def removeTriangle(self, tri):
        self.triangles.remove(tri)


class Line:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

        if v2.x - v1.x == 0:
            print("Please don't use vertical lines in polygons! We're "
                  + "working on a fix but for now this breaks"
                  + " the implementation.")
            exit(1)

        self.m = (v2.y - v1.y) / (v2.x - v1.x)
        self.b = v1.y - self.m * v1.x

    def point_above(self, point):
        return (self.m * point.x + self.b - point.y) >= 0


class Triangle:
    def __init__(self, vertices, polygon=None):
        self.vertices = vertices
        self.polygon = polygon
        self.i = 0

    def contains(self, point):
        line1 = Line(self.vertices[0], self.vertices[1])
        line2 = Line(self.vertices[1], self.vertices[2])
        line3 = Line(self.vertices[2], self.vertices[0])

        onetrue = lambda x, y, z: (int(x) + int(y) + int(z)) == 1

        one_above = onetrue(line1.point_above(point), line2.point_above(point), line3.point_above(point))
        one_below = onetrue((not line1.point_above(point)), (not line2.point_above(point)), (not line3.point_above(point)))

        return one_above or one_below

    def overlaps(self, tri):
        lines = []
        lines.append((self.vertices[2], Line(self.vertices[0], self.vertices[1])))
        lines.append((self.vertices[0], Line(self.vertices[1], self.vertices[2])))
        lines.append((self.vertices[1], Line(self.vertices[2], self.vertices[0])))

        for v, line in lines:
            all_below = True
            all_above = True
            for p in tri.vertices:
                above = line.point_above(p)
                all_below = all_below and (not above)
                all_above = all_above and above

            if all_above and not line.point_above(v):
                return False
            elif all_below and line.point_above(v):
                return False

        return True

    def copy(self):
        return Triangle(self.vertices, self.polygon)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i > 2:
            self.i = 0
            raise StopIteration
        self.i += 1
        return self.vertices[self.i - 1]

