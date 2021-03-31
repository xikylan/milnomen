import csv

with open('es.tsv', 'r') as file:
    tsv = csv.reader(file, delimiter="\t")

    max = 5
    for i in range(0, 10):
        file.seek(0)
        count = 0
        print()
        for line in tsv:
            if count >= max:
                break
            print(line[1])
            count += 1
