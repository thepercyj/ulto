// Initialize CodeMirror editor
var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    mode: 'python',
    lineNumbers: true,
    theme: 'default'
});

// Example codes
const exampleCodes = {
    example1: `print('Hello, World!')`,
    example2: `for i in range(5):\n    print('This is loop iteration', i)`,
    example3: `x = 10\nif x > 5:\n    print('x is greater than 5')\nelse:\n    print('x is not greater than 5')`
};

// Function to load example code into the editor
 function loadExampleCode(filename) {
        fetch('/load_example/' + filename)
            .then(response => response.text())
            .then(data => {
                editor.setValue(data);
            })
            .catch(error => {
                console.error('Error loading example:', error);
                alert('Could not load example code.');
            });
    }

function runCode() {
    const code = editor.getValue();
    fetch('/run', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.output;
    })
    .catch(error => {
        document.getElementById('output').innerText = 'Error: ' + error.message;
    });
}

function clearCode() {
    editor.setValue('');
}