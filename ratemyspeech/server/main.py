import openai
import whisper
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from io import BytesIO
import tempfile
from pydantic import BaseModel

# Creating the FastAPI object to use for calls
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # You can specify specific HTTP methods
    allow_headers=["*"],  # You can specify specific headers
)

PORT_NUMBER = 8000

openai.api_key = "sk-proj-yKongnqBqZGAXeUfQsc4T3BlbkFJ9RVnpIyCg7RfJ7Atzigq"


app = FastAPI()


@app.post("/audio")
async def process_audio(file: UploadFile = File(...)):

    model = whisper.load_model("base.en")
    try:
        audio_data = await file.read()
        
        # Convert audio data to AudioSegment
        # audio = AudioSegment.from_file(BytesIO(audio_data))

        input_words = ''
        with tempfile.NamedTemporaryFile(suffix='.mp3') as audioFile:
            audioFile.write(audio_data)
            result = model.transcribe(audioFile.name, fp16=False)
            input_words = result["text"]
        
        print(input_words)

        return JSONResponse(
            status_code=200,
            content={"transcription": input_words},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000"
            }
        )

    
class TranscriptionRequest(BaseModel):
    transcription: str


@app.options('/evaluate')
async def show_methods():
    return JSONResponse(
        status_code=200,
        content={'message':'Options request successfully handled'},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )
    

@app.post('/evaluate')
async def evaluate(ft_output: TranscriptionRequest):

    # Retrieve the gpt-3.5-turbo finetuned llm 
    print(ft_output.transcription)

    try:
        openai.FineTuningJob.retrieve("ftjob-7MeRmaRQoCcXUzcNhw7UdGUS")

        # generate a name for the stream of data sent to backend and save that file
        response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::8CTSBp6M",
        messages= [{"role": "system", "content": "You are RMS, a technical interviewer that rates the technical interview performance of its clients with the answer format `positives: [positive_judgements] | negatives: [negative_judgements] | score_out_of_10` where score_out_of_10 is a decimal, positive_judgements and negative_judgements are strings of positive and negative feedback of the interview performance. analyze the interview performance based on the following, keeping in mind the weights of each parameter:\nUser response is a valid approach to solve the problem - 2\nUser response is the most optimal approach to solve the problem - 2\nConciseness - 2\nMentioning Time Complexity - 1\nMentioning Space Complexity - 1\nFiller words (such as um, uh, etc) avoided - 1\nUser response mentions edge cases - 1.\nProvide your positive and negative judgements in a conversational manner."},{"role": "user", "content": f"{ft_output.transcription}"}])
        
        response = response.choices[0]['message']['content']
        response = response.split('|')

        print(response)
        # positives = response[0][response[0].index('[')+1:-2]
        # negatives = response[1][response[1].index('[')+1:-2]
        # score = int(response[2].split(':')[-1].strip())

        # print(f"Positives: {positives}\nNegatives: {negatives}\nscore: {score}")
        
        return JSONResponse(
            status_code=200,
            content={"response": response},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000"
            }
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=PORT_NUMBER)