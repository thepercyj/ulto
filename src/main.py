# Ulto - Imperative Reversible Programming Language
#
# main.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

import sys
from src.lexer import tokenize
from src.parser import Parser
from src.interpreter import Interpreter
from src.semantic_analyser import SemanticAnalyser


def main():
    """
    Main function to run the Ulto program.
    """
    if len(sys.argv) != 2:
        print("Usage: ulto <filename>.ul")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.ul'):
        print("Error: The file must have a .ul extension")
        sys.exit(1)

    with open(filename, 'r') as file:
        code = file.read()

    tokens = tokenize(code)

    parser = Parser(tokens)
    ast = parser.parse()

    analyser = SemanticAnalyser(ast)
    analyser.analyse()

    engine = Interpreter(ast)
    engine.execute()


if __name__ == '__main__':
    main()
