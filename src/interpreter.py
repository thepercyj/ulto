# Ulto - Imperative Reversible Programming Language
#
# interpreter.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import sys
import time
import threading
from datetime import datetime
from src.core.malloc import MemoryManager
from src.core.lazyeval import LazyEval
from src.core.logstack import LogStack
from sortedcontainers import SortedDict


class Interpreter:
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
        _, condition, true_branch, false_branch = node
        self.update_profiling_data(condition)
        for stmt in true_branch:
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
        # threshold set to 3 to avoid inaccuracy of dealing hotspots, can shift it to 5 for reducing overhead but for now is good. can be tweaked based on nature of application.
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
        elif node_type == 'while':
            self.execute_while(node)
        elif node_type == 'print':
            self.execute_print(node)
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

        # Considering hybrid approach since, some programs developed can have circular dependency. Hence, based on the source code profile eager and lazy accordingly.
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

        # deallocate memory based on previous value for reusability on a different operation.
        if previous_value is not None:
            prev_size = sys.getsizeof(previous_value)
            self.memory_manager.deallocate(prev_size)

        self.logstack.push(var_name, previous_value)
        self.symbol_table[var_name] = lazy_value

    def execute_if(self, node):
        """
        Executes an if node.

        Args:
        node (tuple): The if node.
        """
        _, condition, true_branch, false_branch = node
        condition_result = self.evaluate_expression(condition)
        branch = true_branch if condition_result else false_branch
        for stmt in branch:
            self.execute_node(stmt)

    def execute_while(self, node):
        """
        Executes a while node.

        Args:
        node (tuple): The while node.
        """
        _, condition, body = node
        while self.evaluate_expression(condition):
            for stmt in body:
                self.execute_node(stmt)

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
        elif isinstance(expr, tuple) and len(expr) == 3:
            left, op, right = expr
            left_val = self.evaluate_expression(left)
            right_val = self.evaluate_expression(right)
            return self.apply_operator(op, left_val, right_val)
        elif isinstance(expr, int):
            return expr
        elif isinstance(expr, str):
            # Handle string literals and backtick-enclosed comments correctly
            if expr.startswith('`') and expr.endswith('`'):
                return expr  # Return the entire string as it is
            elif isinstance(expr, str) and expr.isnumeric() is False and (
                    expr.startswith('"') and expr.endswith('"')) == False:
                value = self.symbol_table.get(expr)
                if isinstance(value, LazyEval):
                    return value.evaluate()
                return value
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
        if op == 'plus':
            return left + right
        elif op == 'minus':
            return left - right
        elif op == 'times':
            return left * right
        elif op == 'over':
            return left / right
        elif op == 'eq':
            return left == right
        elif op == 'neq':
            return left != right
        elif op == 'lt':
            return left < right
        elif op == 'gt':
            return left > right
        elif op == 'lte':
            return left <= right
        elif op == 'gte':
            return left >= right
        else:
            self.error(f'Unknown operator: {op}')

    def execute_reverse(self, node):
        """
        Executes a reverse node.

        Args:
        node (tuple): The reverse node.
        """
        self.reversals += 1
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
        _, var_name, index = node
        index = int(index)  # Ensure index is treated as an integer

        # Retrieve the previous value from the reverse log stack
        previous_value = self.logstack.peek(var_name, index)
        if previous_value is not None:
            print(f"Reversed state {index} of {var_name}: {previous_value}")
        else:
            print(f"No state found for {var_name} at index {index}")

    def get_previous_value(self, var_name, index):
        """
        Retrieves the previous value of a variable from the log stack by index.

        Args:
        var_name (str): The name of the variable.
        index (int): The index of the state to retrieve.

        Returns:
        The previous value of the variable or None if not found.
        """
        values = []
        while len(values) < index:
            previous_value = self.logstack.pop(var_name)
            if previous_value is None:
                break
            values.append(previous_value)

        # Restoring the log stack state to tracepath assignment history
        for value in reversed(values):
            self.logstack.push(var_name, value)

        if index <= len(values):
            return values[index - 1]
        else:
            return None

    def execute_import(self, node):
        """
        Executes an import node.

        Args:
        node (tuple): The import node.
        """
        _, module_name = node

    def execute_class(self, node):
        """
        Executes a class node.

        Args:
        node (tuple): The class node.
        """
        _, class_name, methods = node
        self.symbol_table[class_name] = {
            'type': 'class',
            'methods': {method[1]: method for method in methods}
        }

    def execute_function(self, node):
        """
        Executes a function node.

        Args:
        node (tuple): The function node.
        """
        _, func_name, params, body = node

    def error(self, message):
        """
        Raises an error with the given message.

        Args:
        message (str): The error message.
        """
        raise Exception(f'Execution error: {message}')

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
        print(f"Memory Usage: {memory_usage:.2f} MB")

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
        with open("../execution_log.txt", "a") as log_file:
            log_file.write(f"Execution Details ({datetime.now()}):\n")
            log_file.write(f"Execution Time: {execution_time} seconds\n")
            log_file.write(f"Number of Threads Used: {num_threads}\n")
            log_file.write(f"Assignments: {self.assignments}\n")
            log_file.write(f"Evaluations: {self.evaluations}\n")
            log_file.write(f"Reversals: {self.reversals}\n")
            log_file.write(f"Memory Usage: {self.get_memory_usage()} MB\n")
            log_file.write("\n")
