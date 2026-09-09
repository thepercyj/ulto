from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from src.lexer import tokenize
from src.parser import Parser
from src.semantic_analyser import SemanticAnalyser
from src.interpreter import Interpreter

app = Flask(__name__)

# The codespace offers the same example programs the test suite uses, read from
# where they already live rather than from a second copy that could drift.
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests', 'examples', 'ulto')


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


@app.route('/docstrings/genindex')
def genindex():
    return render_template('html/genindex.html')


@app.route('/docstrings/search')
def search():
    return render_template('html/search.html')


@app.route('/docstrings/core')
def core():
    return render_template('html/core.html')


@app.route('/docstrings/lexer')
def lexer():
    return render_template('html/lexer.html')


@app.route('/docstrings/parser')
def parser():
    return render_template('html/parser.html')


@app.route('/docstrings/semantic_analyser')
def semantic_analyser():
    return render_template('html/semantic_analyser.html')


@app.route('/docstrings/interpreter')
def interpreter():
    return render_template('html/interpreter.html')


@app.route('/docstrings/lazyeval')
def lazyeval():
    return render_template('html/lazyeval.html')


@app.route('/docstrings/malloc')
def malloc():
    return render_template('html/malloc.html')


@app.route('/docstrings/logstack')
def logstack():
    return render_template('html/logstack.html')


@app.route('/docstrings/trace')
def trace():
    return render_template('html/trace.html')


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
        # Captured rather than printed: the browser needs the text back, and a
        # WSGI server has no console for it to go to.
        output = interpreter.execute(capture=True)
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
