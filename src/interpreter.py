# Ulto - Imperative Reversible Programming Language
#
# interpreter.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

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
from sortedcontainers import SortedDict


class BreakException(Exception):
    pass


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
        self.logstack = LogStack()

        # Determining the OS family
        system = platform.system()
        # loading machine compiled arithmetic and compound assignment file.
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if system == "Windows":
            lib_path = os.path.join(script_dir, 'operations.dll')
        else:  # If Linux or other Unix-like systems
            lib_path = os.path.join(script_dir, 'liboperations.so')

        self.lib = ctypes.CDLL(lib_path)

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

    def execute(self):
        """
        Executes the AST.
        """
        print("\n~~~~~~~~~~~~~~~~~~~~OUTPUT~~~~~~~~~~~~~~~~~~~~\n")
        start_time = time.time()
        try:
            # collecting profiling data to find hotspots and manage accordingly during runtime.
            self.collect_profiling_data(self.ast)
            # for detecting eager variables that are often used in the source code, preprocessing it at the start of AST execution.
            self.detect_eager_vars()
            for node in self.ast:
                self.execute_node(node)
                self.prune_logstack()
        finally:
            end_time = time.time()
            self.print_computation_cost()
            self.log_execution_details(start_time, end_time)

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
            lazy_value = LazyEval(value, self)

        previous_value = self.symbol_table.get(var_name, None)

        # estimates memory use and pools itself for only what is required to perform operations below the set threshold.
        size = sys.getsizeof(lazy_value)
        self.memory_manager.allocate(size)

        # deallocate memory based on previous value for re-usability on a different operation.
        if previous_value is not None:
            prev_size = sys.getsizeof(previous_value)
            self.memory_manager.deallocate(prev_size)

        self.logstack.push(var_name, previous_value)
        self.symbol_table[var_name] = lazy_value

    def execute_plus_assign(self, node):
        """
        Executes a plus assignment operation (`+=`) on a variable.

        Args:
            node (tuple): A tuple containing the operation and the variable name, and the value
                          to be added. Expected format: (_, var_name, value).

        Raises:
            KeyError: If `var_name` is not found in the symbol table.
        """
        _, var_name, value = node
        current_value = self.symbol_table.get(var_name)
        if isinstance(current_value, LazyEval):
            current_value = current_value.evaluate()
        addition_value = self.evaluate_expression(value)
        if isinstance(addition_value, LazyEval):
            addition_value = addition_value.evaluate()
        # Log current value for maybe reversal in logstack
        self.logstack.push(var_name, current_value)
        new_value = self.lib.execute_add_assign(ctypes.byref(ctypes.c_int(current_value)), addition_value)
        # If lazy, wrap it in LazyEval again
        if var_name in self.eager_vars:
            self.symbol_table[var_name] = new_value
        else:
            self.symbol_table[var_name] = LazyEval(new_value, self)

    def execute_minus_assign(self, node):
        """
        Executes a minus assignment operation (`-=`) on a variable.

        Args:
            node (tuple): A tuple containing the operation and the variable name, and the value
                          to be subtracted. Expected format: (_, var_name, value).

        Raises:
            KeyError: If `var_name` is not found in the symbol table.
        """
        _, var_name, value = node
        current_value = self.symbol_table.get(var_name)
        if isinstance(current_value, LazyEval):
            current_value = current_value.evaluate()
        subtraction_value = self.evaluate_expression(value)
        if isinstance(subtraction_value, LazyEval):
            subtraction_value = subtraction_value.evaluate()
        # Log current value for maybe reversal in logstack
        self.logstack.push(var_name, current_value)
        new_value = self.lib.execute_sub_assign(ctypes.byref(ctypes.c_int(current_value)), subtraction_value)
        # If lazy, wrap it in LazyEval again
        if var_name in self.eager_vars:
            self.symbol_table[var_name] = new_value
        else:
            self.symbol_table[var_name] = LazyEval(new_value, self)

    def execute_times_assign(self, node):
        """
        Executes a times assignment operation (`*=`) on a variable.

        Args:
            node (tuple): A tuple containing the operation and the variable name, and the value
                          to be multiplied. Expected format: (_, var_name, value).

        Raises:
            KeyError: If `var_name` is not found in the symbol table.
        """
        _, var_name, value = node
        current_value = self.symbol_table.get(var_name)
        if isinstance(current_value, LazyEval):
            current_value = current_value.evaluate()
        multiplication_value = self.evaluate_expression(value)
        if isinstance(multiplication_value, LazyEval):
            multiplication_value = multiplication_value.evaluate()
        # Log current value for maybe reversal in logstack
        self.logstack.push(var_name, current_value)
        new_value = self.lib.execute_mul_assign(ctypes.byref(ctypes.c_int(current_value)), multiplication_value)
        # If lazy, wrap it in LazyEval again
        if var_name in self.eager_vars:
            self.symbol_table[var_name] = new_value
        else:
            self.symbol_table[var_name] = LazyEval(new_value, self)

    def execute_over_assign(self, node):
        """
         Executes a division assignment operation (`/=`) on a variable.

         Args:
             node (tuple): A tuple containing the operation and the variable name, and the value
                           to be divided. Expected format: (_, var_name, value).

         Raises:
             KeyError: If `var_name` is not found in the symbol table.
         """
        _, var_name, value = node
        current_value = self.symbol_table.get(var_name)
        if isinstance(current_value, LazyEval):
            current_value = current_value.evaluate()
        division_value = self.evaluate_expression(value)
        if isinstance(division_value, LazyEval):
            division_value = division_value.evaluate()
        # Log current value for maybe reversal in logstack
        self.logstack.push(var_name, current_value)
        new_value = self.lib.execute_div_assign(ctypes.byref(ctypes.c_int(current_value)), division_value)
        # If lazy, wrap it in LazyEval again
        if var_name in self.eager_vars:
            self.symbol_table[var_name] = new_value
        else:
            self.symbol_table[var_name] = LazyEval(new_value, self)

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

        for stmt in branch:
            self.execute_node(stmt)

    def execute_while(self, node):
        """
        Executes a while node.

        Args:
        node (tuple): The while node.
        """
        _, condition, body = node

        if isinstance(condition, tuple) and len(condition) == 3:
            left, op, right = condition

            if op == 'lt' and isinstance(right, int):
                n_value = self.evaluate_expression(right)
                while self.evaluate_expression(left) < n_value:
                    for stmt in body:
                        self.execute_node(stmt)
                    # Eagerly evaluate i to avoid re-evaluation
                    self.symbol_table[left] = self.evaluate_expression(self.symbol_table.get(left)) + 1
            else:
                while self.evaluate_expression(condition):
                    try:
                        for stmt in body:
                            self.execute_node(stmt)
                    except BreakException:
                        break
        else:
            while self.evaluate_expression(condition):
                try:
                    for stmt in body:
                        self.execute_node(stmt)
                except BreakException:
                    break

    def execute_for(self, node):
        """
        Executes a for loop node.

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
                self.symbol_table[var_name] = current_value
                try:
                    for stmt in body:
                        self.execute_node(stmt)
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
                self.symbol_table[var_name] = item
                try:
                    for stmt in body:
                        self.execute_node(stmt)
                except BreakException:
                    break

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
            if expr._evaluated_value is None:
                expr._evaluated_value = self.evaluate_expression(expr.expression)
            return expr._evaluated_value

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
        if op == 'plus':
            try:
                result = self.lib.execute_add(left, right)
                if result is None:
                    raise ValueError("execute_add returned None")
            except Exception:
                result = left + right
            return result
        elif op == 'minus':
            try:
                result = self.lib.execute_sub(left, right)
                if result is None:
                    raise ValueError("execute_sub returned None")
            except Exception:
                result = left - right
            return result
        elif op == 'times':
            try:
                result = self.lib.execute_mul(left, right)
                if result is None:
                    raise ValueError("execute_mul returned None")
            except Exception:
                result = left * right
            return result
        elif op == 'over':
            try:
                result = self.lib.execute_div(left, right)
                if result is None:
                    raise ValueError("execute_div returned None")
            except Exception:
                result = left / right
            return result
        elif op == 'modulo':
            try:
                result = self.lib.execute_modulo(left, right)
                if result is None:
                    raise ValueError("execute_modulo returned None")
            except Exception:
                result = left % right
            return result
        elif op == 'int_div':
            try:
                result = self.lib.execute_int_div(left, right)
                if result is None:
                    raise ValueError("execute_int_div returned None")
            except Exception:
                result = left // right
            return result
        elif op == 'eq':
            try:
                result = self.lib.execute_eq(left, right)
                if result is None:
                    raise ValueError("execute_eq returned None")
            except Exception:
                result = left == right
            return result
        elif op == 'neq':
            try:
                result = self.lib.execute_neq(left, right)
                if result is None:
                    raise ValueError("execute_neq returned None")
            except Exception:
                result = left != right
            return result
        elif op == 'lt':
            try:
                result = self.lib.execute_lt(left, right)
                if result is None:
                    raise ValueError("execute_lt returned None")
            except Exception:
                result = left < right
            return result
        elif op == 'gt':
            try:
                result = self.lib.execute_gt(left, right)
                if result is None:
                    raise ValueError("execute_gt returned None")
            except Exception:
                result = left > right
            return result
        elif op == 'lte':
            try:
                result = self.lib.execute_lte(left, right)
                if result is None:
                    raise ValueError("execute_lte returned None")
            except Exception:
                result = left <= right
            return result
        elif op == 'gte':
            try:
                result = self.lib.execute_gte(left, right)
                if result is None:
                    raise ValueError("execute_gte returned None")
            except Exception:
                result = left >= right
            return result
        elif op == 'and':
            try:
                result = self.lib.execute_and(left, right)

                if result is None:
                    raise ValueError("execute_and returned None")
            except Exception:
                result = left and right
            return result
        elif op == 'or':
            try:
                result = self.lib.execute_or(left, right)
                if result is None:
                    raise ValueError("execute_or returned None")
            except Exception:
                result = left or right
            return result
        else:
            self.error(f'Unknown operator: {op}')

    def execute_reverse(self, node):
        """
        Executes a reverse node.

        Args:
        node (tuple): The reverse node.
        """
        self.reversals += 1
        if node[0] == 'reversible_block':
            _, block = node
            for stmt in reversed(block):
                self.execute_node(stmt)
        else:
            _, var_name = node
            previous_value = self.logstack.pop(var_name)
            if previous_value is not None:
                self.symbol_table[var_name] = previous_value

                # memory estimation required since, reversal keeps track of history consuming space.
                current_size = sys.getsizeof(self.symbol_table[var_name])
                prev_size = sys.getsizeof(previous_value)
                self.memory_manager.deallocate(current_size)
                self.memory_manager.allocate(prev_size)

    def execute_revtrace(self, node):
        """
        Executes a revtrace node.

        Args:
        node (tuple): The revtrace node.
        """
        _, var_name, index_expr = node
        index = self.evaluate_expression(index_expr)  # support for both iterable variables and integers

        # Retrieve the previous value from the reverse log stack
        previous_value = self.logstack.peek(var_name, index)
        if previous_value is not None:
            print(f"Reverse Tracepath state {index} of {var_name}: {previous_value}")
        else:
            print(f"No state found for {var_name} at index {index}")

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
        with open("execution_log.txt", "a") as log_file:
            log_file.write(f"Execution Details ({datetime.now()}):\n")
            log_file.write(f"Execution Time: {execution_time} seconds\n")
            log_file.write(f"Number of Threads Used: {num_threads}\n")
            log_file.write(f"Assignments: {self.assignments}\n")
            log_file.write(f"Evaluations: {self.evaluations}\n")
            log_file.write(f"Reversals: {self.reversals}\n")
            log_file.write(f"Memory Usage: {self.get_memory_usage()} MB\n")
            log_file.write("\n")

    def error(self, message):
        """
        Raises an error with the given message.

        Args:
        message (str): The error message.
        """
        raise Exception(f'Execution error: {message}')
