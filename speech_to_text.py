import openai
import whisper

# Transcribe data from user input audio
model = whisper.load_model("base.en")

user_input_audio_file = 'recording.mp3'

result = model.transcribe(user_input_audio_file, fp16=False)

input_words = result["text"]

# Retrieve the gpt-3.5-turbo finetuned llm 
openai.FineTuningJob.retrieve("ftjob-Bjca3SCCckSqKuOsXDMqWQdy")

response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo-0613:personal::8CTSBp6M",
    messages=[
      {"role": "user", "content": "With the answer format `score_out_of_10 | positives: [positive judgements] | negatives: [negative judgements]` please judge the conceptual solution given below for leetcode number 1 based on criteria that a real world technical interviewer would use? Conceptual Solution: " + input_words}
    ]
)

# Print the generated completion
out_response = response.choices[0]['message']['content']

out_response = out_response.split('|')
print(input_words)
print(out_response)

