from openai import OpenAI
import whisper
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from io import BytesIO
from os import getenv
import tempfile
from pydantic import BaseModel


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # change the origin address when deploying
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  
    allow_headers=["*"],  
)

PORT_NUMBER = 8000

# Accessible through OpenAI acc
client = OpenAI(api_key=getenv('OPENAI_API_KEY_personal'))

app = FastAPI()


# Transcribe input audio file to text and return
@app.post("/audio")
async def process_audio(file: UploadFile = File(...)):

    # Using the base model for high speed transcription
    model = whisper.load_model("base.en")
    try:
        audio_data = await file.read()
    
        input_words = ''
        with tempfile.NamedTemporaryFile(suffix='.mp3') as audioFile:
            audioFile.write(audio_data)
            result = model.transcribe(audioFile.name, fp16=False)
            input_words = result["text"]
        
        # print(input_words)

        return JSONResponse(
            status_code=200,
            content={"transcription": input_words},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000" # change origin
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000" # change origin
            }
        )


class TranscriptionRequest(BaseModel):
    transcription: str


# Handling OPTIONS requesrt from website to show allowed headers and origins
@app.options('/evaluate')
async def show_methods():
    return JSONResponse(
        status_code=200,
        content={'message':'Options request successfully handled'},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000", # change origin
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )
    

@app.post('/evaluate')
async def evaluate(ft_output: TranscriptionRequest):

    # print(ft_output.transcription)

    try:
        # Retrieve the gpt-3.5-turbo finetuned llm 

        # openai.FineTuningJob.retrieve("ftjob-7MeRmaRQoCcXUzcNhw7UdGUS")

        # Rertrive fine-tuned model response 
        response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal:final-rms:9XxeZoxm",
        messages= [{"role": "system", "content": "You are RMS, a technical interviewer that rates the technical interview performance of its clients with the answer format `positives: [positive_judgements] | negatives: [negative_judgements] | score_out_of_10` where score_out_of_10 is a decimal, positive_judgements and negative_judgements are strings of positive and negative feedback of the interview performance. analyze the interview performance based on the following, keeping in mind the weights of each parameter:\nUser response is a valid approach to solve the problem - 2\nUser response is the most optimal approach to solve the problem - 2\nConciseness - 2\nMentioning Time Complexity - 1\nMentioning Space Complexity - 1\nFiller words (such as um, uh, etc) avoided - 1\nUser response mentions edge cases - 1.\nProvide your positive and negative judgements in a conversational manner."},{"role": "user", "content": f"{ft_output.transcription}"}])
        
        response = response.choices[0].message.content
        response = response.split('|')

        # If input audio is indeed an attempt to solve a technical problem 
        if len(response) == 3:
            positives = response[0][response[0].index('[')+1:-2]
            negatives = response[1][response[1].index('[')+1:-2]
            score = int(response[2].split(':')[-1].strip())

            response = f"Positives: {positives}\nNegatives: {negatives}\nscore: {score}"

            print(response)
            return JSONResponse(
                status_code=200,
                content={"response": response},
                headers={
                    "Access-Control-Allow-Origin": "http://localhost:3000"
                }
            )

        
        # Sometimes, the input might not be a genuine technical problem solution. If not, then the response will not have thes expected positives, negatives and score
        print(response)
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

    uvicorn.run(app, host="localhost", port=PORT_NUMBER) # change uvicorn server port