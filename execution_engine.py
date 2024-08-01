# Ulto - Imperative Reversible Programming Language
#
# execution_engine.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>


import sys
import time
import threading
from datetime import datetime

class ExecutionEngine:
    def __init__(self, ast, symbol_table):
        self.ast = ast
        self.symbol_table = symbol_table
        self.history = []
        self.assignments = 0
        self.evaluations = 0
        self.reversals = 0
        self.energy_cost = 0

        # Define costs for operations
        self.costs = {
            'assignment': 1,  # Energy cost for assignment
            'evaluation': 2,  # Energy cost for evaluation
            'reversal': 3,  # Energy cost for reversal
            'function_call': 5,  # Energy cost for function call
        }

    def execute(self):
        start_time = time.time()
        for node in self.ast:
            self.execute_node(node)
        end_time = time.time()
        print("Execution finished")
        print("Final state of variables:", self.symbol_table)
        self.print_computation_cost()
        self.log_execution_details(start_time, end_time)

    def execute_node(self, node):
        if node[0] == 'assign':
            self.execute_assignment(node)
        elif node[0] == 'reverse':
            self.execute_reverse(node)
        elif node[0] == 'if':
            self.execute_if(node)
        elif node[0] == 'while':
            self.execute_while(node)
        elif node[0] == 'print':
            self.execute_print(node)
        elif node[0] == 'import':
            self.execute_import(node)
        elif node[0] == 'class':
            self.execute_class(node)
        elif node[0] == 'function':
            self.execute_function(node)
        elif node[0] == 'return':
            pass  # Handle return if necessary in function execution
        else:
            self.error(f'Unknown node type: {node[0]}')

    def execute_assignment(self, node):
        self.assignments += 1
        self.energy_cost += self.costs['assignment']
        _, var_name, value = node
        evaluated_value = self.evaluate_expression(value)
        print(f"Evaluated value of {var_name}: {evaluated_value}")
        previous_value = self.symbol_table.get(var_name, None)
        if var_name not in self.symbol_table:
            self.symbol_table[var_name] = None  # Initialize if not present
        self.history.append((var_name, previous_value))
        self.symbol_table[var_name] = evaluated_value
        print(f"Updated value of {var_name}: {self.symbol_table[var_name]}")

    def execute_if(self, node):
        _, condition, true_branch, false_branch = node
        condition_result = self.evaluate_expression(condition)
        if condition_result:
            for stmt in true_branch:
                self.execute_node(stmt)
        else:
            for stmt in false_branch:
                self.execute_node(stmt)

    def execute_while(self, node):
        _, condition, body = node
        while self.evaluate_expression(condition):
            for stmt in body:
                self.execute_node(stmt)

    def execute_print(self, node):
        _, value = node
        evaluated_value = self.evaluate_expression(value)
        print(evaluated_value)

    def evaluate_expression(self, expr):
        self.evaluations += 1
        self.energy_cost += self.costs['evaluation']
        if isinstance(expr, list):
            return [self.evaluate_expression(item) for item in expr]
        elif isinstance(expr, tuple) and len(expr) == 3:
            left = self.evaluate_expression(expr[0])
            op = expr[1]
            right = self.evaluate_expression(expr[2])
            if op == 'plus':
                result = left + right
            elif op == 'minus':
                result = left - right
            elif op == 'times':
                result = left * right
            elif op == 'over':
                result = left / right
            elif op == 'eq':
                result = left == right
            elif op == 'neq':
                result = left != right
            elif op == 'lt':
                result = left < right
            elif op == 'gt':
                result = left > right
            elif op == 'lte':
                result = left <= right
            elif op == 'gte':
                result = left >= right
            else:
                self.error(f'Unknown operator: {op}')
            print(f"Evaluating: {left} {op} {right} = {result}")
            return result
        elif isinstance(expr, int):
            return expr
        elif isinstance(expr, str):
            if expr.startswith('"') and expr.endswith('"'):
                return expr[1:-1]  # Return the string literal without quotes
            elif expr in self.symbol_table:
                return self.symbol_table[expr]
            else:
                self.error(f'Undefined variable or non-numeric value: {expr}')
        return expr

    def execute_reverse(self, node):
        self.reversals += 1
        self.energy_cost += self.costs['reversal']
        _, var_name = node
        previous_value = self.find_previous_value(var_name)
        print(f"Previous value of {var_name}: {previous_value}")  # Debug statement
        if previous_value is not None or var_name in self.symbol_table:
            self.history.append((var_name, self.symbol_table[var_name]))
            self.symbol_table[var_name] = previous_value
            print(f"Reversed value of {var_name}: {self.symbol_table[var_name]}")
        else:
            self.error(f'No previous value found for variable "{var_name}"')

    def find_previous_value(self, var_name):
        print(f"Finding previous value for {var_name}")  # Debug statement
        for var, value in reversed(self.history):
            if var == var_name:
                print(f"Previous value found: {value}")  # Debug statement
                self.history.remove((var, value))  # Remove the found value
                return value
        return None

    def execute_import(self, node):
        _, module_name = node
        # Implement import logic as needed
        print(f"Imported module: {module_name}")

    def execute_class(self, node):
        _, class_name, methods = node
        self.symbol_table[class_name] = {
            'type': 'class',
            'methods': {method[1]: method for method in methods}
        }
        print(f"Defined class: {class_name}")

    def execute_function(self, node):
        _, func_name, params, body = node
        # Implement function execution logic as needed
        print(f"Defined function: {func_name}")

    def error(self, message):
        raise Exception(f'Execution error: {message}')

    def print_computation_cost(self):
        print("\nComputation Cost:")
        print(f"Assignments: {self.assignments}")
        print(f"Evaluations: {self.evaluations}")
        print(f"Reversals: {self.reversals}")
        print(f"Energy Cost: {self.energy_cost} units")
        memory_usage = self.get_memory_usage()
        print(f"Memory Usage: {memory_usage} bytes")

    def get_memory_usage(self):
        symbol_table_size = sys.getsizeof(self.symbol_table)
        history_size = sys.getsizeof(self.history)
        total_size = symbol_table_size + history_size
        for key, value in self.symbol_table.items():
            total_size += sys.getsizeof(key)
            total_size += sys.getsizeof(value)
        for entry in self.history:
            total_size += sys.getsizeof(entry)
        return total_size

    def log_execution_details(self, start_time, end_time):
        num_threads = threading.active_count()
        execution_time = end_time - start_time
        with open("execution_log.txt", "a") as log_file:
            log_file.write(f"Execution Details ({datetime.now()}):\n")
            log_file.write(f"Execution Time: {execution_time} seconds\n")
            log_file.write(f"Number of Threads Used: {num_threads}\n")
            log_file.write(f"Assignments: {self.assignments}\n")
            log_file.write(f"Evaluations: {self.evaluations}\n")
            log_file.write(f"Reversals: {self.reversals}\n")
            log_file.write(f"Energy Cost: {self.energy_cost} units\n")
            log_file.write(f"Memory Usage: {self.get_memory_usage()} bytes\n")
            log_file.write("\n")

