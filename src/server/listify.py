import sys

max = 1050
count = 0

input = sys.argv[1]

with open(input, "r") as es:
    with open('top_1000.txt', 'w') as top:
        for line in es:
            if count >= max:
                break

            top.write(line)
            count += 1
