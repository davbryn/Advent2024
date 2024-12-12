class DFS:
    def __init__(self, graph=None):
        self.graph = graph if graph is not None else {}
        self.visited = set()

    def set_graph(self, graph):

        self.graph = graph
        self.visited = set()

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




