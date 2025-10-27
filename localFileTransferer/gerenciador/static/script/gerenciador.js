const form = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const fileList = document.getElementById("file-list");
const statusMessage = document.getElementById("upload-status");
const fileNameSpan = document.getElementById('file-name');

// Só executa o código se os elementos do formulário existirem nesta página
if (form && fileInput && fileList && statusMessage && fileNameSpan) {
    
    const currentPath = fileList.dataset.currentPath;

    // --- Lógica de Upload (CSRF) ---
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Impede o envio normal do formulário

        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

        statusMessage.textContent = "Uploading file...";

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            // Adiciona uma verificação para erros HTTP (como 404, 500)
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            // Se o servidor retornar algo que não é JSON (como uma página de erro HTML),
            // isso também pode causar um erro que será pego pelo .catch()
            return response.json();
        })
        .then(data => {
            if (data.success) {
                statusMessage.textContent = `File "${data.filename}" uploaded successfully!`;

                const newLi = document.createElement("li");
                const newLink = document.createElement("a");

                newLink.className = "file";
                newLink.textContent = data.filename;

                newLink.href = `/download/file/${currentPath}${data.filename}`;

                newLi.appendChild(newLink);
                fileList.appendChild(newLi);

                const emptyMessage = document.getElementById("empty-folder-message");
                if (emptyMessage) {
                    emptyMessage.remove();
                }

                fileInput.value = "";
            } else {
                statusMessage.textContent = `Error: ${data.error}`;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            statusMessage.textContent = "A network error occurred. Please try again."; 
        });
    });

    // --- Lógica para mostrar o nome do arquivo ---
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            fileNameSpan.textContent = fileInput.files[0].name;
        } else {
            fileNameSpan.textContent = 'No file selected';
        }
    });

}