// src/App.jsx
import React, { useState, useRef } from 'react';
import './App.css';
import VoiceRecorder from './components/VoiceRecorder'


const App = () => {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState('');
  const [toDisplay, setToDisplay] = useState();
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const audioStreamRef = useRef(null);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioStreamRef.current = stream;
    mediaRecorderRef.current = new MediaRecorder(stream);
    mediaRecorderRef.current.ondataavailable = (event) => {
      chunksRef.current.push(event.data);
    };
    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
      const url = URL.createObjectURL(blob);
      setAudioURL(url);
      chunksRef.current = [];
      // Stop all tracks to release the microphone
      audioStreamRef.current.getTracks().forEach((track) => track.stop());
    };
    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };


  return (
    <section className="voice-recorder">
      <div className="site-logo">RateMySpeech</div>
      <div className="recorder-container">
        <VoiceRecorder />
      </div>
      <div className="chatbox-container">
        <p>{toDisplay ? toDisplay["result"] : "Chat messages here..."}</p>
      </div>
      <div className="playback-container">
        {audioURL && <audio controls src={audioURL} />}
      </div>
    </section>
  );  
};

export default App;
