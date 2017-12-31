from kirkpatrick import planar
from kirkpatrick import dag
from kirkpatrick import triangulate
import functools


class PointLocator:
    def __init__(self, polygon, hull, vizualize=False):
        self.polygon = polygon
        self.hull = hull
#        # triangulate each polygon
#        trangs = [p.triangluate() for p in polygons]
#        # merge triangulations into one triangulation
#        T = functools.reduce(lambda a,b: a.merge(b), trangs, None)
#        # TODO: possibly add 3 dummy points at extremes to fix convex hull

        P = planar.PlanarGraph()
        # Add vertices to planar graph
        [P.addVertex(p) for p in hull]
        [P.addVertex(p) for p in polygon]
        # Build planar graph edges
        for v_i in range(1, len(polygon)):
            P.connect(polygon[v_i], polygon[v_i-1])
            P.connect(polygon[-1], polygon[0])
        # Connect up the outer triangle-hull
        for v_i in range(1, len(hull)):
            P.connect(hull[v_i], hull[v_i-1])
        P.connect(hull[-1], hull[0])

        # Triangulate the vertices not on the big triangle-hull
        triangulate.triangulate(P, polygon)
        triangulate.triangulate(P, hull, polygon)

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

    def query(self, point):
        cf = lambda x: x.contains(point)
        return self.D.find_leaf_where(cf)
