import csv
from kirkpatrick import planar_graph
import earcut

polygon = []

with open('../test/simple_polygon.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        polygon.append((float(row[0]), float(row[1])))

print("Polygon: " + str(polygon))

outer_triangle = []

with open('../test/outer_triangle.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        outer_triangle.append((float(row[0]), float(row[1])))

print("Outer Triangle: " + str(outer_triangle))

pg = planar_graph.PlanarGraph()

vertex_ids = [pg.addVertex(p[0], p[1]) for p in polygon]
print("Vertex IDs of polygon: " + str(vertex_ids))

vertex_ids_triangle = [pg.addVertex(p[0], p[1]) for p in outer_triangle]
print("Vertex IDs of outer triangle: " + str(vertex_ids_triangle))


print("Find the triangles that are the outside the polygon:")
input_to_earcut = earcut.flatten([outer_triangle, polygon])
print("Ear-cut input: " + str(input_to_earcut))



output_earcut = earcut.earcut(input_to_earcut["vertices"], input_to_earcut["holes"], input_to_earcut["dimensions"])
print("Earcut Triangles output (3 ids, 3ids....): " + str(output_earcut))


print("Find the triangles from inside the polygon")
p_list = earcut.flatten([polygon, []])
p_triangles = earcut.earcut(p_list["vertices"], dim=p_list["dimensions"])
print(p_list)
print(p_triangles)



