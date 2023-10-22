import openai

# Retrieve the state of a fine-tune
openai.FineTuningJob.retrieve("ftjob-Bjca3SCCckSqKuOsXDMqWQdy")

response = openai.ChatCompletion.create(
    model="ft:gpt-3.5-turbo-0613:personal::8CTSBp6M",
    messages=[
      {"role": "user", "content": "With the answer format `score_out_of_10 | positives: [positive judgements] | negatives: [negative judgements]` please judge the conceptual solution given below for leetcode number 1 based on criteria that a real world technical interviewer would use? Conceptual Solution: Leetcode problem 349, Intersection of Two Arrays. So, for this one, I believe we can find the intersection of two arrays. One way to do it is by using a hash set, right? We can add all elements of the first array to the set and then iterate through the second array, checking if each element exists in the set. You know, checking if each element exists. If it does, we add it to the result. The time complexity uhh should be Oh of m plus n, where m and n the lengths of the two arrays, and the space complexity is Oh of m or n, depending on which array we store in the set. Seems pretty straightforward to me."}
    ]
)

# Print the generated completion
out_response = response.choices[0]['message']['content']

out_response = out_response.split('|')
print(out_response)


# Define the prompt message
# prompt_message = (
#     "With the answer format `score_out_of_10 | positives: [positive judgements] | negatives: [negative judgements]` please judge the conceptual solution given below for leetcode number 1 based on criteria that a real world technical interviewer would use? Leetcode problem 20, Valid Parentheses. To validate parentheses, we can use a stack data structure. We iterate through the string and push opening parentheses onto the stack. When we encounter a closing parenthesis, we check if it matches the top of the stack. If they match, we pop the stack; otherwise, the string is invalid. This approach has a time complexity of O(n) as it makes a single pass through the string, and a space complexity of O(n) in the worst case for the stack."
# )

# Generate a completion using GPT-3.5
# response = openai.Completion.create(
#     engine="gpt-3.5-turbo-0613",  
#     prompt=prompt_message,
#     max_tokens=80,  # Adjust max tokens as needed
#     n = 1
# )
