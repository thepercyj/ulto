import sys
import threading
import time
from datetime import datetime


class ExecutionEngine:
    def __init__(self, ast, symbol_table):
        self.ast = ast
        self.symbol_table = symbol_table
        self.history = []
        self.assignments = 0
        self.evaluations = 0
        self.reversals = 0

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
        else:
            self.error(f'Unknown node type: {node[0]}')

    def execute_assignment(self, node):
        self.assignments += 1
        _, var_name, value = node
        evaluated_value = self.evaluate_expression(value)
        print(f"Evaluated value of {var_name}: {evaluated_value}")
        previous_value = self.symbol_table.get(var_name, None)
        if var_name not in self.symbol_table:
            self.symbol_table[var_name] = None
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

    def evaluate_expression(self, expr):
        self.evaluations += 1
        if isinstance(expr, tuple) and len(expr) == 3:
            left = self.evaluate_expression(expr[0])
            op = expr[1]
            right = self.evaluate_expression(expr[2])
            if op == 'plus':
                result = left + right
            elif op == 'minus':
                result = left - right
            elif op == 'multiply':
                result = left * right
            elif op == 'divide':
                result = left / right
            elif op == '==':
                result = left == right
            print(f"Evaluating: {left} {op} {right} = {result}")
            return result
        elif isinstance(expr, int):
            return expr
        elif isinstance(expr, str):
            if expr in self.symbol_table:
                return self.symbol_table[expr]
            else:
                self.error(f'Undefined variable or non-numeric value: {expr}')
        return expr

    def execute_reverse(self, node):
        self.reversals += 1
        _, var_name = node
        previous_value = self.find_previous_value(var_name)
        print(f"Previous value of {var_name}: {previous_value}")
        if previous_value is not None or var_name in self.symbol_table:
            self.history.append((var_name, self.symbol_table[var_name]))
            self.symbol_table[var_name] = previous_value
            print(f"Reversed value of {var_name}: {self.symbol_table[var_name]}")
        else:
            self.error(f'No previous value found for variable "{var_name}"')

    def find_previous_value(self, var_name):
        print(f"Finding previous value for {var_name}")
        for var, value in reversed(self.history):
            if var == var_name:
                print(f"Previous value found: {value}")
                self.history.remove((var, value))
                return value
        return None

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
            log_file.write(f"Memory Usage: {self.get_memory_usage()} bytes\n")
            log_file.write("\n")


if __name__ == '__main__':
    from semantic_analyser import SemanticAnalyser
    from ulto_parser import Parser
    from lexer import tokenize

    code = """
    assign x to 5
    assign y to x plus 3
    reverse y
    assign z to x minus 2
    assign z to x
    reverse z
    assign w to x times 4
    assign v to x over 2
    if x == 5
    assign a to 1
    else
    assign a to 2
    endif
    """

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

    analyser = SemanticAnalyser(ast)
    analyser.analyse()

    engine = ExecutionEngine(ast, analyser.symbol_table)
    engine.execute()

    print(engine.symbol_table)
