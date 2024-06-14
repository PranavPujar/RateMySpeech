// src/VoiceRecorder.jsx
import React, { useState, useRef } from 'react';
import './VoiceRecorder.css'; 

const VoiceRecorder = () => {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState('');
  const [generateable, setGenerateable] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const audioStreamRef = useRef(null);
  const audioBlobRef = useRef(null); //stores the  blob of audio for transmission

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    setGenerateable(false);
    audioStreamRef.current = stream;
    mediaRecorderRef.current = new MediaRecorder(stream);
    mediaRecorderRef.current.ondataavailable = (event) => {
      chunksRef.current.push(event.data);
    };
    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
      const url = URL.createObjectURL(blob);
      audioBlobRef.current = blob; // Store Blob in audioBlobRef
      setAudioURL(url);
      chunksRef.current = [];
      // Stop all tracks to release the microphone
      audioStreamRef.current.getTracks().forEach((track) => track.stop());
    };
    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const transmitAudioToBackend = async () => {
    if (audioBlobRef.current) {
      const formData = new FormData();
      formData.append("file", audioBlobRef.current, "recording.wav");

      try {

        const response = await fetch("http://localhost:8000/audio", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          console.log("Audio file successfully transmitted to the backend");
          const output = await response.json();
          return output; // Return the response JSON
        } else {
          console.error("Failed to transmit audio file");
        }
      } catch (error) {
        console.error("Error transmitting audio file", error);
      }
    } else {
      console.error("No audio to transmit");
    }
  };

  const extractGPTAnalysis = async (transcription) => {
    console.log(JSON.stringify({transcription}))
    try {
      const response = await fetch("http://localhost:8000/evaluate", {
        method: "POST", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({transcription}), 
      });
      
      const result = await response.json();
      console.log(result);

      // setToDisplay(result);
      
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
    setGenerateable(true);
  };


  const handleDoneClick = async () => {
    const response = await transmitAudioToBackend();
    await extractGPTAnalysis(response.transcription);
    
    setAudioURL('');
    setGenerateable(false);
  };


  return (
    <div className="text-holder">
      <h1>Audio Recorder</h1>
      <div className="button-container">
        <button 
          onClick={startRecording} 
          disabled={recording} 
          className="record-button" 
          type="button"
        >
          Record
        </button>
        <button 
          onClick={stopRecording} 
          disabled={!recording} 
          className="stop-button" 
          type="button"
        >
          &#x25A0; {/* Unicode for the stop icon */}
        </button>
      </div>
      {audioURL && <audio src={audioURL} controls />}
      {generateable && (
        <button onClick={handleDoneClick} className="done-button" type="button">
          Analyze Performance
        </button>
      )}
    </div>
  );
};

export default VoiceRecorder;
