import openai
import uvicorn
import whisper
from fastapi import FastAPI, HTTPException, Query, UploadFile
from starlette.middleware.cors import CORSMiddleware

# Creating the FastAPI object to use for calls
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods
    allow_headers=["*"],  # You can specify specific headers
)

PORT_NUMBER = 8000

openai.api_key = "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"

@app.get('/evaluate')
async def evaluate(file_name, leetcode_num = None):
    
    # if not file_name.endswith(('.wav', '.mp3', '.ogg', '.m4a')):
    #     raise HTTPException(status_code=400, detail="Only wav, mp3, m4a, and ogg files are supported. Your file name is " + file_name)
    model = whisper.load_model("base.en")

    # Retrieve the gpt-3.5-turbo finetuned llm 
    openai.FineTuningJob.retrieve("ftjob-Bjca3SCCckSqKuOsXDMqWQdy")
    
    file_path = '../' + file_name
    
    result = model.transcribe(file_path, fp16=False)
    input_words = result["text"] #this needs to have leetcode number

    if leetcode_num: 
        input_words = f"For the leetcode number {leetcode_num} {input_words}"

    response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo-0613:personal::8CTSBp6M",
    messages=[
    {"role": "user", "content": "With the answer format `score_out_of_10 (integer form) | positives: [positive judgements] | negatives: [negative judgements]` please judge the conceptual solution given below for this leetcode question based on criteria that a real world technical interviewer would use? Conceptual Solution: " + input_words}
    ])
    
    # Get the generated completion
    out_response = response.choices[0]['message']['content']
    out_response = out_response.split('|')

    return {"result": out_response,
            "file_name": file_name}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=PORT_NUMBER)