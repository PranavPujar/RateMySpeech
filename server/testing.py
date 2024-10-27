response = ['positives: [valid approach, optimal approach, concise, time complexity mentioned, space complexity mentioned, no filler words, mentions edge cases] ', ' negatives: [] ', ' score_out_of_10: 10']

positives = response[0][response[0].index('[')+1:-2]

print(positives)

idx = response[1].index('[')
negatives = response[1][idx+1:-2]

print(len(negatives))

score = int(response[2].split(':')[-1].strip())
print(type(score), score)