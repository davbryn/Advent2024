
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

def walk_map(map_2d_array, pos, dir, debug_draw=False):
    cells_visited = 1 # Start position
    next_pos = pos + dir
    map_2d_array[pos.y][pos.x] = 'X'
    chosen_path = [Point2D(dir.x, dir.y)]
    rot_count = 0
    while not out_of_bounds(next_pos, map_2d_array):
        if cell_at(next_pos, map_2d_array) == '#':
            dir.rotate_90()
            rot_count += 1
        else:
            pos += dir
            if cell_at(pos,map_2d_array) == '.':
                cells_visited += 1
                map_2d_array[pos.y][pos.x] = 'X'
                chosen_path.append(Point2D(pos.y, pos.x))
                rot_count = 0
        
        if debug_draw: draw_map(map_2d_array)
        next_pos = pos + dir
        if rot_count > 4:
            print('Loop detected')
            return None

    return chosen_path

def puzzle1():
    map_2d_array, pos = load_map('input.txt')
    dir = Point2D(0, -1)
    walk_map(map_2d_array, pos, dir)

def puzzle2():
    map_2d_array, pos = load_map('input.txt')
    dir = Point2D(0, -1)
    #if turning right puts me on a path I've already visited (in the same direction)
    # I would be in a loop if I put a Printing Press in front of me.
    path_walked = walk_map(map_2d_array, pos, dir, debug_draw=False)
    steps = len(path_walked)
    print('steps ' + str(steps))
    num_danger_nodes = 0
    for enum, cell in enumerate(path_walked):
        print('percentage ' + str((enum/steps) * 100))
        if enum == 0:
            continue
        map, pos = load_map('input.txt')
        map[cell.x][cell.y] = '#'
        dir = Point2D(0, -1)
        length_of_walk = walk_map(map, pos, dir, debug_draw=False)
        if length_of_walk is None:
            num_danger_nodes += 1
        
    print('num_danger_nodes ' + str(num_danger_nodes)) 
puzzle2()