import openai
import whisper

import os
import time

# Transcribe data from user input audio
model = whisper.load_model("base.en")

# Retrieve the gpt-3.5-turbo finetuned llm 
openai.FineTuningJob.retrieve("ftjob-Bjca3SCCckSqKuOsXDMqWQdy")

# Directory to monitor
download_folder = 'downloads' #change of chrisians system

# Initialize a set to store the previous list of files
previous_files = set()
previous_files += os.listdir(download_folder)

#always scanning downloads folder
while True:
    # Get the current list of files in the folder
    current_files = set(os.listdir(download_folder))

    # Find the new files
    new_files = current_files - previous_files

    if new_files:
        for new_file in new_files:
        
            user_input_audio_file = new_files
        
            # print(f"New audio file detected: {new_file}")
        
            result = model.transcribe(user_input_audio_file, fp16=False)
            input_words = result["text"] #this needs to have leetcode number
        
            response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::8CTSBp6M",
            messages=[
            {"role": "user", "content": "With the answer format `score_out_of_10 | positives: [positive judgements] | negatives: [negative judgements]` please judge the conceptual solution given below for this leetcode question based on criteria that a real world technical interviewer would use? Conceptual Solution: " + input_words}
            ])

            # Get the generated completion
            out_response = response.choices[0]['message']['content']
            out_response = out_response.split('|')
            #SEND TO FRONTEND
            
    # Update the previous file list
    previous_files = current_files

    # Sleep for a specified interval (e.g., 10 seconds) before checking again
    time.sleep(10)





