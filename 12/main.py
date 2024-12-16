from sys import stdin

def load_map(file):
    with open(file, 'r') as f:
        return [list(line.strip()) for line in f]

def get_neighbors(y, x, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            neighbors.append((ny, nx))
    return neighbors

def find_plants(grid):
    seen = set()
    plant_map = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (y, x) in seen:
                continue
            plant = []
            moves = [(y, x)]
            while moves:
                move_y, move_x = moves.pop()
                if (move_y, move_x) in seen:
                    continue
                seen.add((move_y, move_x))
                plant.append([move_y, move_x])
                for ny, nx in get_neighbors(move_y, move_x, grid):
                    if grid[ny][nx] == grid[move_y][move_x] and (ny, nx) not in seen:
                        moves.append((ny, nx))
            if plant:
                plant_map.append(plant)
    return plant_map

def calculate_price(plant_map):
    price = 0
    for plant in plant_map:
        corners = set()
        for y, x in plant:
            for dy, dx in [(0.5, 0.5), (-0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]:
                corners.add((y + dy, x + dx))
        corners_count = 0
        for cy, cx in corners:
            variants = [
                [cy - 0.5, cx - 0.5] in plant,
                [cy + 0.5, cx - 0.5] in plant,
                [cy + 0.5, cx + 0.5] in plant,
                [cy - 0.5, cx + 0.5] in plant
            ]
            number = sum(variants)
            if number == 1:
                corners_count += 1
            elif number == 2 and (variants == [True, False, True, False] or variants == [False, True, False, True]):
                corners_count += 2
            elif number == 3:
                corners_count += 1
        price += len(plant) * corners_count
    return price

if __name__ == "__main__":
    grid = load_map('input.txt')
    plant_map = find_plants(grid)
    price = calculate_price(plant_map)
    print(price)
