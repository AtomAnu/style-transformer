import csv
tsv_filename = 'data/tweet/nontox_zli_text.pos'

with open(tsv_filename, 'r') as text_file:
    text_file_lines = text_file.readlines()

tsv_file = open(tsv_filename)

read_tsv = csv.reader(tsv_file, delimiter="\t")

counter = 0
for row in read_tsv:
    # if row[0].strip() not in text_file_lines[counter].strip():
    #     print('Mismatch at line: {}'.format(counter))
    #     print('TSV sentence: {}'.format(row[0]))
    #     print('Original sentence: {}'.format(text_file_lines[counter]))

    if counter == 5432:
    # if counter == 0:
        print('TSV sentence: {}'.format(row))
        # print('Original sentence: {}'.format(text_file_lines[counter]))
    counter += 1

print(counter)