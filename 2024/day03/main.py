import aoc_helper
import re

# DEBUG = True
DEBUG = False

def process_part(part):
    # Calculates sum for a single part of a String, captures required part with regex,
    # extract numbers multiplies it and sums all of them
    return sum([
        int(a) * int(b)
        for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", part)
    ])

input_data = aoc_helper.get_data(DEBUG)
# Remove new lines
input_data = ["".join(input_data)]

total = 0
for line in input_data:
    total += process_part(line)
print(f"[T1] Total sum of all operation: {total}")

parts_to_be_executed = []
# Check every line
for line in input_data:
    # split it on do-s, for them to be executed
    do_splits = re.split(r"do\(\)", line)
    # check if split for don't-s, and remove everything after first don't
    for split in do_splits:
        final_dos = re.split(r"don't\(\)", split)
        parts_to_be_executed.append(final_dos[0])

total = 0
for part in parts_to_be_executed:
    total += process_part(part)
print(f"[T2] Total sum of all operation: {total}")

