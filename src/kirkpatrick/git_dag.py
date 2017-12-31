# intended to work on triangle id's... 
class DAG:
    def __init__(self, root=None):
        pass

    def __str__(self):
        ret = "=================================="
        ret += "\nDAG ADJACENCY LIST:\n"
        for x in self.adj_list.keys():
            ret += str(x) + " maps to: ["
            for y in self.adj_list[x]:
                ret += str(y) + ", "
            ret += "] \n"
        ret += "=================================="
        return ret

    def add_root(self, elem):
        pass

    def add_directed_edge(self, v1, v2):
        pass

    def children(self, elem):
        pass 

    # Use condition_fun to trace to bottom
    def find_leaf_where(self, condition_fun):
        pass
