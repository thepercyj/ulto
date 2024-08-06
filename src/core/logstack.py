# Ulto - Imperative Reversible Programming Language
#
# logstack.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import time
import sys


class LogStack:
    def __init__(self):
        self.log = {}
        self.last_pruned = time.time()

    def push(self, var_name, old_value):
        if var_name not in self.log:
            self.log[var_name] = []
        self.log[var_name].append((old_value, time.time()))

    def pop(self, var_name):
        if var_name in self.log and self.log[var_name]:
            return self.log[var_name].pop()[0]
        return None

    def peek(self, var_name, index=1):
        if var_name in self.log and len(self.log[var_name]) >= index:
            return self.log[var_name][-index][0]
        return None

    def prune(self, retention_time=3600):
        current_time = time.time()
        if current_time - self.last_pruned > retention_time:
            for var_name in list(self.log.keys()):
                self.log[var_name] = [val for val in self.log[var_name] if (current_time - val[1]) < retention_time]
            self.last_pruned = current_time

    def get_memory_usage(self):
        total_size = sys.getsizeof(self.log)
        for var_name, values in self.log.items():
            total_size += sys.getsizeof(var_name)
            for value, _ in values:
                total_size += sys.getsizeof(value)
        return total_size / (1024 * 1024)
