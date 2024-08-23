# Ulto - Imperative Reversible Programming Language
#
# logstack.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import time
import sys


class LogStack:
    """
    A class to manage a stack-based log of variable values with support for undo operations.

    The `LogStack` class is designed to keep track of the changes made to variables over time.
    It stores the history of variable values along with timestamps, allowing for operations
    like pushing new values, popping the most recent value, peeking at previous values, pruning
    old entries, and calculating memory usage.

    Attributes:
        log (dict): A dictionary where keys are variable names and values are lists of tuples
                    storing old values and their corresponding timestamps.
        last_pruned (float): The last time the log was pruned, stored as a Unix timestamp.
    """

    def __init__(self):
        """
        Initializes a new instance of the LogStack class.

        The constructor initializes an empty log dictionary and sets the `last_pruned`
        attribute to the current time.
        """
        self.log = {}
        self.last_pruned = time.time()

    def push(self, var_name, old_value):
        """
        Pushes the old value of a variable onto the log stack.

        If the variable does not have an existing log, a new entry is created.
        The old value is stored along with the current timestamp.

        Args:
            var_name (str): The name of the variable whose value is being logged.
            old_value (Any): The old value of the variable to be pushed onto the log.
        """
        if var_name not in self.log:
            self.log[var_name] = []
        self.log[var_name].append((old_value, time.time()))

    def pop(self, var_name):
        """
        Pops the most recent value from the log stack for a given variable.

        If the variable has an entry in the log and it is not empty, the most recent
        value is removed and returned. If the log is empty or the variable does not
        exist in the log, `None` is returned.

        Args:
            var_name (str): The name of the variable whose most recent value is to be popped.

        Returns:
            Any: The most recent old value of the variable, or `None` if no value is available.
        """
        if var_name in self.log and self.log[var_name]:
            return self.log[var_name].pop()[0]
        return None

    def peek(self, var_name, index=1):
        """
        Peeks at a specific previous value in the log stack for a given variable.

        This method allows you to view a previous value without removing it from the stack.
        The `index` parameter specifies how far back to look (1 for the most recent, 2 for
        the second most recent, etc.).

        Args:
            var_name (str): The name of the variable to peek at.
            index (int): The position in the log stack to peek at (1 for the most recent).

        Returns:
            Any: The value at the specified position in the log stack, or `None` if the
                 position is out of range or the variable does not exist.
        """
        if var_name in self.log and len(self.log[var_name]) >= index:
            return self.log[var_name][-index][0]
        return None

    def prune(self, retention_time=50000):
        """
        Prunes old log entries based on a specified retention time.

        This method removes any entries in the log that are older than the specified
        `retention_time`. The default retention time is 50,000 seconds. Pruning is
        only performed if enough time has passed since the last pruning.

        Args:
            retention_time (int, optional): The maximum age of log entries to retain, in seconds.
                                            Entries older than this will be removed. Defaults to 50,000.
        """
        current_time = time.time()
        if current_time - self.last_pruned > retention_time:
            for var_name in list(self.log.keys()):
                self.log[var_name] = [val for val in self.log[var_name] if (current_time - val[1]) < retention_time]
            self.last_pruned = current_time

    def get_memory_usage(self):
        """
        Calculates the memory usage of the log stack.

        This method computes the total memory usage of the log stack, including the memory
        used by the log dictionary, variable names, and their stored values.

        Returns:
            float: The total memory usage of the log stack in megabytes (MB).
        """
        total_size = sys.getsizeof(self.log)
        for var_name, values in self.log.items():
            total_size += sys.getsizeof(var_name)
            for value, _ in values:
                total_size += sys.getsizeof(value)
        return total_size / (1024 * 1024)