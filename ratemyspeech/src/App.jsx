import { useState } from "react";
import "./app.css";
import RecorderControls from "./components/recorder-controls";
import RecordingsList from "./components/recordings-list";
import useRecorder from "./hooks/useRecorder";

export default function App() {
  const { recorderState, ...handlers } = useRecorder();
  const { audio } = recorderState;
  const [ toDisplay, setToDisplay ] = useState();


  const fetchThing = () => {
    // make call to fetch response
    const fetchData = async () => {
        console.log("File")
        try {
          const response = await fetch(`http://localhost:8000/evaluate?file_name=output.mp3`);
          console.log(response)
          const result = await response.json();
          console.log(result)
          setToDisplay(result)
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };
      fetchData();
  }

  return (
    <section className="voice-recorder">
      <div className="site-logo">RateMySpeech</div>
      <div className="recorder-container">
        <RecorderControls recorderState={recorderState} handlers={handlers} />
        <RecordingsList audio={audio} />
        <button onClick={fetchThing}>Done</button>
      </div>
      <div className="chatbox-container">
        <p>{toDisplay ? toDisplay["result"] : "Chat messages here..."}</p>
      </div>
    </section>
  );
}

