from interpreter import Interpreter
from lexer import Lexer
from ulto_parser import Parser

code = """
x = 5
y = x + 3
print y
x = y - 2
print x
"""

lexer = Lexer(code)
parser = Parser(lexer)
nodes = parser.parse()

interpreter = Interpreter()
interpreter.interpret(nodes)
print("Reversing last operation")
interpreter.reverse()
print(interpreter.variables)
