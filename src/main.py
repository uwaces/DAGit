import csv
from kirkpatrick import poly
from kirkpatrick import pl
from kirkpatrick import simplices

p = []
with open('../test/simple_polygon.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        p.append(simplices.Vertex(float(row[0]), float(row[1])))

polygon = poly.Polygon("Polygon 1", list(p))
print(polygon)

p = []
with open('../test/outer_triangle.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        p.append(simplices.Vertex(float(row[0]), float(row[1]), True))

hull = poly.Polygon("Outer Hull (None)", p)
print(hull)

locator = pl.PointLocator([polygon], hull, True)
print(locator.query(simplices.Vertex(6, 4)))
print(locator.query(simplices.Vertex(100, 100)))

