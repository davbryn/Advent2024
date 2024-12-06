from collections import defaultdict, deque

class PrintQueue:

    def __init__(self, rules):
        self.print_order = defaultdict(set)
        self.dependencies = defaultdict(set)
        self.load_rules(rules)

    def load_rules(self, rules):
        for l, r in rules:
            self.print_order[l].add(r)
            self.dependencies[r].add(l)

    def is_valid_update(self, update):
        page_index = {page: idx for idx, page in enumerate(update)}
        
        # Check all rules
        for l, dependents in self.print_order.items():
            if l in page_index:  # Only check if `l` is in the update
                l_index = page_index[l]
                for r in dependents:
                    if r in page_index and page_index[r] < l_index:
                        return False
        return True

    '''This was a failure because the actual test data contained cyclical references - But I am not wasting it
        so I will use it in part 2 where I won't need all the data from the data set'''
    def topological_sort(self, update):
        relevant_rules = defaultdict(set)
        relevant_dependencies = defaultdict(set)
        nodes = set(update)

        for node in nodes:
            if node in self.print_order:
                relevant_rules[node] = self.print_order[node].intersection(nodes)
            if node in self.dependencies:
                relevant_dependencies[node] = self.dependencies[node].intersection(nodes)

        # Number of connections coming in to each node
        in_degree = {node: len(relevant_dependencies[node]) for node in nodes}
        queue = deque([node for node in nodes if in_degree[node] == 0])
        sorted_order = []

        while queue:
            node = queue.popleft()
            sorted_order.append(node)
            for dependent in relevant_rules[node]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return sorted_order

    def fix_updates(self, updates):
        fixed_updates = []
        for update in updates:
            if not self.is_valid_update(update):
                fixed_update = self.topological_sort(update)
                fixed_updates.append(fixed_update)
        return fixed_updates

    def find_middle_pages(self, updates):
        middle_pages = []
        for update in updates:
            middle_index = len(update) // 2
            middle_pages.append(int(update[middle_index]))
        return middle_pages