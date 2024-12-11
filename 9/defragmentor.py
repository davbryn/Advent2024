from disk import Disk
class Defragmentor:
    def __init__(self, disk):
        self.disk = disk

    def defragment(self, whole_file=False):
        if whole_file:
            self._defragment_whole_file()
        else:
            self._defragment_individual_files()

    def _defragment_whole_file(self):
        flattened_disk = [block for file in self.disk for block in file if block != '.']
        index = 0
        for file in self.disk:
            for i in range(len(file)):
                if file[i] != '.':
                    file[i] = flattened_disk[index]
                    index += 1
                else:
                    file[i] = '.'

    def _defragment_individual_files(self):
        for file in self.disk:
            blocks = [block for block in file if block != '.']
            for i in range(len(file)):
                if i < len(blocks):
                    file[i] = blocks[i]
                else:
                    file[i] = '.'

    def defragment(disk, whole_file=False):
        defragmentor = Defragmentor(disk)
        defragmentor.defragment(whole_file)