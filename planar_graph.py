from sets import Set
import copy

class PlanarGraph:

    def __init__(self):
        self.adj_list = dict()        

    def add_point(self, point, edges):
        self.adj_list[point] = edges

    def remove_point(self, point):
        del self.adj_list[point]

    def find_indep_low_deg(self):
        independant_set = set()
        for point, edges in self.adj_list.items():
            if len(edges) =< 8:
                is_indep = True
                for e in edges:
                    is_indep = is_indep and (e not in independant_set)
                if is_indep:
                    independant_set.add(point)
        return independant_set

    def copy(self):
        new_PlanarGraph = PlanarGraph()
        new_PlanarGraph.adj_list = self.adj_list.copy()
        ## May cause issues -- not sure how objects in dictionary are copied or 
        ## what the desired behavior is... .deepcopy() is also an option
