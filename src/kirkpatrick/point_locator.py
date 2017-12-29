import functools


class PointLocator:
    def __init__(self, polygons):
        self.polygons = polygons
        # triangulate each polygon
        trangs = [p.triangluate() for p in polygons]
        # merge triangulations into one triangulation
        T = functools.reduce(lambda a,b: a.merge(b), trangs, None)
        # TODO: possibly add 3 dummy points at extremes to fix convex hull
        # treat triangulation as planar graph
        P = PlanarGraph(T)
        # initialize dag as a forest
        self.D = DAG()
        for t in T.triangles():
            D.add_vertex(t, None)
        while True:
            S = P.find_indep_low_deg()
            Tc = T.copy()
            Pc = P.copy()
            for v in S:
                Tc.remove_point(v.value)
                Pc.remove_vertex(v)
            # TODO: retriangulate both efficiently
            # TODO: look for overlaps and add to D


    def query(point):
        cf = lambda x: x.value.contains(point)
        return self.D.find_leaf_where(cf)
