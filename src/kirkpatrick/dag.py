class DAG:
    def __init__(self, root=None):
        # May consider making 2 parallel arrays and keeping the root as the first
        # element -- will make some operations faster... for now roots are maintained
        # in the dictionary
        self.adj_list = dict()
        self.root = root

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
        if elem not in self.adj_list.keys():
            self.adj_list[elem] = set()
        self.root = elem

    def add_directed_edge(self, v1, v2):
        if v1 not in self.adj_list:
            self.adj_list[v1] = set()
        self.adj_list[v1].add(v2)
        if v2 not in self.adj_list:
            self.adj_list[v2] = set()

    def children(self, elem):
        return self.adj_list[elem]

    # Take a value to be the new root and a list of DAGs to be the children
    # returns the new DAG
    def merge(self, value, dag_list):
        pass

    # Use condition_fun to trace to bottom
    def find_leaf_where(self, condition_fun):
        if not condition_fun(self.root):
            return None

        cur = self.root
        while len(self.children(cur)) > 0:
            for v in self.children(cur):
                if condition_fun(v):
                    cur = v
                    break
        return cur

    
