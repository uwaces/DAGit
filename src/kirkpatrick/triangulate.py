from kirkpatrick import earcut
from kirkpatrick import simplices

def get_triangulation(graph, polygon, hole=None):
    # Flatten the points
    points = []
    for p in polygon:
        points.append(p.x)
        points.append(p.y)

    # Triangulate -- including hole
    if hole is not None:
        hole_begin = len(points) // 2
        for p in hole:
            points.append(p.x)
            points.append(p.y)

        triangulation = earcut.earcut(points, [hole_begin])
    else:
        triangulation = earcut.earcut(points)

    # convert back into a list of triangles
    triangles = set()
    for i in range(0, len(triangulation), 3):
        v1 = triangulation[i]
        v2 = triangulation[i+1]
        v3 = triangulation[i+2]

        p1 = polygon[v1] if v1 < len(polygon) else hole[v1 - len(polygon)]
        p2 = polygon[v2] if v2 < len(polygon) else hole[v2 - len(polygon)]
        p3 = polygon[v3] if v3 < len(polygon) else hole[v3 - len(polygon)]

        triangles.add(simplices.Triangle([p1, p2, p3]))

    return triangles


# Triangulate a polygon and fix graph appropriately
def triangulate(graph, polygon, hole=None):
    # magic triangulation
    triangles = get_triangulation(graph, polygon, hole)

    # connect the graph / add triangles to the points / return the triangle ids
    new_triangles = set()
    for t in triangles:
        print(t)
        graph.connect(t.vertices[0], t.vertices[1])
        graph.connect(t.vertices[1], t.vertices[2])
        graph.connect(t.vertices[2], t.vertices[0])

        # create new triangle
        new_triangles.add(t)
        graph.all_triangles.add(t)

        # add new triangle to each of the three vertices' lists
        t.vertices[0].addTriangle(t)
        t.vertices[1].addTriangle(t)
        t.vertices[2].addTriangle(t)

    return new_triangles
