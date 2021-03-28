import csv

# Filter top 1000 words
count = 0
with open('es.txt', 'r') as file:
    with open('top_es.txt', 'w') as top:
        for line in file:
            if count >= 1000:
                break
            pair = line.split(' ')
            top.write(pair[0])
            top.write('\n')
            count += 1
