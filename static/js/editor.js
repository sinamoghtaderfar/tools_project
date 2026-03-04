document.getElementById('run-btn').addEventListener('click', () => {
    const code = document.getElementById('code-editor').value;
    const outputDiv = document.getElementById('output');
    
    outputDiv.textContent = "Running...";

    fetch("{% url 'editor:run_code' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        outputDiv.textContent = data.result;
    })
    .catch(err => {
        outputDiv.textContent = "Error: " + err;
    });
});