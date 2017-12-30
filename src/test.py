import csv
from kirkpatrick import planar
from kirkpatrick import earcut
from kirkpatrick import dag as DAG

def getTriangulation(graph, polygon, hole=None):
        # Flatten the points
        points = []
        for p in polygon:
                points.append(graph.vertices[p].point[0])
                points.append(graph.vertices[p].point[1])

        # Triangulate -- including hole
        if hole is not None:
                hole_begin = len(points) // 2
                for p in hole:
                        points.append(graph.vertices[p].point[0])
                        points.append(graph.vertices[p].point[1])

                triangulation = earcut.earcut(points, [hole_begin]);
        else: 
                triangulation = earcut.earcut(points)
 
        # convert back into a list of triangles
        triangles = []
        for i in range(0, len(triangulation), 3): 
                id1 = triangulation[i] 
                id2 = triangulation[i+1]
                id3 = triangulation[i+2]

                p1 = polygon[id1] if id1 < len(polygon) else hole[id1 - len(polygon)] 
                p2 = polygon[id2] if id2 < len(polygon) else hole[id2 - len(polygon)]
                p3 = polygon[id3] if id3 < len(polygon) else hole[id3 - len(polygon)]

                triangles.append([p1, p2, p3])

        return triangles 

# Triangulate a polygon and fix graph appropriately
def triangulate(graph, polygon, hole=None):
        # magic triangulation
        triangles = getTriangulation(graph, polygon, hole)

        # connect the graph / add triangles to the points / return the triangle id's 
        new_triangle_ids = []
        for t in triangles:
                print(t)
                graph.connect(t[0], t[1])
                graph.connect(t[1], t[2]) 
                graph.connect(t[2], t[0]) 

                # create new triangle 
                tri = planar.Triangle(t[0], t[1], t[2])
                triangle_id = len(graph.all_triangles)
                new_triangle_ids.append(triangle_id)  
                graph.all_triangles.append(tri) 

                # add new triangle to each of the three vertices' lists 
                graph.vertices[t[0]].addTriangle(triangle_id) 
                graph.vertices[t[1]].addTriangle(triangle_id) 
                graph.vertices[t[2]].addTriangle(triangle_id) 

        return new_triangle_ids 

def removeVertices(graph, vs, dag, triangles):
        print("LINE 66 Removing vertices: " + str(vs))
        for v in vs:
                print("Removing vertex: " + str(v))
                # Remove the given vertex
                res = graph.removeVertex(v)
                # Remove the old triangles from the triangles 
                triangles = [t for t in triangles if not t in res["old_triangles"]]
                # Triangulate the resulting polygon
                new_triangles = triangulate(graph, res["polygon"])

                triangles = new_triangles + triangles

                # Update DAG
                for o in res["old_triangles"]:
                        for n in new_triangles: 
                                if graph.overlaps(o, n):
                                        dag.addDirectedEdge(n, o)

        return triangles

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

pg = planar.PlanarGraph()


# Order matters so that vertex id's match
vertex_ids_triangle = [pg.addVertex(p[0], p[1]) for p in outer_triangle]
print("Vertex IDs of outer triangle: " + str(vertex_ids_triangle))

vertex_ids = [pg.addVertex(p[0], p[1]) for p in polygon]
print("Vertex IDs of polygon: " + str(vertex_ids))

# Connect up the polygon
for v_i in range(1, len(vertex_ids)):
        pg.connect(vertex_ids[v_i], vertex_ids[v_i-1])
pg.connect(vertex_ids[-1], vertex_ids[0])

# Get the inner triangles:
triangles = triangulate(pg, vertex_ids)

print("Inner triangle id's: " + str(triangles))

# Connect up the outer triangle
for v_i in range(1, len(vertex_ids_triangle)):
        pg.connect(vertex_ids_triangle[v_i], vertex_ids_triangle[v_i-1])
pg.connect(vertex_ids_triangle[-1], vertex_ids_triangle[0])

outer_triangles = triangulate(pg, vertex_ids_triangle, vertex_ids)

print("Outer Triangle ID's " + str(outer_triangles))

triangle_list = triangles + outer_triangles

dag = DAG.DAG()

while len(pg.find_indep_low_deg()):
        print(triangle_list)
        triangle_list = removeVertices(pg, pg.find_indep_low_deg(), dag, triangle_list)

print(triangle_list)
print(dag)

# DAG BUILT: Next step query: