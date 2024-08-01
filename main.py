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
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    analyser = SemanticAnalyser(ast)
    analyser.analyse()

    engine = ExecutionEngine(ast, analyser.symbol_table)
    engine.execute()

    print("Final state of variables:", engine.symbol_table)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ulto <filename>.ul")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.ul'):
        print("Error: The file must have a .ul extension")
        sys.exit(1)

    main(filename)