var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    mode: 'python',
    lineNumbers: true,
    theme: 'default'
});

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