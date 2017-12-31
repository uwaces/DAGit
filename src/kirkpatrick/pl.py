import sys
import math
from kirkpatrick import planar
from kirkpatrick import dag
from kirkpatrick import triangulate
from kirkpatrick import simplices
from kirkpatrick import poly


class PointLocator:
    def __init__(self, polygons, vizualize=False):
        self.polygons = polygons

        xmin = simplices.Vertex(sys.maxsize, 0)
        xmax = simplices.Vertex(-sys.maxsize - 1, 0)
        ymin = simplices.Vertex(0, sys.maxsize)
        ymax = simplices.Vertex(0, -sys.maxsize - 1)
        for p in polygons:
            for v in p:
                if v.x < xmin.x: xmin = v
                if v.x > xmax.x: xmax = v
                if v.y < ymin.y: ymin = v
                if v.y > ymax.y: ymax = v

        width = xmax.x - xmin.x
        height = ymax.y - ymin.y
        Ox = width / 2 + xmin.x
        tri_left = simplices.Vertex(Ox - width, ymin.y - 1, True)
        tri_right = simplices.Vertex(Ox + width, ymin.y - 1, True)
        tri_top = simplices.Vertex(Ox, ymin.y + height * 2 + 1, True)

        hull = poly.Polygon("Outer Hull (None)", [tri_left, tri_right, tri_top])
        P = planar.PlanarGraph()

        for polygon in polygons:
            # Add vertices to planar graph
            for v in polygon:
                P.add_vertex(v)
            # Build planar graph edges

        for polygon in polygons:
            for v_i in range(1, len(polygon)):
                P.connect(polygon[v_i], polygon[v_i - 1])
                P.connect(polygon[-1], polygon[0])
        for polygon in polygons:
            # Triangulate the vertices not on the big triangle-hull
            triangulate.triangulate(P, polygon)

        for v in hull:
            P.add_vertex(v)
        for v_i in range(1, len(hull)):
            P.connect(hull[v_i], hull[v_i-1])
        P.connect(hull[-1], hull[0])

        alledges = set()
        for p in polygons:
            edges = set()
            for i in range(1, len(p)):
                edges.add(frozenset([p[i], p[i - 1]]))
            edges.add(frozenset([p[-1], p[0]]))
            alledges.add(frozenset(edges))

        union = set()
        for polyedges in alledges:
            union = union.union(polyedges)

        intersections = set()
        for polyedges1 in alledges:
            for polyedges2 in alledges:
                if polyedges1 == polyedges2:
                    continue
                intersections.add(frozenset(polyedges1.intersection(polyedges2)))

        hole_edges = set()
        for edge in union:
            for intersection in intersections:
                if edge in intersection:
                    break
            else:
                hole_edges.add(edge)

        hole = []
        cur_edge = list(hole_edges)[0]
        endpts = lambda s: list(s)
        hole.append(endpts(cur_edge)[0])
        nxt = endpts(cur_edge)[1]
        while nxt != hole[0]:
            hole.append(nxt)
            for s in hole_edges:
                if s != cur_edge and nxt in s:
                    cur_edge = s
                    nxt = [x for x in s if x is not nxt][0]
                    break

        triangulate.triangulate(P, hull, hole)

        file_name = "../test/test"
        fnum = 0

        self.D = dag.DAG()
        ind_set = P.find_indep_low_deg()
        while len(ind_set) > 0:
            fnum += 1
            if vizualize:
                P.make_fig(file_name+str(fnum) + ".svg")
            old_tris, new_tris = P.remove_vertices(ind_set)
            # Update DAG
            for o in old_tris:
                for n in new_tris:
                    if o.overlaps(n):
                        self.D.add_directed_edge(n, o)

            ind_set = P.find_indep_low_deg()

        fnum += 1
        if vizualize:
            P.make_fig(file_name + str(fnum) + ".svg")

        # Set root of the DAG
        last = P.get_last_triangle()
        self.D.add_root(last)

    def query(self, point):
        cf = lambda x: x.contains(point)
        triangle = self.D.find_leaf_where(cf)
        if triangle is None:
            return None
        return triangle.polygon
