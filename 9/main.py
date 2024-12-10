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

def defragment(disk):

    def first_gap():
        for index, file in enumerate(disk):
            if len(file) == 0:
                continue
            if file[0] == '.':
                return disk[index]
        return None
    def last_file():
        last_index = None
        for index, file in enumerate(disk):
            if file[0] != '.':
                last_index = index
        return disk[last_index]
    def is_defragmented():
        pattern = r'^\d+\.{0,}$'  # Matches one or more digits followed by zero or more '.'
        return bool(re.fullmatch(pattern, as_string(disk)))
    
    gap = first_gap()
    file_to_move = last_file()
    files_moved = 0
    while gap is not None and file_to_move is not None:
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
        debug_draw_disk(disk)
        
        

    return True
    


disk_map = load_text_from_file('input.txt')
disk = build_files_and_spaces(disk_map)
debug_draw_disk(disk)
defragment(disk)
debug_draw_disk(disk)