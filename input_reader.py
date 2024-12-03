def ged_data(debug=False):
    input_file = "input_test.txt" if debug else "input.txt"
    input_lines = []
    with open(input_file, 'r') as f:
        while line := f.readline():
            input_lines.append(line)

    return input_lines