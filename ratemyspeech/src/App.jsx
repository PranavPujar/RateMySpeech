import RecorderControls from "./components/recorder-controls";
import RecordingsList from "./components/recordings-list";
import useRecorder from "./hooks/useRecorder";
import "./app.css";

export default function App() {
  const { recorderState, ...handlers } = useRecorder();
  const { audio } = recorderState;

  return (
    <section className="voice-recorder">
      <div className="site-logo">RateMySpeech</div>
      <div className="recorder-container">
        <RecorderControls recorderState={recorderState} handlers={handlers} />
        <RecordingsList audio={audio} />
      </div>
      <div className="chatbox-container">
        {/* Your chatbox contents go here */}
        <p>Chat messages here...</p>
      </div>
    </section>
  );
}

