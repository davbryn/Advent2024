
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from helpers.point2d import Point2D

def load_map(file):
    with open(file, 'r') as f:
        map = [list(line.strip()) for line in f]
        pos = next(Point2D(y, x) for x, row in enumerate(map) for y, char in enumerate(row) if char == '^')
    return map, pos

def draw_map(map_2d_array):
    for line in map_2d_array:
        print(''.join(line))
    print('\n')

def out_of_bounds(pos, map_2d_array):
    return pos.x < 0 or pos.x >= len(map_2d_array) or pos.y < 0 or pos.y >= len(map_2d_array[0])

def cell_at(pos, map_2d_array):
    return map_2d_array[pos.y][pos.x]

def puzzle1():
    map_2d_array, pos = load_map('input.txt')
    draw_map(map_2d_array)
    dir = Point2D(0, -1)
    cells_visited = 1 # Start position
    next_pos = pos + dir
    while not out_of_bounds(next_pos, map_2d_array):
        if cell_at(next_pos, map_2d_array) == '#':
            dir.rotate_90()
        else:
            pos += dir
            if cell_at(pos,map_2d_array) == '.':
                cells_visited += 1
                map_2d_array[pos.y][pos.x] = 'X'
        next_pos = pos + dir
        draw_map(map_2d_array)
        
    print(cells_visited)


puzzle1()