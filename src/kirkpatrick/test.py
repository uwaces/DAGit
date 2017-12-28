import csv
from planar_graph import PlanarGraph
import earcut

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

vertex_ids = [pg.addVertex(p[0], p[1]) for p in polygon]
print(vertex_ids)

vertex_ids_triangle = [pg.addVertex(p[0], p[1]) for p in outer_triangle]
print(vertex_ids_triangle)

input_to_earcut = earcut.flatten([polygon, outer_triangle])

earcut.earcut(input_to_earcut["vertices"], input_to_earcut["holes"], input_to_earcut["dimensions"])
