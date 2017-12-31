import csv
from kirkpatrick import poly
from kirkpatrick import pl
from kirkpatrick import simplices

# Initialize list of Polygon objects to pass into point locator
polygons = []

# Load one polygon at a time into our list, from CSV test files
for i in range(1, 8):
    p = []
    with open("../test/crazy_poly" + str(i) + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            p.append(simplices.Vertex(float(row[0]), float(row[1])))
    polygon = poly.Polygon("Polygon " + str(i), list(p))
    polygons.append(polygon)

# Load outer hull from a file; this could be calculated, but for now we simply
# load in the big triangle from a file
p = []
with open('../test/crazy_outer.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        p.append(simplices.Vertex(float(row[0]), float(row[1]), True))

hull = poly.Polygon("Outer Hull (None)", p)

# Construct a point locator, initializing it with these polygons and hull
locator = pl.PointLocator(polygons, hull, True)

# Run some test cases
print(locator.query(simplices.Vertex(15, 0))) # Polygon 1
print(locator.query(simplices.Vertex(5, 0))) # Polygon 2
print(locator.query(simplices.Vertex(5, 10))) # Polygon 3
print(locator.query(simplices.Vertex(5, -10))) # Polygon 4
print(locator.query(simplices.Vertex(20, 10))) # Polygon 5
print(locator.query(simplices.Vertex(20, 0))) # Polygon 6
print(locator.query(simplices.Vertex(10, 5))) # Polygon 6 (again; it's big)
print(locator.query(simplices.Vertex(0, 0))) # Polygon 7
print(locator.query(simplices.Vertex(40, 0))) # Outer hull, i.e. no polygon
print(locator.query(simplices.Vertex(100, 100))) # Outside even the outer hull

