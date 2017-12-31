from kirkpatrick import earcut
from kirkpatrick import simplices

def get_triangulation(graph, polygon, hole=None):
    # Flatten the points
    points = []
    for p in polygon:
        points.append(graph.vertices[p].point.x)
        points.append(graph.vertices[p].point.y)

    # Triangulate -- including hole
    if hole is not None:
        hole_begin = len(points) // 2
        for p in hole:
            points.append(graph.vertices[p].point.x)
            points.append(graph.vertices[p].point.y)

        triangulation = earcut.earcut(points, [hole_begin])
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
    triangles = get_triangulation(graph, polygon, hole)

    # connect the graph / add triangles to the points / return the triangle ids
    new_triangle_ids = []
    for t in triangles:
        print(t)
        graph.connect(t[0], t[1])
        graph.connect(t[1], t[2])
        graph.connect(t[2], t[0])

        # create new triangle
        tri = simplices.Triangle([t[0], t[1], t[2]])
        triangle_id = len(graph.all_triangles)
        new_triangle_ids.append(triangle_id)
        graph.all_triangles.append(tri)

        # add new triangle to each of the three vertices' lists
        graph.vertices[t[0]].addTriangle(triangle_id)
        graph.vertices[t[1]].addTriangle(triangle_id)
        graph.vertices[t[2]].addTriangle(triangle_id)

    return new_triangle_ids
