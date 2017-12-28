import csv
from planar_graph import PlanarGraph

polygon = []

with open('simple_polygon.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        polygon.append((float(row[0]), float(row[1])))

print("Polygon: " + str(polygon))

outer_triangle = []

with open('outer_triangle.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        outer_triangle.append((float(row[0]), float(row[1])))
print("Outer Triangle: " + str(outer_triangle))

pg = PlanarGraph()