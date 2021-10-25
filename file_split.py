def split_file(original_filename, file1, file2, line_to_split):

    with open(original_filename, 'r') as original, open(file1, 'w') as first, open(file2, 'w') as second:

        original_lines = original.readlines()

        first_file_lines, second_file_lines = original_lines[:line_to_split], original_lines[line_to_split:]

        print('First file lines: {}'.format(len(first_file_lines)))
        print('Second file lines: {}'.format(len(second_file_lines)))

        # Write the first file
        for line in first_file_lines:
            first.write(line)

        # Write the second file
        for line in second_file_lines:
            second.write(line)


original_filename = 'zli_title.txt'
file1 = 'tox_to_nontox_title_field.txt'
file2 = 'nontox_to_tox_title_field.txt'
line_to_split = 516

split_file(original_filename, file1, file2, line_to_split)