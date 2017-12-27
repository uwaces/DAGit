class PointLocator:

    def __init__(self, polygons):
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

