from kirkpatrick import planar
from kirkpatrick import dag
from kirkpatrick import triangulate


class PointLocator:
    def __init__(self, polygons, hull, vizualize=False):
        self.polygons = polygons
        self.hull = hull

        P = planar.PlanarGraph()

        for polygon in polygons:
            # Add vertices to planar graph
            for v in polygon:
                P.add_vertex(v)
            # Build planar graph edges
            for v_i in range(1, len(polygon)):
                P.connect(polygon[v_i], polygon[v_i - 1])
                P.connect(polygon[-1], polygon[0])
            # Triangulate the vertices not on the big triangle-hull
            triangulate.triangulate(P, polygon)

        for v in hull:
            P.add_vertex(v)
        for v_i in range(1, len(hull)):
            P.connect(hull[v_i], hull[v_i-1])
        P.connect(hull[-1], hull[0])
        triangulate.triangulate(P, hull, [v for p in polygons for v in p])

        file_name = "../test/test"
        fnum = 0

        self.D = dag.DAG()
        ind_set = P.find_indep_low_deg()
        while len(ind_set) > 0:
            fnum += 1
            if vizualize:
                P.make_fig(file_name+str(fnum) + ".png")
            old_tris, new_tris = P.remove_vertices(ind_set)
            # Update DAG
            for o in old_tris:
                for n in new_tris:
                    if o.overlaps(n):
                        self.D.add_directed_edge(n, o)

            ind_set = P.find_indep_low_deg()

        fnum += 1
        if vizualize:
            P.make_fig(file_name + str(fnum) + ".png")

        # Set root of the DAG
        last = P.get_last_triangle()
        self.D.add_root(last)
        print(self.D)

    def query(self, point):
        cf = lambda x: x.contains(point)
        triangle = self.D.find_leaf_where(cf)
        if triangle is None:
            return None
        return triangle.polygon
