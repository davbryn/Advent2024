
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
    while not out_of_bounds(next_pos, map_2d_array):
        if cell_at(next_pos, map_2d_array) == '#':
            dir.rotate_90()
        else:
            pos += dir
            if cell_at(pos,map_2d_array) == '.':
                cells_visited += 1
                map_2d_array[pos.y][pos.x] = 'X'
        next_pos = pos + dir
        if debug_draw: draw_map(map_2d_array)
        
    print(cells_visited)

def place_printing_press(map_2d_array, pos, dir, debug_draw=False):
    loopable_places = 0
    cells_visited = 1 # Start position
    next_pos = pos + dir
    map_2d_array[pos.y][pos.x] = 'X'
    map_2d_history = [[Point2D(0, 0) for _ in row] for row in map_2d_array]
    while not out_of_bounds(next_pos, map_2d_array):
        
                
        if cell_at(next_pos, map_2d_array) == '#':
            dir.rotate_90()
        else:
            pos += dir
            if cell_at(pos,map_2d_array) == '.':
                cells_visited += 1
                map_2d_array[pos.y][pos.x] = 'X'
                map_2d_history[pos.y][pos.x] = Point2D(dir.x, dir.y)
        

        #if turning right puts me on a path I've already visited (in the same direction)
        # I would be in a loop if I put a Printing Press in front of me.
        if cell_at(next_pos, map_2d_array) != '#':
            probe_dir = Point2D(dir.x, dir.y)
            probe_dir.rotate_90()
            probe_pos = pos + probe_dir
            while not out_of_bounds(probe_pos, map_2d_array):
                if cell_at(probe_pos, map_2d_history) == probe_dir:
                    printing_press_pos = pos + dir
                    print(f"Printing Press at {printing_press_pos}")
                    loopable_places += 1
                    break 
                probe_pos = probe_pos + probe_dir
        if debug_draw: draw_map(map_2d_array)

        next_pos = pos + dir

        
    print(cells_visited)
    print(loopable_places)

def puzzle1():
    map_2d_array, pos = load_map('input.txt')
    dir = Point2D(0, -1)
    walk_map(map_2d_array, pos, dir)

def puzzle2():
    map_2d_array, pos = load_map('input.txt')
    dir = Point2D(0, -1)
    #if turning right puts me on a path I've already visited (in the same direction)
    # I would be in a loop if I put a Printing Press in front of me.
    place_printing_press(map_2d_array, pos, dir, debug_draw=False)

puzzle2()