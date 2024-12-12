class DFS:
    def __init__(self, graph=None):
        self.graph = graph if graph is not None else {}
        self.visited = set()

    def set_graph(self, graph):
        self.graph = graph
        self.visited = set()

    def run(self, start_node):
        self.visited = set()
        order = []
        self._dfs_recursive(start_node, order)
        return order

    def _dfs_recursive(self, node, order):
        if node in self.visited:
            return
        self.visited.add(node)
        order.append(node)
        for neighbor in self.graph.get(node, []):
            if neighbor not in self.visited:
                self._dfs_recursive(neighbor, order)

    def get_all_paths(self, start, goal):
        results = []
        
        def backtrack(path):
            current = path[-1]
            if current == goal:
                results.append(path[:])
                return
            for neighbor in self.graph.get(current, []):
                if neighbor not in path:
                    path.append(neighbor)
                    backtrack(path)
                    path.pop()

        backtrack([start])
        return results
