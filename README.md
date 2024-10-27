# RateMySpeech - AI Interview Assistant

## Overview

RateMySpeech is a powerful AI-driven tool designed to assist users in preparing for technical interviews. Leveraging advanced speech recognition technology and the OpenAI GPT model, this application provides real-time feedback on interview responses, helping users improve their performance through constructive critiques.

## Key Features

- **Audio Recording**: Users can easily record their responses during mock interviews using the built-in voice recorder.
- **Transcription**: The app transcribes recorded audio into text, enabling users to review their answers.
- **AI Feedback**: Utilizing a fine-tuned OpenAI model, the app analyzes the transcription and provides feedback on various aspects of the interview performance, including:
  - Technical accuracy
  - Clarity and conciseness
  - Time and space complexity considerations
  - Awareness of edge cases
  - Usage of filler words
- **User-Friendly Interface**: The application features an intuitive interface that guides users through the recording and feedback process seamlessly.

## How It Works

1. **Record Your Response**: Users can record their answers to technical questions.
2. **Transcription**: Once the recording is complete, the audio is sent to the server, where it is transcribed into text using the Whisper AI model.
3. **Feedback Analysis**: The transcribed text is analyzed by a fine-tuned OpenAI GPT model, which provides feedback structured in a clear format.
4. **Review Feedback**: Users receive detailed insights on their performance, including positives, negatives, and a score out of 10, enabling them to focus on areas for improvement.

## Getting Started

To get started with RateMySpeech:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd RateMySpeech
   ```

   _on one terminal_:

   ```bash
   cd server
   uvicorn main:app --reload
   ```

   _on another terminal terminal_:

   ```bash
   npm install
   npm start
   ```

2. **RMS is Deployed! Check the website:**
   `www.ratemyspeech.com`
