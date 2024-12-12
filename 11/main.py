def apply_rule(stone):
    # stone is an integer
    label = str(stone)
    if stone == 0:
        return [1]
    elif len(label) % 2 == 0:
        mid = len(label) // 2
        stone_a = int(label[:mid])
        stone_b = int(label[mid:])
        return [stone_a, stone_b]
    else:
        return [stone * 2024]

def count_stones(stone, steps, cache):
    if steps == 0:
        return 1  

    key = (stone, steps)
    if key in cache:
        return cache[key]

    transformed = apply_rule(stone)
    total = 0
    for s in transformed:
        total += count_stones(s, steps - 1, cache)

    cache[key] = total
    return total

'''
Can't keep calculating the same stones over and over again.
Since we will see a lot of the same numbers appearing in the tree of stones,
and their children will be identical we can cache the results and use those to
sum up the parts and skip the calculations
'''
def puzzle2(start_stones, steps=75):
    cache = {}
    total = 0
    for stone in start_stones:
        total += count_stones(stone, steps, cache)
    return total





def puzzle1(start_stones):
    stones = start_stones

    for i in range(25):
        stones = [
            item 
            for sublist in stones 
            for item in (sublist if isinstance(sublist, list) else [sublist])
        ]
        print(stones)
        print()
        new_stones = []
        for stone in stones:
            transformed = apply_rule(stone)
            if isinstance(transformed, list):
                new_stones.append(transformed)
            else:
                new_stones.append([transformed])
        stones = new_stones
    stones = [
        item 
        for sublist in stones 
        for item in (sublist if isinstance(sublist, list) else [sublist])
    ]

    return len(stones)

input_data = [4, 4841539, 66, 5279, 49207, 134, 609568, 0]
print(puzzle2(input_data, 75))
