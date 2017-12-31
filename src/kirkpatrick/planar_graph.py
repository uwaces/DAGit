from kirkpatrick import simplices
from kirkpatrick import triangulate


# A vertex is a point (x, y) and a list of triangles of which the vertex is a vertex
# the id is to be set as unique to the vertex and the removed variable marks weather the 
# vertex was removed or not.
class Vertex:
    def __init__(self, x, y):
        self.id = -1
        self.point = simplices.Point(x, y)
        self.triangles = []
        self.removed = False

    def addTriangle(self, tri):
        if tri not in self.triangles:
            self.triangles.append(tri)

    def removeTriangle(self, tri):
        l = self.triangles
        l_n = []
        for x in l:
            if x is not tri:
                l_n.append(x)
        self.triangles = l_n

    def getPoint(self):
        return simplices.Point(self.point.x, self.point.y)


class PlanarGraph:
    """
    The PlanarGraph contains two parallel list of vertices and the vertices' ids 
    adjacent to the vertex in the graph
    The list of all triangles is the list of all the triangles currently in the 
    graph (which will change as vertices are removed)
    When a vertex is removed it is not removed from the list but rather it is 
    marked as removed and the adjacent edges are removed and the number of vertices 
    are decremented 
    """
    def __init__(self):
        self.vertices = [] # list of Verteices
        self.adj = []   # parallel list of Vertecies
        self.all_triangles = []  # list of triangles
        self.numVertices = 0

    def addVertex(self, x, y):
        v = Vertex(x, y)
        v.id = len(self.vertices)

        self.vertices.append(v)
        self.adj.append([])
        self.numVertices += 1

        return v.id

    def addDirectedEdge(self, v_id1, v_id2):
        self.adj[v_id1].append(v_id2)

    def removeDirectedEdge(self, point1, point2):
        l = self.adj[point1]
        l_n = []
        for x in l:
            if x is not point2:
                l_n.append(x)
        self.adj[point1] = l_n

    def connect(self, p1, p2):
        if (not p2 in self.adj[p1]) and (not p1 in self.adj[p2]):
            self.addDirectedEdge(p1, p2)
            self.addDirectedEdge(p2, p1)

    def neighbors(self, point):
        return self.adj[point]

    def degree(self, point):
        return len(self.adj[point])

    def removeVertex(self, point):
        self.vertices[point].removed = True
        self.numVertices -= 1

        neighbors = self.adj[point]

        # remove the neighboring directed edges
        for p2 in neighbors:
            self.removeDirectedEdge(p2, point)
            self.removeDirectedEdge(point, p2)

        # get the old triangle id's of the triangles adjacent
        # to the vertex to removed
        old_triangle_ids = [t for t in self.vertices[point].triangles]

        # clockwise list of vertexes around the vertex to remove,
        # i.e. the part we need to retriangulate
        polygon = []

        triangles = []
        for t_id in self.vertices[point].triangles:
            t = self.all_triangles[t_id]
            triangles.append([x for x in t if x is not point])

        nxt = triangles[0]
        polygon.append(nxt[0])
        query = nxt[-1]
        polygon.append(query)
        triangles = triangles[1:]
        for i in range(0, len(neighbors)-2):
            # find the triangle which contains the query point
            for t in triangles:
                if query in t:
                    nxt = t
            old_query = query
            query = nxt[1] if nxt[0] == query else nxt[0]
            polygon.append(query)

            triangles_new = []
            for t in triangles:
                if old_query not in t:
                    triangles_new.append(t)

            triangles = triangles_new

        for t_id in old_triangle_ids:
            t = self.all_triangles[t_id]
            for p in t:
                self.vertices[p].removeTriangle(t_id)
            #self.vertices[t.points[0]].removeTriangle(t_id)
            #self.vertices[t.points[1]].removeTriangle(t_id)
            #self.vertices[t.points[2]].removeTriangle(t_id)

        return {"old_triangles": old_triangle_ids, "polygon": polygon}

    def find_indep_low_deg(self):
        ind_set = []
        forbidden = []
        # add outer triangle at end so that this function does not find the final
        # outter triangle might be a better way to do this...
        for i in range(3, max(3, len(self.vertices))):
            if not self.vertices[i].removed:
                if not i in forbidden:
                    if self.degree(i) <= 8:
                        ind_set.append(i)
                        for n in self.neighbors(i):
                            forbidden.append(n)
        return ind_set

    def removeVertices(self, vs, dag, triangles):
        print("LINE 66 Removing vertices: " + str(vs))
        for v in vs:
            print("Removing vertex: " + str(v))
            # Remove the given vertex
            res = self.removeVertex(v)
            # Remove the old triangles from the triangles
            triangles = [t for t in triangles if not t in res["old_triangles"]]
            # Triangulate the resulting polygon
            new_triangles = triangulate.triangulate(self, res["polygon"])

            triangles = new_triangles + triangles

            # Update DAG
            for o in res["old_triangles"]:
                for n in new_triangles:
                    t1 = simplices.Triangle([self.vertices[p].getPoint() for p in self.all_triangles[o]])
                    t2 = simplices.Triangle([self.vertices[p].getPoint() for p in self.all_triangles[n]])
                    if t1.overlaps(t2):
                        dag.addDirectedEdge(n, o)

            return triangles
