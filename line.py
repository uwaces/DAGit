class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.m = (p2.y - p1.y) / (p2.x - p1.x)
        self.b = p1.y - self.m * p1.x

    def point_above(self, point):
        return (m * point.x + b - point.y) >= 0
