import sys

input = sys.argv[1]

bad_tokens = [
    'george',
    'joe',
    'frank',
    'john',
    'david',
    'michael',
    'peter',
    'ah',
    'ok',
    'eh',
    'dr',
    'oh',
    'hey'
    'the'
    'ah',
    's',
    'uh'
]

with open(input, 'r') as file:
    lines = file.readlines()

with open(input, 'w') as file:
    for line in lines:
        word = line.split()[0]

        if word in bad_tokens:
            continue
        elif not word.isalpha():
            continue
        else:
            file.write(line)
