# Ulto - Imperative Reversible Programming Language
#
# interpreter.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import io
import os
import sys
import time
import threading
import ctypes
import platform
from datetime import datetime
from src.core.malloc import MemoryManager
from src.core.lazyeval import LazyEval
from src.core.logstack import LogStack
from src.core.trace import ExecutionTrace
from sortedcontainers import SortedDict


class BreakException(Exception):
    pass


# Bounds for the C fast path. The shared library takes and returns 32-bit
# signed ints, and ctypes truncates out-of-range arguments silently instead of
# raising, so an unguarded call cannot be trusted to fail loudly. Anything that
# could leave that range is evaluated in Python instead.
INT32_MIN = -2 ** 31
INT32_MAX = 2 ** 31 - 1
# Operand bounds that rule out an overflow without first doing the arithmetic in
# Python, which would defeat the point of calling into C at all. Two operands
# within ADDITIVE_SAFE cannot sum past INT32_MAX, and two within
# MULTIPLICATIVE_SAFE (isqrt of INT32_MAX) cannot multiply past it.
ADDITIVE_SAFE = 2 ** 30 - 1
MULTIPLICATIVE_SAFE = 46340


def in_c_range(value):
    """
    Reports whether a value can cross the FFI boundary as a C int without loss.

    Args:
    value (any): The value to be checked.

    Returns:
    bool: True if the value is an integer inside the 32-bit signed range.
    """
    return isinstance(value, int) and INT32_MIN <= value <= INT32_MAX


def additive_safe(left, right):
    """
    Reports whether an addition or subtraction can be delegated to C safely.
    """
    return (isinstance(left, int) and isinstance(right, int)
            and -ADDITIVE_SAFE <= left <= ADDITIVE_SAFE
            and -ADDITIVE_SAFE <= right <= ADDITIVE_SAFE)


def multiplicative_safe(left, right):
    """
    Reports whether a multiplication can be delegated to C safely.
    """
    return (isinstance(left, int) and isinstance(right, int)
            and -MULTIPLICATIVE_SAFE <= left <= MULTIPLICATIVE_SAFE
            and -MULTIPLICATIVE_SAFE <= right <= MULTIPLICATIVE_SAFE)


def division_safe(left, right):
    """
    Reports whether a division, integer division or modulo can be delegated to C.

    A zero divisor is excluded because the library exits the process on it, and
    INT32_MIN / -1 is excluded because its result does not fit in a C int.
    """
    return (in_c_range(left) and in_c_range(right) and right != 0
            and not (left == INT32_MIN and right == -1))


def comparison_safe(left, right):
    """
    Reports whether a comparison or logical operation can be delegated to C.

    Comparisons cannot overflow, so only the operand range matters.
    """
    return in_c_range(left) and in_c_range(right)


def c_truncated_div(left, right):
    """
    Divides two integers truncating toward zero, matching C's `/` on ints.

    Python's `//` floors instead, so the two disagree on negative operands. The
    C behaviour is the one Ulto programs already observe, so the Python path
    reproduces it rather than letting results shift with operand magnitude.
    """
    quotient = abs(left) // abs(right)
    return -quotient if (left < 0) != (right < 0) else quotient


def c_remainder(left, right):
    """
    Returns a remainder taking the sign of the dividend, matching C's `%`.
    """
    return left - c_truncated_div(left, right) * right


class Interpreter:
    class Interpreter:
        """
        An interpreter for the Ulto programming language.

        The `Interpreter` class is responsible for executing the abstract syntax tree (AST) of an Ulto program.
        It manages variable assignments, control flow (e.g., loops, conditionals), arithmetic operations, and
        reversible operations. The interpreter also handles memory management, profiling, and logging of
        execution details. Additionally, it interfaces with a C library for optimized arithmetic and compound
        assignment operations through foreign function interface (FFI) using `ctypes`.

        Attributes:
            ast (list): The abstract syntax tree representing the program.
            symbol_table (SortedDict): A sorted dictionary used to store variable names and their associated values.
            history (list): A list to keep track of execution history.
            detailed_history (list): A list to store detailed execution history.
            assignments (int): A counter for the number of assignments performed.
            evaluations (int): A counter for the number of expressions evaluated.
            reversals (int): A counter for the number of reversals executed.
            current_step (int): The current step number in the execution.
            memory_manager (MemoryManager): An instance of the MemoryManager class for managing memory allocation.
            eager_vars (set): A set of variables identified for eager evaluation.
            profiling_data (dict): A dictionary to store profiling data for optimizing execution.
            profile_batch_size (int): The batch size for profiling updates.
            profile_counter (int): A counter to manage profiling updates.
            logstack (LogStack): An instance of the LogStack class to manage reversible operations.
            lib (ctypes.CDLL): A C library loaded for performing arithmetic and compound assignments.
        """
    # Each entry maps an Ulto operator to the C entry point that implements it,
    # the guard deciding whether that call is safe for a given pair of operands,
    # and the Python equivalent used when it is not. The Python side mirrors the
    # C semantics exactly so results do not change with operand magnitude.
    OPERATORS = {
        'plus': ('execute_add', additive_safe, lambda left, right: left + right),
        'minus': ('execute_sub', additive_safe, lambda left, right: left - right),
        'times': ('execute_mul', multiplicative_safe, lambda left, right: left * right),
        'over': ('execute_div', division_safe, c_truncated_div),
        'int_div': ('execute_int_div', division_safe, c_truncated_div),
        'modulo': ('execute_modulo', division_safe, c_remainder),
        'eq': ('execute_eq', comparison_safe, lambda left, right: 1 if left == right else 0),
        'neq': ('execute_neq', comparison_safe, lambda left, right: 1 if left != right else 0),
        'lt': ('execute_lt', comparison_safe, lambda left, right: 1 if left < right else 0),
        'gt': ('execute_gt', comparison_safe, lambda left, right: 1 if left > right else 0),
        'lte': ('execute_lte', comparison_safe, lambda left, right: 1 if left <= right else 0),
        'gte': ('execute_gte', comparison_safe, lambda left, right: 1 if left >= right else 0),
        'and': ('execute_and', comparison_safe, lambda left, right: 1 if (left and right) else 0),
        'or': ('execute_or', comparison_safe, lambda left, right: 1 if (left or right) else 0),
    }

    # The compound assignments have their own C entry points, which take the
    # target by pointer. They are guarded on the same bounds as the plain
    # arithmetic they stand for.
    COMPOUND_OPERATORS = {
        'plus_assign': ('execute_add_assign', additive_safe, lambda left, right: left + right),
        'minus_assign': ('execute_sub_assign', additive_safe, lambda left, right: left - right),
        'times_assign': ('execute_mul_assign', multiplicative_safe, lambda left, right: left * right),
        'over_assign': ('execute_div_assign', division_safe, c_truncated_div),
    }

    def __init__(self, ast):
        """
        Initializes the ExecutionEngine with the given AST.

        Args:
        ast (list): The abstract syntax tree.
        """
        self.ast = ast
        self.symbol_table = SortedDict()
        self.history = []
        self.detailed_history = []
        self.assignments = 0
        self.evaluations = 0
        self.reversals = 0
        self.current_step = 0
        # limiting programs to 50 MB for the moment. If exceeds throws malloc exception errors.
        self.memory_manager = MemoryManager(50)
        self.eager_vars = set()
        self.profiling_data = {}
        self.profile_batch_size = 250
        self.profile_counter = 0
        # The trace records state changes in execution order, which is what lets
        # a whole branch or loop reverse as a unit. The logstack indexes into it
        # per variable, for `rev x` and `revtrace x n`.
        self.trace = ExecutionTrace()
        self.logstack = LogStack(self.trace)
        # Marks for the statements completed in each enclosing block, so a bare
        # `rev` knows where the statement before it began.
        self.scopes = []
        # AST nodes whose effect can be undone by inverting the operation, so no
        # replaced value has to be stored for them.
        self.self_invertible = set()
        # For each loop, the variables whose changes can be summed over the whole
        # run and recorded once, rather than once per iteration.
        self.loop_accumulable = {}
        # Variables named by a `rev x` or `revtrace x n` anywhere in the program,
        # which therefore need their per-step history kept.
        self.named_reversals = set()
        # While an accumulating loop runs, the net change to each eligible
        # variable is gathered here instead of being recorded a step at a time.
        self.coalescing = None
        self.coalescing_owner = None
        self.coalescing_eligible = frozenset()
        self.coalesced_bindings = set()

        # loading machine compiled arithmetic and compound assignment file.
        self.lib = ctypes.CDLL(self.locate_operations_library())

        # Here, arithmetic and compound assignments are handled via C compiler through FFI using ctypes
        self.lib.execute_add.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_add.restype = ctypes.c_int

        self.lib.execute_sub.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_sub.restype = ctypes.c_int

        self.lib.execute_mul.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_mul.restype = ctypes.c_int

        self.lib.execute_div.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_div.restype = ctypes.c_int

        self.lib.execute_modulo.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_modulo.restype = ctypes.c_int

        self.lib.execute_int_div.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_int_div.restype = ctypes.c_int

        self.lib.execute_eq.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_eq.restype = ctypes.c_int

        self.lib.execute_neq.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_neq.restype = ctypes.c_int

        self.lib.execute_lt.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_lt.restype = ctypes.c_int

        self.lib.execute_gt.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_gt.restype = ctypes.c_int

        self.lib.execute_lte.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_lte.restype = ctypes.c_int

        self.lib.execute_gte.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_gte.restype = ctypes.c_int

        self.lib.execute_and.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_and.restype = ctypes.c_int

        self.lib.execute_or.argtypes = [ctypes.c_int, ctypes.c_int]
        self.lib.execute_or.restype = ctypes.c_int

        # Define argument and return types for the compound assignment operations
        self.lib.execute_add_assign.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.execute_add_assign.restype = ctypes.c_int

        self.lib.execute_sub_assign.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.execute_sub_assign.restype = ctypes.c_int

        self.lib.execute_mul_assign.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.execute_mul_assign.restype = ctypes.c_int

        self.lib.execute_div_assign.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        self.lib.execute_div_assign.restype = ctypes.c_int

        # Resolving the C entry points once keeps the getattr lookup out of the
        # hot path, since these tables are consulted on every operation.
        self.operators = {
            op: (getattr(self.lib, c_name), guard, fallback)
            for op, (c_name, guard, fallback) in self.OPERATORS.items()
        }
        self.compound_operators = {
            op: (getattr(self.lib, c_name), guard, fallback)
            for op, (c_name, guard, fallback) in self.COMPOUND_OPERATORS.items()
        }

    def locate_operations_library(self):
        """
        Finds the compiled arithmetic library built for the machine in use.

        Builds are shipped for more than one architecture, so the right one is
        chosen from the running machine rather than assumed. The build filed
        under this machine's architecture is preferred over the loose copy beside
        this file, because that loose copy can only ever be right for one
        architecture. It is still used as a fallback, since an installed package
        may ship nothing else.

        Returns:
        str: The path of the library to load.

        Raises:
        FileNotFoundError: If no build matches this machine.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        windows = platform.system() == "Windows"
        name = 'operations.dll' if windows else 'liboperations.so'
        folder = 'Windows' if windows else 'Linux'

        machine = platform.machine().lower()
        if machine in ('x86_64', 'amd64', 'x64'):
            architecture = 'x86_64'
        elif machine in ('aarch64', 'arm64', 'armv8'):
            architecture = 'ARM_Aarch'
        else:
            architecture = None

        candidates = []
        if architecture:
            candidates.append(os.path.join(script_dir, 'architecture', architecture, folder, name))
        candidates.append(os.path.join(script_dir, name))

        for candidate in candidates:
            if os.path.isfile(candidate):
                return candidate

        raise FileNotFoundError(
            f'No compiled operations library for {platform.system()} on '
            f'{platform.machine()}. Looked in: ' + ', '.join(candidates))

    def execute(self, capture=False):
        """
        Executes the AST.

        Args:
            capture (bool): When true, the program's output is collected instead
                of being written to stdout. A host embedding the interpreter,
                such as the web front end, needs the text back rather than
                printed, and under a WSGI server there may be no usable stdout
                to print to.

        Returns:
        str: The program's output. Empty unless `capture` was requested.
        """
        collected = io.StringIO()
        original_stdout = sys.stdout
        if capture:
            sys.stdout = collected

        start_time = time.time()
        try:
            print("\n~~~~~~~~~~~~~~~~~~~~OUTPUT~~~~~~~~~~~~~~~~~~~~\n")
            # collecting profiling data to find hotspots and manage accordingly during runtime.
            self.collect_profiling_data(self.ast)
            # for detecting eager variables that are often used in the source code, preprocessing it at the start of AST execution.
            self.detect_eager_vars()
            # marking the statements that can be undone by inverting them, so
            # they never have to store the value they replaced. The variables
            # reversed by name are collected first, since they are the ones whose
            # step by step history has to survive.
            self.collect_named_reversals(self.ast)
            self.analyse_reversibility(self.ast)
            self.execute_block(self.ast)
        finally:
            end_time = time.time()
            # The cost report belongs to the program's output, so it is written
            # before stdout is handed back.
            try:
                self.print_computation_cost()
            finally:
                sys.stdout = original_stdout
            self.log_execution_details(start_time, end_time)

        return collected.getvalue()

    def collect_profiling_data(self, ast):
        """
        Collects profiling data from the AST.

        Args:
        ast (list): The abstract syntax tree.
        """
        for node in ast:
            self.profile_node(node)

    def profile_node(self, node):
        """
        Profiles a single node in the AST. For now, handling conditionals, assignments, reversals and prints.

        Args:
        node (tuple): The node to be profiled.
        """
        if node[0] == 'assign':
            self.profile_assignment(node)
        elif node[0] == 'reverse':
            self.profile_reverse(node)
        elif node[0] == 'revtrace':
            self.profile_revtrace(node)
        elif node[0] == 'if':
            self.profile_if(node)
        elif node[0] == 'while':
            self.profile_while(node)
        elif node[0] == 'print':
            self.profile_print(node)

    def profile_assignment(self, node):
        """
        Profiles an assignment node.

        Args:
        node (tuple): The assignment node.
        """
        _, var_name, value = node
        self.update_profiling_data(var_name)
        self.update_profiling_data(value)

    def profile_reverse(self, node):
        """
        Profiles a reverse node.

        Args:
        node (tuple): The reverse node.
        """
        _, var_name = node
        self.update_profiling_data(var_name)

    def profile_revtrace(self, node):
        """
        Profiles a revtrace node.

        Args:
        node (tuple): The revtrace node.
        """
        _, var_name, index = node
        self.update_profiling_data(var_name)
        self.update_profiling_data(index)

    def profile_if(self, node):
        """
        Profiles an if node.

        Args:
        node (tuple): The if node.
        """
        _, condition, true_branch, elif_branches, false_branch = node

        self.update_profiling_data(condition)
        for stmt in true_branch:
            self.profile_node(stmt)

        for elif_condition, elif_branch in elif_branches:
            self.update_profiling_data(elif_condition)
            for stmt in elif_branch:
                self.profile_node(stmt)

        for stmt in false_branch:
            self.profile_node(stmt)

    def profile_while(self, node):
        """
        Profiles a while node.

        Args:
        node (tuple): The while node.
        """
        _, condition, body = node
        self.update_profiling_data(condition)
        for stmt in body:
            self.profile_node(stmt)

    def profile_print(self, node):
        """
        Profiles a print node.

        Args:
        node (tuple): The print node.
        """
        _, value = node
        self.update_profiling_data(value)

    def update_profiling_data(self, expr):
        """
        Updates the profiling data with the given expression.

        Args:
        expr (any): The expression to be profiled.
        """
        if isinstance(expr, tuple):
            for item in expr:
                self.update_profiling_data(item)
        elif isinstance(expr, list):
            for item in expr:
                self.update_profiling_data(item)
        elif isinstance(expr, str):
            if expr in self.profiling_data:
                self.profiling_data[expr] += 1
            else:
                self.profiling_data[expr] = 1

        # Batch profiling updates
        self.profile_counter += 1
        if self.profile_counter >= self.profile_batch_size:
            self.profile_counter = 0
            self.detect_eager_vars()

    def detect_eager_vars(self):
        """
        Detects eager variables based on the profiling data.
        """
        # threshold set to 3 to avoid inaccuracy of dealing hotspots, can shift it to 5 for reducing overhead but for
        # now is good. can be tweaked based on nature of application.
        threshold = 3
        for var, count in self.profiling_data.items():
            if count > threshold:
                self.eager_vars.add(var)

    def analyse_reversibility(self, statements):
        """
        Marks the statements that can be undone without storing a value.

        `x += e` and `x -= e` are their own inverse as long as `e` does not read
        `x`, so undoing one is a matter of applying the opposite operation rather
        than restoring what was there before. That is worth detecting because the
        replaced value is often far larger than the operand, and because an
        inverted operation is what a reversible target would run without erasing
        anything. `*=` and `/=` are excluded: integer division truncates, so
        multiplying back does not reliably land on the original value.

        Args:
        statements (list): The statements to analyse.
        """
        for node in statements:
            node_type = node[0]
            if node_type in ('plus_assign', 'minus_assign'):
                _, var_name, value = node
                if not self.references(value, var_name):
                    self.self_invertible.add(id(node))
            elif node_type == 'if':
                _, _, true_branch, elif_branches, false_branch = node
                self.analyse_reversibility(true_branch)
                for _, elif_branch in elif_branches:
                    self.analyse_reversibility(elif_branch)
                self.analyse_reversibility(false_branch)
            elif node_type == 'while':
                self.analyse_reversibility(node[2])
                self.mark_accumulable(node, node[2])
            elif node_type == 'for':
                self.analyse_reversibility(node[3])
                self.mark_accumulable(node, node[3])

    def mark_accumulable(self, node, body):
        """
        Works out which of a loop's variables can be recorded once for the run.

        Args:
        node (tuple): The loop node.
        body (list): The statements of the loop body.
        """
        eligible = self.accumulable_variables(node, body)
        if eligible:
            self.loop_accumulable[id(node)] = eligible

    def accumulable_variables(self, node, body):
        """
        Returns the variables whose changes a loop can sum instead of listing.

        Successive self-invertible updates to one variable compose: a thousand
        `i += 1` steps undo as a single `i -= 1000`. So a variable a loop only
        ever adds to or subtracts from needs one recorded change for the entire
        run, however many times the loop goes round, even when the rest of the
        body is doing things that must still be recorded step by step.

        A variable is disqualified when summing would lose something that is
        actually asked for:

        - It is also assigned outright somewhere in the loop. An assignment
          replaces the value rather than shifting it, so the steps either side of
          it do not compose.
        - It is the target of a `rev x` or `revtrace x n` anywhere in the
          program. Both walk a variable back one change at a time, which is
          exactly the history summing discards.
        - The loop body contains any reversal at all, which would be asking to
          unwind iterations that are no longer recorded separately.

        Args:
        node (tuple): The loop node.
        body (list): The statements of the loop body.

        Returns:
        set: The variables eligible to be accumulated over the whole loop.
        """
        delta_targets = set()
        # A `for` binds its own variable afresh each iteration, which replaces
        # the value the same way an assignment does.
        hard_targets = {node[1]} if node[0] == 'for' else set()

        for stmt in self.walk_statements(body):
            kind = stmt[0]
            if kind in ('reverse', 'revtrace'):
                return set()
            if kind in ('plus_assign', 'minus_assign') and id(stmt) in self.self_invertible:
                delta_targets.add(stmt[1])
            elif kind in ('assign', 'plus_assign', 'minus_assign', 'times_assign', 'over_assign'):
                hard_targets.add(stmt[1])
            elif kind == 'for':
                hard_targets.add(stmt[1])

        return delta_targets - hard_targets - self.named_reversals

    def walk_statements(self, statements):
        """
        Yields every statement in a block, including those nested inside it.

        Args:
        statements (list): The statements to walk.

        Yields:
        tuple: Each statement, outermost first.
        """
        for stmt in statements:
            yield stmt
            if stmt[0] == 'if':
                yield from self.walk_statements(stmt[2])
                for _, elif_branch in stmt[3]:
                    yield from self.walk_statements(elif_branch)
                yield from self.walk_statements(stmt[4])
            elif stmt[0] == 'while':
                yield from self.walk_statements(stmt[2])
            elif stmt[0] == 'for':
                yield from self.walk_statements(stmt[3])

    def collect_named_reversals(self, ast):
        """
        Collects every variable reversed or traced by name in the program.

        These need their history kept one change at a time, so they are never
        accumulated, wherever in the program the reversal appears relative to the
        loop that changes them.

        Args:
        ast (list): The abstract syntax tree.
        """
        for stmt in self.walk_statements(ast):
            if stmt[0] in ('reverse', 'revtrace') and stmt[1] is not None:
                self.named_reversals.add(stmt[1])

    def references(self, expr, var_name):
        """
        Reports whether an expression reads a given variable.

        Args:
        expr (any): The expression to inspect.
        var_name (str): The variable to look for.

        Returns:
        bool: True if the variable may be read by the expression.
        """
        if isinstance(expr, str):
            return expr == var_name
        if isinstance(expr, (list, tuple)):
            return any(self.references(item, var_name) for item in expr)
        return False

    def execute_block(self, statements):
        """
        Executes a block of statements, remembering where each one began.

        The mark taken before a statement runs is what a later bare `rev` unwinds
        back to, so reversing a statement reverses everything it did, however
        many branches or iterations that turned out to involve. Marks are kept
        per block, so a `rev` inside a loop body reverses a statement of that
        body rather than reaching outside it.

        Args:
        statements (list): The statements to execute.
        """
        self.scopes.append([])
        top_level = len(self.scopes) == 1
        try:
            for stmt in statements:
                mark = self.trace.mark()
                self.execute_node(stmt)
                # A reversal is not itself something to reverse, so consecutive
                # `rev` statements walk further back instead of undoing my own
                # previous undo.
                if stmt[0] not in ('reverse', 'revtrace'):
                    self.scopes[-1].append(mark)
                if top_level:
                    self.prune_logstack()
        finally:
            self.scopes.pop()

    def execute_node(self, node):
        """
        Executes a single node in the AST.

        Args:
        node (tuple): The node to be executed.
        """
        node_type = node[0]
        if node_type == 'assign':
            self.execute_assignment(node)
        elif node_type == 'reverse':
            self.execute_reverse(node)
        elif node_type == 'revtrace':
            self.execute_revtrace(node)
        elif node_type == 'if':
            self.execute_if(node)
        elif node_type == 'for':
            self.execute_for(node)
        elif node_type == 'while':
            self.execute_while(node)
        elif node_type == 'print':
            self.execute_print(node)
        elif node_type == 'plus_assign':
            self.execute_plus_assign(node)
        elif node_type == 'minus_assign':
            self.execute_minus_assign(node)
        elif node_type == 'times_assign':
            self.execute_times_assign(node)
        elif node_type == 'over_assign':
            self.execute_over_assign(node)
        elif node_type == 'break':
            raise BreakException()
        else:
            self.error(f'Unknown node type: {node_type}')

    def execute_assignment(self, node):
        """
        Executes an assignment node.

        Args:
        node (tuple): The assignment node.
        """
        self.assignments += 1
        _, var_name, value = node

        # Considering hybrid approach since, some programs developed can have circular dependency. Hence, based on the
        # source code profile eager and lazy accordingly.
        # for eg: "i = i + 1" meets the requirement of circular dependency causing infinite loops if lazily evaluated.
        if var_name in self.eager_vars:
            evaluated_value = self.evaluate_expression(value)
            lazy_value = evaluated_value
        else:
            # The bindings are captured now and the arithmetic is left for later.
            # Deferring the lookup too would read whatever the variables happen to
            # hold when the value is finally wanted, which is not what the
            # statement said.
            lazy_value = LazyEval(self.substitute(value), self)

        previous_value = self.symbol_table.get(var_name, None)

        # estimates memory use and pools itself for only what is required to perform operations below the set threshold.
        size = sys.getsizeof(lazy_value)
        self.memory_manager.allocate(size)

        # deallocate memory based on previous value for re-usability on a different operation.
        if previous_value is not None:
            prev_size = sys.getsizeof(previous_value)
            self.memory_manager.deallocate(prev_size)

        self.record_change(var_name, ('value', var_name, previous_value))
        self.symbol_table[var_name] = lazy_value

    def substitute(self, expr):
        """
        Replaces the variables in an expression with what they are bound to now.

        Laziness is meant to defer the work of computing a value, not to change
        which value gets computed. An expression that still names its variables
        when it is finally evaluated reads whatever they hold at that later
        moment, so `t = p + q` followed by `p = q` would compute `t` from the new
        `p`. Capturing the bindings at the point of assignment keeps a lazy result
        identical to the eager one.

        Nothing is forced here. A binding that is itself unevaluated is carried
        into the expression as it stands, so the deferral survives. It also ends
        the self reference in `i = i + 1`, which used to describe a value in terms
        of itself: the captured binding is the old one, not the one being created.

        Args:
        expr (any): The expression to capture bindings for.

        Returns:
        The expression with its variables replaced by their current bindings.
        """
        if isinstance(expr, str):
            # Backtick and double quoted forms are literals, and so are digits.
            if expr.startswith('`') and expr.endswith('`'):
                return expr
            if expr.isnumeric() or expr.startswith('"'):
                return expr
            return self.symbol_table[expr] if expr in self.symbol_table else expr

        if isinstance(expr, list):
            return [self.substitute(item) for item in expr]

        if isinstance(expr, tuple):
            if len(expr) == 3:
                # The middle element names the operation, not a variable.
                left, op, right = expr
                return (self.substitute(left), op, self.substitute(right))
            if len(expr) == 2 and expr[0] == 'len':
                return ('len', self.substitute(expr[1]))

        return expr

    def record_change(self, var_name, event):
        """
        Records a state change on the trace and indexes it by variable.

        Args:
        var_name (str): The variable the change applies to.
        event (tuple): The event describing how to undo the change.

        Returns:
        int: The position of the event in the trace.
        """
        position = self.trace.record(event)
        self.logstack.push(var_name, position)
        self.current_step += 1
        return position

    def undo_event(self, event):
        """
        Undoes a single recorded state change.

        Args:
        event (tuple): The event to undo.
        """
        if event is None:
            return
        if event[0] == 'value':
            _, var_name, old_value = event
            # A `None` here means the variable did not exist before the change,
            # and there is no earlier state to return it to.
            if old_value is not None:
                self.symbol_table[var_name] = old_value
        else:
            _, var_name, op, operand = event
            current_value = self.evaluate_expression(self.symbol_table.get(var_name))
            inverse = 'minus' if op == 'plus_assign' else 'plus'
            self.symbol_table[var_name] = self.apply_operator(inverse, current_value, operand)

    def reverse_to(self, mark):
        """
        Unwinds every outstanding change recorded after a mark, newest first.

        This is what makes a branch or a loop reverse deterministically. The
        trace already says which statements ran, so the condition never has to be
        re-tested to work out which way the `if` went, and the iteration count
        never has to be recovered. Both are consequences of what was recorded
        rather than something re-derived from state the body may have destroyed.

        Args:
        mark (int): The trace position to unwind back to.

        Returns:
        int: The number of changes undone.
        """
        positions = self.trace.pending_since(mark)
        for position in positions:
            event = self.trace.events[position]
            self.trace.consume(position)
            self.undo_event(event)
        self.reversals += len(positions)
        return len(positions)

    def execute_compound_assign(self, node, op):
        """
        Executes a compound assignment (`+=`, `-=`, `*=`, `/=`) on a variable.

        The arithmetic goes to the matching C entry point whenever the operands
        are small enough for the result to stay inside a 32-bit int, and is done
        in Python otherwise.

        Args:
            node (tuple): The compound assignment node, as (_, var_name, value).
            op (str): The compound operator, used to select the C entry point.

        Raises:
            KeyError: If `var_name` is not found in the symbol table.
        """
        _, var_name, value = node
        current_value = self.symbol_table.get(var_name)
        if isinstance(current_value, LazyEval):
            current_value = current_value.evaluate()
        operand = self.evaluate_expression(value)
        if isinstance(operand, LazyEval):
            operand = operand.evaluate()
        # A statement the analyser proved self-invertible is undone by applying
        # the opposite operation, so only the operand is recorded. Otherwise the
        # replaced value is what has to be kept.
        if id(node) in self.self_invertible:
            if self.coalescing is not None and var_name in self.coalescing_eligible:
                # Inside an accumulating loop the operands are summed and recorded
                # once when the loop finishes, so the trace does not grow with the
                # number of iterations.
                net = self.coalescing.get(var_name, 0)
                signed = operand if op == 'plus_assign' else -operand
                self.coalescing[var_name] = self.apply_operator('plus', net, signed)
            else:
                self.record_change(var_name, ('delta', var_name, op, operand))
        else:
            self.record_change(var_name, ('value', var_name, current_value))

        c_function, guard, fallback = self.compound_operators[op]
        if guard(current_value, operand):
            # The target is passed by pointer, so it is held in a named cell for
            # the duration of the call rather than a discarded temporary.
            cell = ctypes.c_int(current_value)
            c_function(ctypes.byref(cell), operand)
            new_value = cell.value
        else:
            new_value = self.python_fallback(fallback, current_value, operand)

        # The result is already computed, so it is stored directly. Wrapping a
        # known value in a LazyEval would allocate a thunk with nothing to defer.
        self.symbol_table[var_name] = new_value

    def execute_plus_assign(self, node):
        """
        Executes a plus assignment operation (`+=`) on a variable.

        Args:
            node (tuple): The assignment node, as (_, var_name, value).
        """
        self.execute_compound_assign(node, 'plus_assign')

    def execute_minus_assign(self, node):
        """
        Executes a minus assignment operation (`-=`) on a variable.

        Args:
            node (tuple): The assignment node, as (_, var_name, value).
        """
        self.execute_compound_assign(node, 'minus_assign')

    def execute_times_assign(self, node):
        """
        Executes a times assignment operation (`*=`) on a variable.

        Args:
            node (tuple): The assignment node, as (_, var_name, value).
        """
        self.execute_compound_assign(node, 'times_assign')

    def execute_over_assign(self, node):
        """
        Executes a division assignment operation (`/=`) on a variable.

        Args:
            node (tuple): The assignment node, as (_, var_name, value).
        """
        self.execute_compound_assign(node, 'over_assign')

    def execute_if(self, node):
        """
        Executes an if node.

        Args:
        node (tuple): The if node.
        """
        _, condition, true_branch, elif_branches, false_branch = node
        condition_result = self.evaluate_expression(condition)
        if condition_result:
            branch = true_branch
        else:
            for elif_condition, elif_branch in elif_branches:
                if self.evaluate_expression(elif_condition):
                    branch = elif_branch
                    break
            else:
                branch = false_branch

        # The branch that ran is recorded implicitly: every change it makes lands
        # on the trace in order, so reversing the `if` reverses exactly those
        # changes without re-testing a condition the branch may have invalidated.
        self.execute_block(branch)

    def execute_while(self, node):
        """
        Executes a while node.

        Args:
        node (tuple): The while node.
        """
        _, condition, body = node

        self.begin_coalescing(node)
        try:
            while self.evaluate_expression(condition):
                try:
                    self.execute_block(body)
                except BreakException:
                    break
        finally:
            self.end_coalescing(node)

    def begin_coalescing(self, node):
        """
        Starts accumulating a loop's eligible variables, if it has any.

        An inner loop inside an already accumulating one does not start its own
        run. Its updates join the outer total, which is both correct and better
        compression, since the outer analysis already covered the inner body.

        Args:
        node (tuple): The loop node about to run.

        Returns:
        bool: True if accumulation was started by this call.
        """
        if self.coalescing is not None:
            return False
        eligible = self.loop_accumulable.get(id(node))
        if not eligible:
            return False
        self.coalescing = {}
        self.coalescing_owner = id(node)
        self.coalescing_eligible = eligible
        self.coalesced_bindings = set()
        return True

    def end_coalescing(self, node):
        """
        Records the net change of an accumulated loop, one event per variable.

        Only the loop that started the run closes it, so an inner loop finishing
        does not flush the totals its parent is still gathering.

        Args:
        node (tuple): The loop node that has finished.
        """
        if self.coalescing_owner != id(node):
            return
        accumulated = self.coalescing
        self.coalescing = None
        self.coalescing_owner = None
        self.coalescing_eligible = frozenset()
        for var_name, net in accumulated.items():
            # A variable the loop left where it found it has nothing to undo.
            if net:
                self.record_change(var_name, ('delta', var_name, 'plus_assign', net))

    def execute_for(self, node):
        """
        Executes a for loop node.

        Args:
        node (tuple): The for loop node.
        """
        _, var_name, iterable, body = node

        self.begin_coalescing(node)
        try:
            self.run_for(node)
        finally:
            self.end_coalescing(node)

    def run_for(self, node):
        """
        Runs the iterations of a for loop.

        Args:
        node (tuple): The for loop node.
        """
        _, var_name, iterable, body = node

        if iterable[0] == 'range':
            _, start_value, end_value, step_value = iterable
            start_value = self.evaluate_expression(start_value)
            end_value = self.evaluate_expression(end_value)
            step_value = self.evaluate_expression(step_value) if step_value else 1

            current_value = start_value
            while current_value < end_value:
                self.bind_loop_variable(var_name, current_value)
                try:
                    self.execute_block(body)
                except BreakException:
                    break
                current_value += step_value
        else:
            if isinstance(iterable, list):
                iterable_value = [self.evaluate_expression(item) for item in iterable]
            else:
                iterable_value = self.evaluate_expression(iterable)
            if not isinstance(iterable_value, (list, str)):
                self.error(f'Variable "{iterable}" is not an iterable')

            for item in iterable_value:
                self.bind_loop_variable(var_name, item)
                try:
                    self.execute_block(body)
                except BreakException:
                    break

    def bind_loop_variable(self, var_name, value):
        """
        Binds a loop variable for one iteration, recording the state it replaced.

        The binding is recorded like any other assignment. Without it the loop
        variable would be the one piece of state a reversed loop could not put
        back, since nothing else says what it held before the loop began.

        In a compressed loop only the first binding is recorded. Restoring a
        value is absolute, so the state from before the first iteration is the
        only one reversal needs, and recording the rest would put back the
        per-iteration cost the compression exists to remove.

        Args:
        var_name (str): The loop variable.
        value (any): The value for this iteration.
        """
        if self.coalescing is None or var_name not in self.coalesced_bindings:
            self.record_change(var_name, ('value', var_name, self.symbol_table.get(var_name)))
            if self.coalescing is not None:
                self.coalesced_bindings.add(var_name)
        self.symbol_table[var_name] = value

    def execute_print(self, node):
        """
        Executes a print node.

        Args:
        node (tuple): The print node.
        """
        _, values = node
        output = []
        for value in values:
            evaluated_value = self.evaluate_expression(value)
            if isinstance(evaluated_value, str) and evaluated_value.startswith('"') and evaluated_value.endswith('"'):
                output.append(evaluated_value[1:-1])  # Strip the double quotations for displaying in the output
            elif isinstance(evaluated_value, str) and evaluated_value.startswith('`') and evaluated_value.endswith('`'):
                output.append(evaluated_value[1:-1])  # Strip the backticks for displaying in the output
            else:
                output.append(str(evaluated_value))
        print(" ".join(output))

    def evaluate_expression(self, expr):
        """
        Evaluates an expression.

        Args:
        expr (any): The expression to be evaluated.

        Returns:
        The evaluated result.
        """
        self.evaluations += 1
        if isinstance(expr, LazyEval):
            return expr.evaluate()

        if isinstance(expr, list):
            return [self.evaluate_expression(item) for item in expr]

        elif isinstance(expr, tuple):
            if len(expr) == 3:
                left, op, right = expr
                if op == 'index':
                    left_val = self.evaluate_expression(left)
                    right_val = self.evaluate_expression(right)
                    if isinstance(left_val, list):
                        return left_val[right_val]
                    else:
                        self.error(f"Cannot index non-list type: {left_val}")
                else:
                    left_val = self.evaluate_expression(left)
                    right_val = self.evaluate_expression(right)
                    return self.apply_operator(op, left_val, right_val)
            elif len(expr) == 2 and expr[0] == 'len':
                _, inner_expr = expr
                evaluated_expr = self.evaluate_expression(inner_expr)
                if isinstance(evaluated_expr, str) or isinstance(evaluated_expr, list):
                    return len(evaluated_expr)
                else:
                    self.error(f"len() function requires a string or list, got {type(evaluated_expr).__name__}")
            else:
                self.error(f"Unexpected tuple structure: {expr}")

        elif isinstance(expr, int) or isinstance(expr, bool):
            return expr

        elif isinstance(expr, str):
            if expr.startswith('`') and expr.endswith('`'):
                return expr
            elif expr.isnumeric() is False and not expr.startswith('"'):
                value = self.symbol_table.get(expr)
                if isinstance(value, LazyEval):
                    return value.evaluate()
                return value
        else:
            self.error(f"Unknown expression type: {expr}")

        return expr

    def apply_operator(self, op, left, right):
        """
        Applies an operator to two operands.

        Args:
        op (str): The operator.
        left (int): The left operand.
        right (int): The right operand.

        Returns:
        The result of the operation.
        """
        if isinstance(left, LazyEval):
            left = left.evaluate()
        if isinstance(right, LazyEval):
            right = right.evaluate()

        handler = self.operators.get(op)
        if handler is None:
            self.error(f'Unknown operator: {op}')

        c_function, guard, fallback = handler
        if guard(left, right):
            return c_function(left, right)
        return self.python_fallback(fallback, left, right)

    def python_fallback(self, fallback, left, right):
        """
        Applies the Python equivalent of an operation the C path cannot take.

        Args:
        fallback (callable): The Python implementation of the operation.
        left (any): The left operand.
        right (any): The right operand.

        Returns:
        The result of the operation.
        """
        try:
            return fallback(left, right)
        except ZeroDivisionError:
            self.error('Division by zero')
        except TypeError as type_error:
            self.error(f'Unsupported operand types: {type_error}')

    def execute_reverse(self, node):
        """
        Executes a reverse node.

        Args:
        node (tuple): The reverse node.
        """
        _, var_name = node
        if var_name is None:
            self.reverse_statement()
            return

        self.reversals += 1
        position = self.logstack.pop(var_name)
        if position is not None:
            current_value = self.symbol_table.get(var_name)
            event = self.trace.events[position]
            self.trace.consume(position)
            self.undo_event(event)

            # memory estimation required since, reversal keeps track of history consuming space.
            self.memory_manager.deallocate(sys.getsizeof(current_value))
            self.memory_manager.allocate(sys.getsizeof(self.symbol_table.get(var_name)))

    def reverse_statement(self):
        """
        Reverses the statement most recently completed in the enclosing block.

        This is the block form of `rev`, written without a variable name. Where
        `rev x` steps one variable back, this steps one whole statement back: an
        `if` reverses whichever branch actually ran, and a loop reverses every
        iteration it actually performed. Repeating it walks back through the
        block a statement at a time, which is the backward reading of the program
        the forward one just executed.

        Statements that changed nothing are stepped over rather than counted. A
        `print` has no state to restore, and output already written cannot be
        unwritten, so stopping on one would make `rev` look like it had done
        nothing. The same applies to a statement whose changes have each already
        been reversed by name.
        """
        marks = self.scopes[-1] if self.scopes else None
        while marks:
            mark = marks.pop()
            if self.trace.has_pending(mark):
                self.reverse_to(mark)
                return
        self.error('Nothing left to reverse in this block')

    def execute_revtrace(self, node):
        """
        Executes a revtrace node.

        Args:
        node (tuple): The revtrace node.
        """
        _, var_name, index_expr = node
        index = self.evaluate_expression(index_expr)  # support for both iterable variables and integers

        # Retrieve the previous state by walking the trace back from the present
        previous_value = self.describe_state(var_name, index)
        if previous_value is not None:
            print(f"Reverse Tracepath state {index} of {var_name}: {previous_value}")
        else:
            print(f"No state found for {var_name} at index {index}")

    def describe_state(self, var_name, index):
        """
        Returns the value a variable held `index` changes ago, without reversing.

        A self-invertible change records the operand rather than the value it
        replaced, so its earlier state is not stored anywhere and has to be
        worked out by inverting. That has to be done from the present backwards
        through every intervening change, which is why this walks rather than
        reading a single entry.

        Args:
        var_name (str): The variable to trace back.
        index (int): How many changes back to look.

        Returns:
        The value held at that point, or `None` if it is out of range.
        """
        value = self.evaluate_expression(self.symbol_table.get(var_name))
        steps = 0
        for position in self.logstack.positions(var_name):
            event = self.trace.events[position]
            if event is None:
                return None
            if event[0] == 'value':
                value = event[2]
            else:
                _, _, op, operand = event
                inverse = 'minus' if op == 'plus_assign' else 'plus'
                value = self.apply_operator(inverse, value, operand)
            steps += 1
            if steps == index:
                return value
        return None

    def prune_logstack(self):
        self.logstack.prune()
        if self.logstack.get_memory_usage() > 50:
            print("Warning: Memory usage exceeded 50 MB")

    def print_computation_cost(self):
        """
        Prints the computation cost of the execution.
        """
        print("\n~~~~~~~~~~~~~~COMPUTATION COSTS~~~~~~~~~~~~~~~~~\n")
        print(f"Assignments: {self.assignments}")
        print(f"Evaluations: {self.evaluations}")
        print(f"Reversals: {self.reversals}")
        memory_usage = self.get_memory_usage()
        print(f"Memory Usage: {memory_usage} MB")

    def get_memory_usage(self):
        """
        Gets the current memory usage.

        Returns:
        float: The memory usage in megabytes.
        """
        symbol_table_size = sys.getsizeof(self.symbol_table)
        total_size = symbol_table_size
        for key, value in self.symbol_table.items():
            total_size += sys.getsizeof(key)
            total_size += sys.getsizeof(value)
        return total_size / (1024 * 1024)

    def log_execution_details(self, start_time, end_time):
        """
        Logs the execution details to a file.

        Args:
        start_time (float): The start time of the execution.
        end_time (float): The end time of the execution.
        """
        num_threads = threading.active_count()
        execution_time = end_time - start_time
        try:
            with open("execution_log.txt", "a") as log_file:
                log_file.write(f"Execution Details ({datetime.now()}):\n")
                log_file.write(f"Execution Time: {execution_time} seconds\n")
                log_file.write(f"Number of Threads Used: {num_threads}\n")
                log_file.write(f"Assignments: {self.assignments}\n")
                log_file.write(f"Evaluations: {self.evaluations}\n")
                log_file.write(f"Reversals: {self.reversals}\n")
                log_file.write(f"Memory Usage: {self.get_memory_usage()} MB\n")
                log_file.write("\n")
        except OSError:
            # The log is a convenience, not part of running a program. A server
            # process with a read-only working directory should still be able to
            # run code, so a failure to write it is not allowed to fail the run.
            pass

    def error(self, message):
        """
        Raises an error with the given message.

        Args:
        message (str): The error message.
        """
        raise Exception(f'Execution error: {message}')
