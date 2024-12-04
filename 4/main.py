def load_grid(input_file):
    with open(input_file, 'r') as file:
        grid = [list(line.strip()) for line in file if line.strip()]
    return grid

def count_word_in_direction(grid, word, x, y, dx, dy):
    for i, char in enumerate(word):
        nx, ny = x + dx * i, y + dy * i
        if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
            return 0  # Out of bounds
        if grid[nx][ny] != char:
            return 0  # Character mismatch
    return 1  # Word found in this direction

def count_straight_words_in_grid(word, grid):
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Up-left, Up, Up-right
        (0, -1),          (0, 1),    # Left,       Right
        (1, -1),  (1, 0), (1, 1)     # Down-left, Down, Down-right
    ]
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == word[0]: # Start of the word
                for dx, dy in directions:
                    count += count_word_in_direction(grid, word, x, y, dx, dy)
    return count

def count_crossed_word_in_grid(word, grid):
    conv_filter_dir = [
        (-1, -1),       (-1, 1),  # Up-left, Up, Up-right
        (1, -1),        (1, 1)     # Down-left, Down, Down-right
    ]

    num_crosses = 0
    for x in range(1, len(grid)-1):
        for y in range(1, len(grid[0])-1):
            if grid[x][y] == 'A': # Central 'A
                count = 0
                for dx, dy in conv_filter_dir:
                    count += count_word_in_direction(grid, word, x + dx, y + dy, -dx, -dy)
                if count == 2:  # Make sure we found two words
                    num_crosses += 1
    return num_crosses

# Example usage:
grid = load_grid('input.txt')
print(count_straight_words_in_grid('XMAS', grid)) # Puzzle 1
print(count_crossed_word_in_grid('MAS', grid))  # Puzzle 2