import pygame

def load_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def build_memory_and_blocks(data: str):
    counts = list(map(int, data.strip()))
    memory = []
    blocks = []
    block_id = 0
    current_index = 0

    for i, count in enumerate(counts):
        if i % 2 == 0:  # Blocks
            memory.extend([block_id] * count)
            blocks.append((block_id, count, current_index))
            block_id += 1
        else:  # Spaces
            memory.extend(["."] * count)
        current_index += count
    
    return memory, blocks

def compute_checksum(memory):
    return sum(i * val for i, val in enumerate(memory) if val != ".")

def defragment_using_partial_blocks(initial_memory, blocks):
    memory = initial_memory[:]
    for block_id, block_size, block_start in reversed(blocks):
        filled = 0
        for i in range(block_start):
            if memory[i] == "." or memory[i] == block_id:
                memory[i] = block_id
                filled += 1
                if filled == block_size:
                    break

        # Clear the old position of the block
        for i in range(filled):
            memory[block_start + block_size - i - 1] = "."

    return memory

def defragment_using_whole_blocks(initial_memory, blocks):
    memory = initial_memory[:]
    for block_id, block_size, block_start in reversed(blocks):
        empty_count = 0
        space_start = -1

        # Find enough space for the block
        for i in range(block_start):
            if memory[i] == ".":
                empty_count += 1
                if empty_count == block_size:
                    space_start = i - block_size + 1
                    break
            else:
                empty_count = 0
                space_start = -1

        # If we found a spot moe the block there
        if space_start != -1:
            for offset in range(block_size):
                memory[space_start + offset] = block_id
                memory[block_start + offset] = "."

    return memory


data = load_text_from_file("input.txt")
initial_memory, blocks = build_memory_and_blocks(data)
puzzle1_result = defragment_using_partial_blocks(initial_memory, blocks)
puzzle2_result = defragment_using_whole_blocks(initial_memory, blocks)
print(compute_checksum(puzzle1_result))
print(compute_checksum(puzzle2_result))
