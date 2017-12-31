class Polygon:
    def __init__(self, name, points):
            self.name = name
            self.points = points
            self.i = 0

    def __str__(self):
        return self.name + ": " + str(self.points)

    def __getitem__(self, item):
        return self.points[item]

    def __len__(self):
        return len(self.points)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= len(self.points):
            self.i = 0
            raise StopIteration
        self.i += 1
        return self.points[self.i - 1]
