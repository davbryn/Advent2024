import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from helpers.point2d import Point2D

def load_map(file):
    with open(file, 'r') as f:
        map_data = [list(line.strip()) for line in f]
        antennas = list([(Point2D(y, x), char) for x, row in enumerate(map_data) for y, char in enumerate(row) if char != '.'])
    return map_data, antennas

def draw_map(map_data_2d_array):
    for line in map_data_2d_array:
        print(''.join(line))
    print('\n')

def out_of_bounds(pos, map_data_2d_array):
    return pos.x < 0 or pos.x >= len(map_data_2d_array) or pos.y < 0 or pos.y >= len(map_data_2d_array[0])

def cell_at(pos, map_data_2d_array):
    return map_data_2d_array[pos.y][pos.x]

def frequency_finder(infinite_broadcast=False, condition=lambda x: x == '#'):
    map_data, antennas = load_map('input.txt')

    def broadcast_signal(start, target, infinite_broadcast):
        """Broadcast signal from one antenna to another."""
        scalar = 1
        distance = Point2D.distance(start, target)  # Precompute distance
        while True:
            anti_node = start + distance * scalar  # Calculate the next anti-node position
            if out_of_bounds(anti_node, map_data):
                break  # Stop if out of bounds
            map_data[anti_node.y][anti_node.x] = '#'  # Mark the map
            if not infinite_broadcast:
                break  # Stop after one broadcast unless infinite_broadcast is True
            scalar += 1  # Move to the next scalar if infinite_broadcast is enabled

    # Process all antenna pairs
    for (pos_a, freq_a) in antennas:
        for (pos_b, freq_b) in antennas:
            if pos_a != pos_b and freq_a == freq_b:
                broadcast_signal(pos_a, pos_b, infinite_broadcast)

    draw_map(map_data)
    return sum(1 for row in map_data for char in row if condition(char))


    
print(frequency_finder(infinite_broadcast=False, condition=lambda x: x == '#'))
print(frequency_finder(infinite_broadcast=True, condition=lambda x: x != '.'))