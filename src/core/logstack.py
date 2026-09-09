# Ulto - Imperative Reversible Programming Language
#
# logstack.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import sys


class LogStack:
    """
    A per-variable index into the execution trace.

    `rev x` and `revtrace x n` reach a single variable's history, so they need to
    find that variable's changes without scanning everything that has happened.
    This class keeps, for each variable, the positions of the trace events that
    changed it. The values themselves live in the trace, which stays the single
    source of truth: keeping them in both places would double the memory a
    reversible program spends on its own history.

    Positions already undone are skipped rather than removed, so that a variable
    reversed as part of a whole block is not reversed a second time by a later
    `rev` naming it directly.

    Attributes:
        trace (ExecutionTrace): The trace the recorded positions point into.
        log (dict): A dictionary of variable names to lists of trace positions.
    """

    def __init__(self, trace):
        """
        Initializes a new instance of the LogStack class.

        Args:
        trace (ExecutionTrace): The trace this index points into.
        """
        self.trace = trace
        self.log = {}

    def push(self, var_name, position):
        """
        Records that a trace event at the given position changed a variable.

        Args:
            var_name (str): The name of the variable that changed.
            position (int): The position of the event in the trace.
        """
        if var_name not in self.log:
            self.log[var_name] = []
        self.log[var_name].append(position)

    def pop(self, var_name):
        """
        Removes and returns the most recent outstanding change to a variable.

        Positions whose events have already been undone are discarded on the way
        past, so a variable reversed as part of a block is not reversed twice.

        Args:
            var_name (str): The name of the variable to reverse.

        Returns:
            int: The trace position of the change, or `None` if there is none.
        """
        positions = self.log.get(var_name)
        while positions:
            position = positions.pop()
            if not self.trace.is_consumed(position):
                return position
        return None

    def peek(self, var_name, index=1):
        """
        Returns a previous change to a variable without reversing it.

        The `index` parameter specifies how far back to look (1 for the most
        recent, 2 for the one before it, and so on). Changes already undone are
        skipped, so the numbering always describes the states still reachable.

        Args:
            var_name (str): The name of the variable to peek at.
            index (int): How many steps back to look.

        Returns:
            int: The trace position of that change, or `None` if out of range.
        """
        positions = self.log.get(var_name, ())
        seen = 0
        for position in reversed(positions):
            if self.trace.is_consumed(position):
                continue
            seen += 1
            if seen == index:
                return position
        return None

    def positions(self, var_name):
        """
        Lists the outstanding changes to a variable, most recent first.

        Args:
            var_name (str): The variable to list changes for.

        Returns:
            list: Trace positions of the changes not yet undone.
        """
        return [position for position in reversed(self.log.get(var_name, ()))
                if not self.trace.is_consumed(position)]

    def prune(self, retention_time=50000):
        """
        Prunes the underlying trace of values that have already been reversed.

        Args:
            retention_time (int, optional): The age in seconds past which a
                                            reversed event's payload is released.
                                            Defaults to 50,000.
        """
        self.trace.prune(retention_time)

    def get_memory_usage(self):
        """
        Calculates the memory usage of the index and the trace it points into.

        Returns:
            float: The total memory usage in megabytes (MB).
        """
        total_size = sys.getsizeof(self.log)
        for var_name, positions in self.log.items():
            total_size += sys.getsizeof(var_name) + sys.getsizeof(positions)
        return total_size / (1024 * 1024) + self.trace.get_memory_usage()
