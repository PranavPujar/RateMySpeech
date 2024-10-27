import openai

openai.api_key = "sk-proj-yKongnqBqZGAXeUfQsc4T3BlbkFJ9RVnpIyCg7RfJ7Atzigq"

openai.FineTuningJob.retrieve("ftjob-7MeRmaRQoCcXUzcNhw7UdGUS")

input_words = "To solve LeetCode problem 33, \"Search in Rotated Sorted Array,\" use a modified binary search. Start with two pointers, left at index 0 and right at the last index. While left is less than or equal to right, calculate the mid index. If nums[mid] equals the target, return mid. If the left half from nums[left] to nums[mid] is sorted, check if the target lies within this range; if so, adjust right to mid - 1, otherwise set left to mid + 1. If the right half from nums[mid] to nums[right] is sorted, check if the target is in this range; if so, adjust left to mid + 1, otherwise set right to mid - 1. If the loop ends without finding the target, return -1. This method efficiently narrows down the search space by leveraging the sorted property of one half of the array in each step."

response = openai.ChatCompletion.create(
model="ft:gpt-3.5-turbo-0613:personal::8CTSBp6M",
messages= [{"role": "system", "content": "You are RMS, a technical interviewer that rates the technical interview performance of its clients with the answer format `positives: [positive_judgements] | negatives: [negative_judgements] | score_out_of_10` where score_out_of_10 is a decimal, positive_judgements and negative_judgements are strings of positive and negative feedback of the interview performance. analyze the interview performance based on the following, keeping in mind the weights of each parameter:\nUser response is a valid approach to solve the problem - 2\nUser response is the most optimal approach to solve the problem - 2\nConciseness - 2\nMentioning Time Complexity - 1\nMentioning Space Complexity - 1\nFiller words (such as um, uh, etc) avoided - 1\nUser response mentions edge cases - 1.\nProvide your positive and negative judgements in a conversational manner."},{"role": "user", "content": f"{input_words}"}])

# Get the generated completion
# print(response)
response = response.choices[0]['message']['content']
response = response.split('|')
['positives: [valid approach, optimal approach, concise, time complexity mentioned, space complexity mentioned, no filler words, mentions edge cases] ', ' negatives: [] ', ' score_out_of_10: 10']

positives = response[0]