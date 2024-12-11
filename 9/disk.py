class Chunk:
    def __init__(self, content):
        self.content = list(content)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]

    def __setitem__(self, index, value):
        self.content[index] = value

    def __str__(self):
        return ''.join(self.content)
    
    def insert(self, index, value):
        self.content.insert(index, value)

    def pop(self, index=-1):
        return self.content.pop(index)

    def append(self, value):
        self.content.append(value)
    
    def has_content(self):
        return len(self.content) > 0
    
    def has_free_blocks(self):
        return any(char == '.' for char in self.content)
    

class Slot(Chunk):
    def __init__(self, size):
        super().__init__('.' * size)

class File(Chunk):
    def __init__(self, id_num, size):
        super().__init__(str(id_num) * size)  # Use file ID for its content
        self.id_num = id_num  # Store file ID


class Disk:
    def __init__(self):
        self.chunks = []
        self.file_id_counter = 0  # Initialize file ID counter
    
    def add_slot(self, size):
        """Add a Slot of the given size to the disk."""
        self.chunks.append(Slot(size))
    
    def add_file(self, size):
        """Add a File with auto-assigned ID to the disk."""
        file_chunk = File(self.file_id_counter, size)  # Automatically assign ID
        self.file_id_counter += 1
        self.chunks.append(file_chunk)
    
    def num_chunks(self):
        return len(self.chunks)
    
    def num_slots(self):
        return sum(1 for chunk in self.chunks if isinstance(chunk, Slot))
    
    def num_files(self):
        return sum(1 for chunk in self.chunks if isinstance(chunk, File))

    def __str__(self):
        return ''.join(str(chunk) for chunk in self.chunks)
    
    def get_all_slots(self):
        return [chunk for chunk in self.chunks if isinstance(chunk, Slot)]
    
    def get_all_files(self):
        return [chunk for chunk in self.chunks if isinstance(chunk, File)]  
    
    def get_last_file(self):
        for chunk in reversed(self.chunks):
            if isinstance(chunk, File) and chunk.has_content():
                return chunk
        return None
    
    def get_first_slot(self):
        for chunk in self.chunks:
            if isinstance(chunk, Slot) and chunk.has_free_blocks():
                return chunk
        return None