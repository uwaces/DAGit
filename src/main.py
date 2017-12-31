import csv
from kirkpatrick import poly
from kirkpatrick import pl
from kirkpatrick import simplices

polygons = []

for i in range(1, 8):
    p = []
    with open("../test/crazy_poly" + str(i) + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            p.append(simplices.Vertex(float(row[0]), float(row[1])))
    polygon = poly.Polygon("Polygon " + str(i), list(p))
    polygons.append(polygon)

p = []
with open('../test/crazy_outer.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        p.append(simplices.Vertex(float(row[0]), float(row[1]), True))

hull = poly.Polygon("Outer Hull (None)", p)

locator = pl.PointLocator(polygons, hull, True)
print(locator.query(simplices.Vertex(15, 0)))
print(locator.query(simplices.Vertex(5, 0)))
print(locator.query(simplices.Vertex(5, 10)))
print(locator.query(simplices.Vertex(5, -10)))
print(locator.query(simplices.Vertex(20, 10)))
print(locator.query(simplices.Vertex(20, 0)))
print(locator.query(simplices.Vertex(10, 5)))
print(locator.query(simplices.Vertex(0, 0)))
print(locator.query(simplices.Vertex(40, 0)))
print(locator.query(simplices.Vertex(100, 100)))

