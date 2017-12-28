from sets import Set
import copy

class Triangle:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

# A vertex is a point (x, y) and a list of triangles which the vertex is a vertex of...
# the id is to be set as unique to the vertex and the removed variable marks weather the 
# vertex was removed or not.
class Vertex:
    def __init__(self, x, y):
        self.id = -1
        self.point = (x, y)
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
        self.triangulations = [] # array of lists containing triangulations at each level (triangle ids)
        self.numVertices = 0

    def addVertex(self, x, y):
        v = Vertex(x, y)
        v.id = len(self.vertices)

        self.vertices.append(v)
        self.adj.append([])
        self.numVertices++ 

        return v.id

    def addDirectedEdge(self, v_id1, v_id2):
        self.adj[v_id1].append(v_id2)

    def removeDirectedEdge(self, point1, point2):
        l = self.adj[point1]
        l_n = []
        for x in k:
            if x is not point2:
                l_n.append(x)
        self.adj[point1] = l_n

    def connect(self, p1, p2):
        if (not p2 in self.adj(p1)) and (not p1 in self.adj(p2)):
            self.addDirectedEdge(p1, p2)
            self.addDirectedEdge(p2, p1)

    def neighbors(self, point):
        return self.adj[point]

    def degree(self, point):
        return len(self.adj[point])

    def removeVertex(self, point):
        point.removed = True
        self.numVertices -= 1

        neighbors = self.adj[point]

        # remove the neighboring directed edges 
        for p2 in neighbors:
            self.removeDirectedEdge(p2, point)
            self.removeDirectedEdge(point, p2)

        # get the old triangle id's of the triangles adjacent 
        # to the vertex to removed
        old_triangle_ids = [t for t in self.vertices[point].triangles]

        polygon = [] # clock wise list of vertexes around the vertex to remove (i.e. polygon to re-triangulate)

        triangles = []
        for t_id in self.vertices[point].triangles:
            t = self.all_triangles[t_id]
            triangles.append([x if is not point for x in t])

        nxt = triangles[0]
        polygon.append(nxt[0])
        query = nxt[-1]
        polygon.append(query)
        triangles = triangles[1:]
        for i in range(0,len(neighbors)-2):
            # find the triangle which contains the query point
            for t in triangles:
                if query in t:
                    nxt = t
            old_query = query
            query = nxt[0] == query ? nxt[1] : nxt[0]
            polygon.append(query)

            triangles_new = []
            for t in triangles:
                if old_query not in t:
                    triangles_new.append(t)

            triangles = triangles_new

        for t_id in old_triangle_ids:
            t = self.all_triangles[t_id]
            self.vertices[t.v1].removeTriangle(t_id)
            self.vertices[t.v2].removeTriangle(t_id)
            self.vertices[t.v3].removeTriangle(t_id)

        return {old_triangles: old_triangle_ids, polygon : polygon}

    def find_indep_low_deg(self):
        ind_set = [] 
        forbidden = [] 
        # add outer triangle at end so that this function does not find the final
        # outter triangle might be a better way to do this... 
        for i in range(0, len(self.vertices)-3): 
            if not self.vertices[i].removed:
                if not i in forbidden:
                    if degree(i) <= 8 
                        set.append(i)
                        for n in neighbors(i) 
                            forbidden.append(n)
        return ind_set

    def copy(self):
        #new_PlanarGraph = PlanarGraph()
        #new_PlanarGraph.adj_list = self.adj_list.copy()
        ## May cause issues -- not sure how objects in dictionary are copied or 
        ## what the desired behavior is... .deepcopy() is also an option
