#class Vertex:
#    def __init__(self, is_root, children, value):
#        self.is_root = is_root
#        self.children = children
#        self.value = value
#
#    def is_root(self):
#        return self.is_root
#
#    def is_leaf(self):
#        return children is []

# intended to work on triangle id's... 
class DAG:
    def __init__(self, id_elem):
        # May consider making 2 parallel arrays and keeping the root as the first
        # element -- will make some operations faster... for now roots are maintained
        # in the dictionary
        self.adj_list = dict()
        self.addRoot(id_elem)
    
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
        # Don't think we need this??

    # Use condition_fun to trace to bottom
    def find_leaf_where(self, condition_fun):
        ## We'll see... 
        pass
        #if not condition_fun(self.root):
        #    return None
        #    
        #cur = self.root
        #
        #while not cur.is_leaf():
        #    for v in cur.children:
        #        if condition_fun(v):
        #            cur = v
        #            break
        #return cur

        


# DAG OF TRIANGLES:
