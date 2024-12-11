
from disk import Disk
from defragmentor import Defragmentor

def load_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return [int(char) for char in file.read().strip()]

            
                
def build_disk(disk_map):
    disk = Disk()
    for index, size in enumerate(disk_map):
        if index % 2 == 0:  # Even index: add File
            disk.add_file(size)
        else:  # Odd index: add Slot
            disk.add_slot(size)
    return disk

def checksum(disk): # Move this to the Disk class
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
#def defragment(disk, whole_file=False):

disk_map = load_text_from_file('input.txt')
disk_map = [2,3,3,3,1,3,3,1,2,1,4,1,4,1,3,1,4,0,2]
disk = build_disk(disk_map)
print(disk) 
print(f"Number of files: {disk.num_files()}")
print(f"Number of slots: {disk.num_slots()}")
defragmentor = Defragmentor(disk)
defragmentor.set_debug_draw(True)
defragmentor.defragment(whole_file=False)

#debug_draw_disk(disk)
#defragment(disk, whole_file=True)
#debug_draw_disk(disk)
#print(checksum(disk))
