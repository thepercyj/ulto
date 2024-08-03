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
    """
    Main function to run the Ulto program.

    Args:
    filename (str): The name of the Ulto file to be executed.
    """
    with open(filename, 'r') as file:
        code = file.read()

    tokens = tokenize(code)

    parser = Parser(tokens)
    ast = parser.parse()

    analyser = SemanticAnalyser(ast)
    analyser.analyse()

    engine = ExecutionEngine(ast)
    engine.execute()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ulto <filename>.ul")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.ul'):
        print("Error: The file must have a .ul extension")
        sys.exit(1)

    main(filename)
