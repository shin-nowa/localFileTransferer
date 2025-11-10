const fileInput = document.getElementById('file-input');
const fileNameSpan = document.getElementById('file-name');

fileInput.addEventListener('change', function() {
  if (fileInput.files.length > 0) {
    fileNameSpan.textContent = fileInput.files[0].name;
  } else {
    fileNameSpan.textContent = 'Arquivo não selecionado';
  }
});