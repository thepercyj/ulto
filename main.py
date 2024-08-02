# Ulto - Imperative Reversible Programming Language
#
# main.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>


import sys
from lexer import tokenize
from ulto_parser import Parser
from execution_engine import ExecutionEngine
from semantic_analyser import SemanticAnalyser

def main(filename):
    with open(filename, 'r') as file:
        code = file.read()

    tokens = tokenize(code)

    parser = Parser(tokens)
    ast = parser.parse()

    analyser = SemanticAnalyser(ast)
    analyser.analyse()

    engine = ExecutionEngine(ast, analyser.symbol_table)
    engine.execute()

    # # Trace back computations for variable 'b'
    # trace_steps = engine.trace_back('b')
    # print("\nTracing back steps for variable 'b':")
    # for step in trace_steps:
    #     var, new_val, prev_val, step_num = step
    #     print(f"{var}: {new_val} -> {prev_val} at step {step_num}")
    #
    # # Navigate to specific steps in the sequence
    # steps_to_navigate = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Example steps
    # for step in steps_to_navigate:
    #     engine.navigate_to_step(step)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ulto <filename>.ulto")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.ul'):
        print("Error: The file must have a .ul extension")
        sys.exit(1)

    main(filename)

