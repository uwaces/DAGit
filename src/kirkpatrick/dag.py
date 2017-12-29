# intended to work on triangle id's... 
class DAG:
    def __init__(self):
        # May consider making 2 parallel arrays and keeping the root as the first
        # element -- will make some operations faster... for now roots are maintained
        # in the dictionary
        self.adj_list = dict()
    
    def addRoot(id_elem):
        self.adj_list[id_elem] = [True, []]

    def addDirectedEdge(id1, id2):
        if id1 not in self.adj_list:
            self.adj_list[id1] = [False, [id2]]
        else:
            self.adj_list[id1][1].append(id2)

    def children(id_elem):
        return self.adj_list[id_elem][1]

    def root():
        root = None
        for x in self.adj_list:
            if self.adj_list[x][0]:
                root = x

        return root

    # Take a value to be the new root and a list of DAGs to be the children
    # returns the new DAG
    def merge(self, value, dag_list):
        pass

    # Use condition_fun to trace to bottom
    def find_leaf_where(self, condition_fun):
        if not condition_fun(self.root()):
            return None
            
        cur = self.root()
        
        while not children(id_elem):
            for v in cur.children:
                if condition_fun(v):
                    cur = v
                    break
        return cur

        


# DAG OF TRIANGLES:
