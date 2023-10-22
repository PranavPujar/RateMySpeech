async function uploadToGCP(signedUrl, file) {
    const response = await fetch(signedUrl, {
        method: 'PUT',
        body: file,
        headers: {
            'Content-Type': 'audio/wav'  // or whichever format you are using
        }
    });

    if (response.ok) {
        console.log('Audio uploaded successfully.');
    } else {
        console.error('Error uploading audio:', response.statusText);
    }
}
