import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from helpers.point2d import Point2D
from helpers.dfs import DFS

def load_map(file):
    with open(file, 'r') as f:
        map_data = [list(line.strip()) for line in f]
        trail_heads = []
        summits = []
        for row_index, row in enumerate(map_data):
            for col_index, char in enumerate(row):
                if char == '0':
                    trail_heads.append((Point2D(col_index, row_index), char))
                if char == '9':
                    summits.append((Point2D(col_index, row_index), char))
        return map_data, trail_heads, summits

def out_of_bounds(pos, map_data_2d):
    return (pos.y < 0 or pos.y >= len(map_data_2d) or
            pos.x < 0 or pos.x >= len(map_data_2d[0]))

def cell_at(pos, map_data_2d_array):
    return map_data_2d_array[pos.y][pos.x]

def build_graph(map_data_2d):
    graph = {}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for row_index, row in enumerate(map_data_2d):
        for col_index, cell in enumerate(row):
            cur_pos = Point2D(col_index, row_index)
            neighbors = []
            cur_val = int(cell_at(cur_pos, map_data_2d))
            for dx, dy in directions:
                new_pos = Point2D(cur_pos.x + dx, cur_pos.y + dy)
                if out_of_bounds(new_pos, map_data_2d):
                    continue
                neigh_char = cell_at(new_pos, map_data_2d)
                new_val = int(neigh_char)
                if new_val - cur_val == 1:
                    neighbors.append(new_pos)
            graph[cur_pos] = neighbors

    return graph

def score_trails():
    map_data, trail_heads, summits = load_map('input.txt')
    graph = build_graph(map_data)
    summit_positions = [pos for pos, char in summits]
    dfs = DFS(graph)
    trail_head_score_sum = 0
    trail_head_ratings = 0
    for (start_pos, start_char) in trail_heads:
        reachable_summits = set()
        for summit_pos in summit_positions:
            paths = dfs.get_all_paths(start_pos, summit_pos)
            if paths:
                reachable_summits.add(summit_pos)
                trail_head_ratings += len(paths)
        trail_head_score = len(reachable_summits)
        trail_head_score_sum += trail_head_score
    return trail_head_score_sum, trail_head_ratings

trail_head_score_sum, trail_head_ratings = score_trails()

print(trail_head_score_sum)
print(trail_head_ratings)
