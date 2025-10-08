const form = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const fileList = document.getElementById("file-list");
const statusMessage = document.getElementById("upload-status");
const currentPath = fileList.dataset.currentPath;
const fileNameSpan = document.getElementById('file-name');

form.addEventListener("submit", function (event) {
  event.preventDefault();

  statusMessage.textContent = "Enviando arquivo...";

  const formData = new FormData(form);

  fetch(form.action, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        statusMessage.textContent = `Arquivo "${data.filename}" enviado com sucesso!`;

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
        statusMessage.textContent = `Erro: ${data.error}`;
      }
    })
    .catch((error) => {
      console.error("Erro:", error);
      statusMessage.textContent = "Ocorreu um erro de rede. Tente novamente.";
    });
});


// file name

fileInput.addEventListener('change', function() {
  if (fileInput.files.length > 0) {
    fileNameSpan.textContent = fileInput.files[0].name;
  } else {
    fileNameSpan.textContent = 'No file selected';
  }
});