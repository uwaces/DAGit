from kirkpatrick import planar_graph
from kirkpatrick import dag
from kirkpatrick import triangulate
import functools


class PointLocator:
    def __init__(self, polygon, hull, vizualize=False):
        self.polygon = polygon
#        # triangulate each polygon
#        trangs = [p.triangluate() for p in polygons]
#        # merge triangulations into one triangulation
#        T = functools.reduce(lambda a,b: a.merge(b), trangs, None)
#        # TODO: possibly add 3 dummy points at extremes to fix convex hull

        P = planar_graph.PlanarGraph()
        # Add vertices to planar graph
        hull = [P.addVertex(p[0], p[1], True) for p in hull]
        vertices = [P.addVertex(p[0], p[1]) for p in polygon]
        # Build planar graph edges
        for v_i in range(1, len(vertices)):
            P.connect(vertices[v_i], vertices[v_i-1])
            P.connect(vertices[-1], vertices[0])
        # Connect up the outer triangle-hull
        for v_i in range(1, len(hull)):
            P.connect(hull[v_i], hull[v_i-1])
        P.connect(hull[-1], hull[0])

        # Triangulate the vertices not on the big triangle-hull
        triangulate.triangulate(P, vertices)
        triangulate.triangulate(P, hull, vertices)

        file_name = "../test/test"
        fnum = 0

        self.D = dag.DAG()
        ind_set = P.find_indep_low_deg()
        while len(ind_set) > 0:
            fnum += 1
            if vizualize:
                P.make_fig(file_name+str(fnum) + ".png")
            old_tris, new_tris = P.removeVertices(ind_set)
            # Update DAG
            for o in old_tris:
                for n in new_tris:
                    if o.overlaps(n):
                        self.D.addDirectedEdge(n, o)

            ind_set = P.find_indep_low_deg()

        fnum += 1
        if vizualize:
            P.make_fig(file_name + str(fnum) + ".png")

        # Set root of the DAG
        last = P.get_last_triangle()
        self.D.addRoot(last)
        print(self.D)
        print("Last Triangle: " + str(last))

    def query(self, point):
        cf = lambda x: x.contains(point)
        return self.D.find_leaf_where(cf)
