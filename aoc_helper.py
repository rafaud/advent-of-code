from math import floor


def ged_data(debug=False):
    input_file = "input_test.txt" if debug else "input.txt"
    input_lines = []
    with open(input_file, 'r') as f:
        while line := f.readline():
            input_lines.append(line)

    return input_lines

def format_time(time):
    time_min = int(floor(time / 60))
    time_s = int(floor(time - time_min * 60))
    time_ms = int(floor((time - time_min * 60 - time_s) * 1000))

    return f"Run time: {time_min}min {time_s}s {time_ms}ms"