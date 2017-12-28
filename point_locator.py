import earcut  ## this allows us to add holes
import numpy as np
class PointLocator:

    def __init__(self, polygons):
        # Assumed to be an array of 2 element arrays
        self.polygons = polygons
        

    def query(point):
        """
        Get as input a list of polygons
        triangulate each polygon
        merge triangulations into one triangulation
        initialize dag as a forest
        find independent set of low degree vertices
        copy triangulation
        remove ind set
        retriangulate
        look for overlaps and add to dag
        """
        # Make points a set() so we don't duplicate them
        points = set()
        # Edges can be tuples of points (check weather each order is present and
        # add to set only if not)
        edges  = set()
        # Make a list of triangles to start DAG
        triangles = list()

        for p in self.polygons:
            points = np.array(p)
            
            list.add(tri)

        for t in triangles:
            for p in t:
                points.add(p)



