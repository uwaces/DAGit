import csv
from kirkpatrick import planar
from kirkpatrick import dag as DAG
from kirkpatrick import triangulate
from kirkpatrick import poly

p = []
with open('../test/simple_polygon.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        p.append((float(row[0]), float(row[1])))

polygon = poly.InputPolygon("Inside", p)
print(polygon)

p = []
with open('../test/outer_triangle.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        p.append((float(row[0]), float(row[1])))

hull = poly.InputPolygon("Outer Triangle", p)
print(hull)

pg = planar.PlanarGraph()

# Order matters so that vertex id's match
vertex_ids_triangle = [pg.addVertex(p[0], p[1]) for p in hull]
print("Vertex IDs of outer triangle: " + str(vertex_ids_triangle))

vertex_ids = [pg.addVertex(p[0], p[1]) for p in polygon]
print("Vertex IDs of polygon: " + str(vertex_ids))

# Connect up the polygon
for v_i in range(1, len(vertex_ids)):
    pg.connect(vertex_ids[v_i], vertex_ids[v_i-1])
pg.connect(vertex_ids[-1], vertex_ids[0])

# Get the inner triangles:
triangles = triangulate.triangulate(pg, vertex_ids)

print("Inner triangle id's: " + str(triangles))

# Connect up the outer triangle
for v_i in range(1, len(vertex_ids_triangle)):
    pg.connect(vertex_ids_triangle[v_i], vertex_ids_triangle[v_i-1])
pg.connect(vertex_ids_triangle[-1], vertex_ids_triangle[0])

outer_triangles = triangulate.triangulate(pg, vertex_ids_triangle, vertex_ids)

print("Outer Triangle ID's " + str(outer_triangles))

triangle_list = triangles + outer_triangles

dag = DAG.DAG()

while len(pg.find_indep_low_deg()):
    print(triangle_list)
    triangle_list = pg.removeVertices(pg.find_indep_low_deg(), dag, triangle_list)

print(triangle_list)
print(dag)

# DAG BUILT: Next step query:
