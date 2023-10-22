import uploadToGCP from './gcpUploadHandler';

export async function startRecording(setRecorderState) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    setRecorderState((prevState) => {
      return {
        ...prevState,
        initRecording: true,
        mediaStream: stream,
      };
    });
  } catch (err) {
    console.log(err);
  }
}

export async function saveRecording(recorder) {
  if (recorder.state !== "inactive") {
    // Add an event listener to the recorder to handle data available after stopping.
    recorder.ondataavailable = async event => {
      const audioBlob = event.data;

      // Get the signed URL from your server (assuming you've set up an endpoint for this).
      const signedUrlResponse = await fetch('YOUR_BACKEND_ENDPOINT_TO_GET_SIGNED_URL');
      if (!signedUrlResponse.ok) {
        console.error('Error getting signed URL.');
        return;
      }
      const { signedUrl } = await signedUrlResponse.json();

      // Upload the audio blob to GCP using the signed URL.
      await uploadToGCP(signedUrl, audioBlob);
    };

    // Stop the recording. This will trigger the 'ondataavailable' event.
    recorder.stop();
  }
}
