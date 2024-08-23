from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from src.lexer import tokenize
from src.parser import Parser
from src.semantic_analyser import SemanticAnalyser
from src.interpreter import Interpreter

app = Flask(__name__)

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests/examples')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/codespace')
def codespace():
    return render_template('codespace.html')


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/vardata')
def vardata():
    return render_template('vardata.html')


@app.route('/control')
def control():
    return render_template('control.html')


@app.route('/reverse')
def reverse():
    return render_template('reverse.html')


@app.route('/docstrings')
def docstrings():
    return render_template('html/index.html')


@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code', '')

    tokens = tokenize(code)

    parser = Parser(tokens)
    ast = parser.parse()

    analyser = SemanticAnalyser(ast)
    analyser.analyse()

    interpreter = Interpreter(ast)
    try:
        output = interpreter.execute()
    except Exception as e:
        output = f"Error: {str(e)}"

    return jsonify({'output': output})


@app.route('/load_example/<filename>', methods=['GET'])
def load_example(filename):
    try:
        return send_from_directory(SAMPLE_DIR, filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


if __name__ == '__main__':
    app.run(debug=True)
