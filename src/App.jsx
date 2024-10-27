// src/App.jsx
import React, { useState } from 'react';
import './app.css';
import VoiceRecorder from './components/VoiceRecorder'

const App = () => {
  const [toDisplay, setToDisplay] = useState();

  const handleDisplayUpdate = (result) => {
    setToDisplay(result);
  };

  return (
    <section className="voice-recorder">
      <div className="site-logo">RateMySpeech</div>
      <div className="recorder-container">
        <VoiceRecorder onDisplayUpdate={handleDisplayUpdate} />
      </div>
      <div className="chatbox-container">
        <p>{toDisplay ? toDisplay["response"] : "Chat messages here..."}</p>
      </div>
    </section>
  );  
};

export default App;
