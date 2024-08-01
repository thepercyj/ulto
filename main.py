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
    # Read the code from the file
    with open(filename, 'r') as file:
        code = file.read()

    # Tokenize the code
    tokens = tokenize(code)
    print("Tokens:", tokens)

    # Parse the tokens into an AST
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    # Perform semantic analysis
    analyser = SemanticAnalyser(ast)
    analyser.analyse()

    # Execute the AST
    engine = ExecutionEngine(ast, analyser.symbol_table)
    engine.execute()

    # Print the final state of the variables
    print("Final state of variables:", engine.symbol_table)


if __name__ == '__main__':
    # Check if the filename is provided
    if len(sys.argv) != 2:
        print("Usage: ulto <filename>.ul")
        sys.exit(1)

    filename = sys.argv[1]
    # Check if the file has the correct extension
    if not filename.endswith('.ul'):
        print("Error: The file must have a .ul extension")
        sys.exit(1)

    main(filename)
