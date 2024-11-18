class TreeNode:
    def __init__(self, data, cords=(0, 0)):
        self.data = data
        self.children = []
        self.parent = None
        self.cords = cords
        self.visited = False
        self.base_cost = self.set_base_cost(data)
        self.cost = float('inf')  

    def set_base_cost(self, data):
        if data == 'C':
            return 1
        elif data == ' ':
            return 1
        elif data == 'R':
            return 0
        elif data == "G":
            return 100
        return 0

    def update_cost(self):
        if self.parent:
            self.cost = self.base_cost + self.parent.cost
        else:
            self.cost = self.base_cost
    def add_child(self, child):
        child.parent = self
        child.cost = child.base_cost
        self.children.append(child)

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + str(self.cords))
        if self.children:
            for child in self.children:
                child.print_tree()
    
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    def propagate_cost_update(self):
        """Propaga la actualización del costo a todos los descendientes."""
        self.update_cost()
        for child in self.children:
            child.propagate_cost_update()
    def get_path_to_root(self):
        path = []
        current = self
        while current is not None:
            path.append(current.cords)  # Puedes cambiar esto a `current.data` si prefieres los datos
            current = current.parent
        return path[::-1]
    # Para la implementacion de UCS
    def __lt__(self, other):
        return self.cost < other.cost
    def __le__(self, other):
        return self.cost <= other.cost
    