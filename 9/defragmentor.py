from disk import Disk
class Defragmentor:
    def __init__(self, disk):
        self.disk = disk
        self.debug_draw = False

    def set_debug_draw(self, debug_draw):
        self.debug_draw = debug_draw
        
    def defragment(self, whole_file=False):
        if whole_file:
            self._defragment_whole_file()
        else:
            self._defragment_individual_blocks()

    def _defragment_whole_file(self):
        pass

    def fragments_exist(self):
        return any(slot.has_free_blocks() for slot in self.disk.get_all_slots())
    
    def _defragment_individual_blocks(self):
        while self.fragments_exist():
            next_file = self.disk.get_last_file()
            next_slot = self.disk.get_first_slot()
            while next_slot and next_slot.has_free_blocks():
                if not next_file.has_content():
                    next_file = self.disk.get_last_file()
                next_slot.pop()
                next_slot.insert(0, next_file.pop())
                if not next_slot.has_free_blocks():
                    next_slot = self.disk.get_first_slot()
                
                if self.debug_draw:
                    print(self.disk)
                    print()
