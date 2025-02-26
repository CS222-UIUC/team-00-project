const fileInput = document.getElementById("fileInput");
const latexOutput = document.getElementById("latexOutput");

fileInput.addEventListener("change", handleFileInput);

function handleFileInput(event) {
  const file = event.target.files[0];
  if (file) {
    processImage(file);
  }
}

function processImage(file) {
  latexOutput.value = "just for testing";
}
