# Ulto - Imperative Reversible Programming Language
#
# trace.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import sys
import time


class ExecutionTrace:
    """
    An ordered record of every state change, so execution can be walked backwards.

    The per-variable stacks in LogStack answer "what was this variable before?",
    but they carry no ordering between variables, so on their own they cannot say
    which statements belonged to the branch that actually ran, or how many times
    a loop went round. The trace supplies that ordering: reversing a block is
    simply unwinding every event recorded after the mark taken when the block
    started, newest first. The branch taken never has to be re-derived from the
    condition, which is what makes reversal deterministic even when the branch
    body overwrote the variables the condition was testing.

    Events take one of two forms:

        ('value', var_name, old_value)    restore the value that was replaced
        ('delta', var_name, op, operand)  apply the inverse of the operation

    A `delta` event inverts the operation that produced it, so it never stores
    the value it replaced. That is cheaper whenever the replaced value is larger
    than the operand, and it is the form a reversible target would run without
    erasing anything.

    Attributes:
        events (list): The recorded events, oldest first.
        timestamps (list): When each event was recorded, parallel to `events`.
        consumed (list): Whether each event has already been undone.
        last_pruned (float): The last time the trace was pruned.
    """

    def __init__(self):
        """
        Initializes an empty trace.
        """
        self.events = []
        self.timestamps = []
        self.consumed = []
        self.last_pruned = time.time()

    def mark(self):
        """
        Returns the current position in the trace.

        A mark taken before a statement runs is what `reverse_to` later unwinds
        back to, which is how a whole block reverses as one unit.

        Returns:
        int: The current end of the trace.
        """
        return len(self.events)

    def record(self, event):
        """
        Appends an event to the trace.

        Args:
        event (tuple): The event to record.

        Returns:
        int: The position the event was recorded at.
        """
        self.events.append(event)
        self.timestamps.append(time.time())
        self.consumed.append(False)
        return len(self.events) - 1

    def is_consumed(self, position):
        """
        Reports whether the event at a position has already been undone.

        Args:
        position (int): The position to check.

        Returns:
        bool: True if the event has been undone.
        """
        return self.consumed[position]

    def consume(self, position):
        """
        Marks the event at a position as undone.

        Events are marked rather than removed so that every position handed out
        earlier stays valid, and so `revtrace` can still walk what happened.

        Args:
        position (int): The position to mark.
        """
        self.consumed[position] = True

    def has_pending(self, mark):
        """
        Reports whether anything recorded after a mark is still to be undone.

        Args:
        mark (int): The position to check from.

        Returns:
        bool: True if there is at least one outstanding event after the mark.
        """
        for position in range(len(self.events) - 1, mark - 1, -1):
            if not self.consumed[position]:
                return True
        return False

    def pending_since(self, mark):
        """
        Lists the events recorded after a mark that are still to be undone.

        Args:
        mark (int): The position to unwind back to.

        Returns:
        list: Positions of the outstanding events, newest first.
        """
        return [position for position in range(len(self.events) - 1, mark - 1, -1)
                if not self.consumed[position]]

    def prune(self, retention_time=50000):
        """
        Releases the values held by events that have already been undone.

        Only consumed events are pruned. An outstanding event is the sole record
        of how to get back to a previous state, so discarding one would destroy
        reversibility, which is the erasure the language exists to avoid. An
        event that has already been reversed has no such duty, so its payload can
        be released once it is older than the retention time.

        Args:
            retention_time (int, optional): The age in seconds past which a
                consumed event's payload is released. Defaults to 50,000.
        """
        current_time = time.time()
        if current_time - self.last_pruned <= retention_time:
            return
        for position, event in enumerate(self.events):
            if event is not None and self.consumed[position] and \
                    (current_time - self.timestamps[position]) >= retention_time:
                self.events[position] = None
        self.last_pruned = current_time

    def get_memory_usage(self):
        """
        Calculates the memory usage of the trace.

        Returns:
        float: The total memory usage of the trace in megabytes (MB).
        """
        total_size = sys.getsizeof(self.events) + sys.getsizeof(self.timestamps) \
            + sys.getsizeof(self.consumed)
        for event in self.events:
            if event is None:
                continue
            total_size += sys.getsizeof(event)
            for item in event:
                total_size += sys.getsizeof(item)
        return total_size / (1024 * 1024)
