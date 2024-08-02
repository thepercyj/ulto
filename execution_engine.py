# Ulto - Imperative Reversible Programming Language
#
# execution_engine.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>


import sys
import time
import threading
from datetime import datetime
import subprocess


class ExecutionEngine:
    def __init__(self, ast, symbol_table):
        self.ast = ast
        self.symbol_table = symbol_table
        self.history = []
        self.detailed_history = []
        self.assignments = 0
        self.evaluations = 0
        self.reversals = 0
        self.current_step = 0

    def execute(self):
        start_time = time.time()
        try:
            for node in self.ast:
                self.execute_node(node)
        finally:
            end_time = time.time()
            self.print_computation_cost()
            self.log_execution_details(start_time, end_time)

    def execute_node(self, node):
        node_type = node[0]
        if node_type == 'assign':
            self.execute_assignment(node)
        elif node_type == 'reverse':
            self.execute_reverse(node)
        elif node_type == 'if':
            self.execute_if(node)
        elif node_type == 'while':
            self.execute_while(node)
        elif node_type == 'print':
            self.execute_print(node)
        else:
            self.error(f'Unknown node type: {node_type}')

    def execute_assignment(self, node):
        self.assignments += 1
        _, var_name, value = node
        evaluated_value = self.evaluate_expression(value)
        previous_value = self.symbol_table.get(var_name, None)
        self.history.append((var_name, previous_value))
        self.detailed_history.append((var_name, previous_value, evaluated_value, self.current_step))
        self.symbol_table[var_name] = evaluated_value
        self.current_step += 1

    def execute_if(self, node):
        _, condition, true_branch, false_branch = node
        condition_result = self.evaluate_expression(condition)
        branch = true_branch if condition_result else false_branch
        for stmt in branch:
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
            return self.symbol_table.get(expr, expr[1:-1] if expr.startswith('"') and expr.endswith('"') else None)
        return expr

    def apply_operator(self, op, left, right):
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
        self.reversals += 1
        _, var_name = node
        previous_value = self.find_previous_value(var_name)
        self.history.append((var_name, self.symbol_table[var_name]))
        self.symbol_table[var_name] = previous_value

    def find_previous_value(self, var_name):
        for var, value in reversed(self.history):
            if var == var_name:
                self.history.remove((var, value))
                return value
        return None

    def trace_back(self, var_name):
        steps = []
        for var, prev_val, new_val, step in reversed(self.detailed_history):
            if var == var_name:
                steps.append((var, new_val, prev_val, step))
        return steps

    def navigate_to_step(self, step):
        if step < 0 or step >= len(self.detailed_history):
            print("Invalid step")
            return
        for var, prev_val, new_val, s in self.detailed_history:
            if s == step:
                self.symbol_table[var] = new_val

    # def start_energy_measurement(self):
    #     power_log_path = "C:\\Program Files\\Intel\\Power Gadget 3.6\\PowerLog3.0.exe"
    #     output_csv_path = "C:\\Users\\amany\\Documents\\PwrData.csv"
    #
    #     # Start the PowerLog process with the -cmd flag
    #     process = subprocess.Popen([power_log_path, '-file', output_csv_path, '-cmd'], stdout=subprocess.PIPE)
    #     return process

    # def stop_energy_measurement(self, process, duration):
    #     # Calculate the duration for the PowerLog process
    #     duration_str = f"{int(duration)}s"
    #
    #     # Stop the PowerLog process after the duration
    #     time.sleep(duration)
    #     process.terminate()
    #     process.wait()
    #
    #     output_csv_path = "C:\\Users\\amany\\Documents\\PwrData.csv"
    #     with open(output_csv_path, "r") as file:
    #         lines = file.readlines()
    #
    #     # Ensure there are enough lines in the CSV file
    #     if len(lines) < 3:
    #         raise Exception("Not enough data in the CSV file to calculate energy usage.")
    #
    #     # Find the index of the "Cumulative IA Energy_0 (Joules)" column
    #     header = lines[0].strip().split(',')
    #     try:
    #         energy_index = header.index('Cumulative IA Energy_0(Joules)')
    #     except ValueError:
    #         raise Exception("Cumulative IA Energy_0(Joules) column not found in CSV header.")
    #
    #     # Extract the energy usage from the first and last relevant entries
    #     start_energy = None
    #     end_energy = None
    #
    #     for line in lines[1:]:
    #         if len(line.strip().split(',')) > energy_index:
    #             start_energy = float(line.strip().split(',')[energy_index])
    #             break
    #
    #     for line in reversed(lines[:-1]):  # Skip the summary line
    #         if len(line.strip().split(',')) > energy_index:
    #             end_energy = float(line.strip().split(',')[energy_index])
    #             break
    #
    #     if start_energy is None or end_energy is None:
    #         raise Exception("Unable to determine start or end energy usage from CSV data.")
    #
    #     return end_energy - start_energy

    def execute_import(self, node):
        _, module_name = node

    def execute_class(self, node):
        _, class_name, methods = node
        self.symbol_table[class_name] = {
            'type': 'class',
            'methods': {method[1]: method for method in methods}
        }

    def execute_function(self, node):
        _, func_name, params, body = node

    def error(self, message):
        raise Exception(f'Execution error: {message}')

    def print_computation_cost(self):
        print("\nComputation Cost:")
        print(f"Assignments: {self.assignments}")
        print(f"Evaluations: {self.evaluations}")
        print(f"Reversals: {self.reversals}")
        memory_usage = self.get_memory_usage()
        print(f"Memory Usage: {memory_usage} bytes")

    def get_memory_usage(self):
        symbol_table_size = sys.getsizeof(self.symbol_table)
        history_size = sys.getsizeof(self.history)
        detailed_history_size = sys.getsizeof(self.detailed_history)
        total_size = symbol_table_size + history_size + detailed_history_size
        for key, value in self.symbol_table.items():
            total_size += sys.getsizeof(key)
            total_size += sys.getsizeof(value)
        for entry in self.history:
            total_size += sys.getsizeof(entry)
        for entry in self.detailed_history:
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
            # log_file.write(f"Energy Consumed: {energy_used:.2f} joules\n")
            log_file.write(f"Memory Usage: {self.get_memory_usage()} bytes\n")
            log_file.write("\n")



