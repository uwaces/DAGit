import csv
from kirkpatrick import poly
from kirkpatrick import pl
from kirkpatrick import simplices

# Initialize list of Polygon objects to pass into point locator
polygons = []

base_filename_str = "../test/crazy_poly"
num_polygons = 8
# Load one polygon at a time into our list, from CSV test files.
# These files are formatted as:
# base_filename_str1.csv
# base_filename_str2.csv
# base_filename_str3.csv
# ...etc, up to num_polygons
for i in range(1, num_polygons):
    p = []
    with open(base_filename_str + str(i) + ".csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            p.append(simplices.Vertex(float(row[0]), float(row[1])))
    polygon = poly.Polygon("Polygon " + str(i), list(p))
    polygons.append(polygon)

# Construct a point locator, initializing it with these polygons
locator = pl.PointLocator(polygons, True)

# Run some test cases
print(locator.query(simplices.Vertex(15, 0)))  # Polygon 1
print(locator.query(simplices.Vertex(5, 0)))  # Polygon 2
print(locator.query(simplices.Vertex(5, 10)))  # Polygon 3
print(locator.query(simplices.Vertex(5, -10)))  # Polygon 4
print(locator.query(simplices.Vertex(20, 10)))  # Polygon 5
print(locator.query(simplices.Vertex(20, 0)))  # Polygon 6
print(locator.query(simplices.Vertex(10, 5)))  # Polygon 6 (again; it's big)
print(locator.query(simplices.Vertex(0, 0)))  # Polygon 7
print(locator.query(simplices.Vertex(0, 15)))  # Outer hull, i.e. no polygon
print(locator.query(simplices.Vertex(100, 100)))  # Outside even the outer hull

