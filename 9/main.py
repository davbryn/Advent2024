import re

def load_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return list(file.read())
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    
def build_files_and_spaces(disk_map):
    disk = []
    disk_count = -1
    for index, size_of_block in enumerate(disk_map):
        file = []
        if index % 2 == 0:
            disk_count += 1
            label = str(disk_count)
        else:
            label = '.'
        for _ in range(int(size_of_block)):
            file.append(label)
        if len(file) > 0: disk.append(file) 
    return disk

def as_string(disk):   
    return ''.join(''.join(file) for file in disk)

def debug_draw_disk(disk):
    print(as_string(disk))

def checksum(disk):
        checksum = 0
        counter = 0
        for file in disk:
            for value in file:
                    if value != '.': checksum += counter * int(value)
                    counter += 1
        return checksum


""" Assuming for the purposes of a disk fragmenter that we want to be operating 
    on a mutable data structure and perform the file movement in the same momory space
    So I won't be making a copy of the data """
def defragment(disk):

    def first_gap():
        for index, file in enumerate(disk):
            if len(file) == 0:
                continue
            if file[0] == '.':
                return disk[index]
        return None
    def count_gaps(disk):
        s = as_string(disk)
        return len(re.findall(r'\.+', s))
    def last_file():
        last_index = None
        for index, file in enumerate(disk):
            if file[0] != '.':
                last_index = index
        return disk[last_index]
    def is_defragmented():
        s = as_string(disk)
        has_seen_dot = False

        for char in s:
            if char == '.':
                has_seen_dot = True  # Once we encounter a dot, all subsequent characters must be dots
            elif has_seen_dot and char.isdigit():
                return False  # A digit after a dot means it's not defragmented

        return True
    
    
    gap = first_gap()
    file_to_move = last_file()
    files_moved = 0
    while gap is not None and file_to_move is not None:
        print("Gaps remaining: ", count_gaps(disk))
        if is_defragmented():
           break
        for index, space in enumerate(gap):
            file_index = len(file_to_move) - files_moved - 1
            if space == '.':
                gap[index] = file_to_move[file_index]
                file_to_move[file_index] = '.'
                files_moved += 1
                if files_moved == len(file_to_move):
                    file_to_move = last_file()
                    files_moved = 0
        gap = first_gap()
        #debug_draw_disk(disk)

disk_map = load_text_from_file('input.txt')
#disk_map = list('2333133121414131402')
disk = build_files_and_spaces(disk_map)
debug_draw_disk(disk)
defragment(disk)
debug_draw_disk(disk)
print(checksum(disk))
