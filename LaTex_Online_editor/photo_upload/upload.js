document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('photoInput');
    formData.append('photo', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:4000/upload', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            // Display the uploaded photo
            const photoPath = result.photo_path;
            const photoElement = document.getElementById('uploadedPhoto');
            photoElement.src = `http://127.0.0.1:4000${photoPath}`;
            photoElement.style.display = 'block';

            // Display the .zip file link
            const zipFilePath = result.zip_file_path;
            const zipLinkElement = document.getElementById('zipFileLink');
            zipLinkElement.href = `http://127.0.0.1:4000${zipFilePath}`;
            zipLinkElement.textContent = 'Download .zip file';
            zipLinkElement.style.display = 'block';
        } else {
            console.error(result.error);
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error uploading file:', error);
        alert('Error uploading file');
    }
});