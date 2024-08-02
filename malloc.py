class MemoryManager:
    def __init__(self, limit_mb):
        self.limit = limit_mb * 1024 * 1024  # Convert MB to bytes
        self.allocated_memory = 0

    def allocate(self, size):
        if self.allocated_memory + size > self.limit:
            raise MemoryError("Program exceeds the given malloc threshold")
        self.allocated_memory += size

    def deallocate(self, size):
        self.allocated_memory -= size
        if self.allocated_memory < 0:
            self.allocated_memory = 0

    def get_allocated_memory(self):
        return self.allocated_memory

    def get_remaining_memory(self):
        return self.limit - self.allocated_memory