class InputPolygon:
        def __init__(self, name, points):
                self.name = name
                self.points = points

        def __str__(self):
            return self.name + ": " + str(self.points)

        def __getitem__(self, item):
            return self.points[item]
