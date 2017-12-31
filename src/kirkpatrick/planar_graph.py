from kirkpatrick import simplices
from kirkpatrick import triangulate
import numpy as np
import pylab as pl
from matplotlib import collections  as mc

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
        self.vertices = set()
        self.adj = dict()
        self.all_triangles = set()  # list of triangles
        self.num_vertices = 0

    def make_fig(self, file_name):
        points_x = [p.x for p in self.adj.keys()]
        points_y = [p.y for p in self.adj.keys()]
        lines = []
        for p1, adj in self.adj.items():
            for p2 in adj:
                lines.append([(p1.x, p1.y), (p2.x, p2.y)])

        lc = mc.LineCollection(lines, linewidths=2)

        fig, ax = pl.subplots()
        ax.axis("off")
        ax.add_collection(lc)
        ax.autoscale()
        ax.margins(0.1)
        ax.plot(points_x, points_y, 'ro')

        fig.savefig(file_name)

    def addVertex(self, x, y, hull_member=False):
        v = simplices.Vertex(x, y, hull_member)
        self.vertices.add(v)
        self.adj[v] = set()
        self.num_vertices += 1
        return v

    def addEdge(self, v1, v2):
        self.adj[v1].add(v2)
        self.adj[v2].add(v1)

    def removeEdge(self, v1, v2):
        self.adj[v1].remove(v2)
        self.adj[v2].remove(v1)

    def connect(self, p1, p2):
        if (not p2 in self.adj[p1]) and (not p1 in self.adj[p2]):
            self.addEdge(p1, p2)

    def neighbors(self, v):
        return self.adj[v]

    def degree(self, v):
        return len(self.adj[v])

    def get_last_triangle(self):
        if self.num_vertices != 3:
            return None
        else:
            t = None
            for x in self.vertices:
                for y in x.triangles:
                    t = y
                    break
                break
        return t

    def removeVertex(self, v):
        self.vertices.remove(v)
        self.num_vertices -= 1

        # shallow copy set since we're removing stuff from self.adj
        neighbors = set(self.adj[v])

        # remove the neighboring directed edges
        for p in neighbors:
            self.removeEdge(p, v)

        # get the triangles v was a part of; shallow copy
        v_tris = [t for t in v.triangles]

        # clockwise list of vertexes around the vertex to remove,
        # i.e. the part we need to retriangulate
        hull = []

        cur_t = v_tris[0]
        endpts = lambda t: [x for x in t if x is not v]
        hull.append(endpts(cur_t)[0])
        nxt = endpts(cur_t)[1]
        while nxt != hull[0]:
            hull.append(nxt)
            for t in v_tris:
                if t != cur_t and nxt in endpts(t):
                    cur_t = t
                    nxt = [x for x in endpts(t) if x is not nxt][0]
                    break

        for t in v_tris:
            for x in t:
                x.removeTriangle(t)

        return v_tris, hull

    def find_indep_low_deg(self):
        ind_set = set()
        forbidden = set()
        # add outer triangle at end so that this function does not find the
        # final outter triangle might be a better way to do this
        for v in self.vertices:
            if not v in forbidden and not v.hull_member:
                if self.degree(v) <= 8:
                    ind_set.add(v)
                    for n in self.neighbors(v):
                        forbidden.add(n)
        return ind_set

    def removeVertices(self, vs):
        for v in vs:
            # Remove the given vertex
            old_tris, hull = self.removeVertex(v)

            # Triangulate the resulting polygon
            new_tris = triangulate.triangulate(self, hull)

            return old_tris, new_tris
