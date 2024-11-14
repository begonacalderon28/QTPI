// URL del documento codificado
const encodedUrl = '/Expedientes/showExternalDocument.do?document=p8%3A%2F%2F%7BE02285E4-DF28-41E2-B590-FC8D9046CA63%7D&idEntidad=59593558';

// Descodificar la parte de la URL que contiene el documento
const decodedUrl = decodeURIComponent(encodedUrl);

// Realizar la descarga del PDF
fetch(decodedUrl, {
    method: 'GET',
    credentials: 'include',
})
.then(response => {
    if (!response.ok) {
        throw new Error('Error al descargar el archivo: ' + response.statusText);
    }
    return response.blob();
})
.then(blob => {
    const downloadLink = document.createElement('a');
    const url = window.URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = 'documento.pdf';  // Puedes cambiar el nombre aquí
    document.body.appendChild(downloadLink);
    downloadLink.click();
    setTimeout(() => {
        window.URL.revokeObjectURL(url);
    }, 100);
})
.catch(err => console.error('Error:', err));
