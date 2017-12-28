class Vertex:
    def __init__(self, is_root, children, value):
        self.is_root = is_root
        self.children = children
        self.value = value

    def is_root(self):
        return self.is_root

    def is_leaf(self):
        return children is []

class DAG:
    def __init__(self, value, children=[], is_root=True):
        self.root = Vertex(is_root, children, value)
        
    def merge(self, value, dag_list):
        for x in dag_list:
            x.root.is_root = False
        root_list = [x.root for x in dag_list]
        new_DAG = DAG(value, children=root_list)
        return new_DAG

    # Use condition_fun to trace to bottom
    def find_leaf_where(self, condition_fun):
        if not condition_fun(self.root):
            return None

        cur = self.root

        while not cur.is_leaf():
            for v in cur.children:
                if condition_fun(v):
                    cur = v
                    break
        return cur

        
