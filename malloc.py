# Ulto - Imperative Reversible Programming Language
#
# malloc.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

class MemoryManager:
    def __init__(self, limit_mb):
        """
        Initializes the MemoryManager with a memory limit.

        Args:
        limit_mb (int): The memory limit in megabytes.
        """
        self.limit = limit_mb * 1024 * 1024
        self.allocated_memory = 0

    def allocate(self, size):
        """
        Allocates the given amount of memory.

        Args:
        size (int): The amount of memory to allocate in bytes.

        Raises:
        MemoryError: If the allocation exceeds the memory limit.
        """
        if self.allocated_memory + size > self.limit:
            raise MemoryError("Program exceeds the given malloc threshold")
        self.allocated_memory += size

    def deallocate(self, size):
        """
        Deallocates the given amount of memory.

        Args:
        size (int): The amount of memory to deallocate in bytes.
        """
        self.allocated_memory -= size
        if self.allocated_memory < 0:
            self.allocated_memory = 0

    def get_allocated_memory(self):
        """
        Returns the total allocated memory.

        Returns:
        int: The total allocated memory in bytes.
        """
        return self.allocated_memory

    def get_remaining_memory(self):
        """
        Returns the remaining memory.

        Returns:
        int: The remaining memory in bytes.
        """
        return self.limit - self.allocated_memory