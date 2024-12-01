import re
import numpy as np

DEBUG = True
# DEBUG = False

# Load test data or task data, depending on the debug variable
if DEBUG:
    input_values = []
    with open("input_test.txt", 'r') as f:
        while line :=  f.readline():
            input_values.append(re.search(r"(\d+)\s+(\d+)", line).groups())
else:
    input_values = []
    with open("input.txt", 'r') as f:
        while line :=  f.readline():
            input_values.append(re.search(r"(\d+)\s+(\d+)", line).groups())

# Transpose for easier sorting
input_transposed = np.transpose(input_values)

# Sort and cast to int
input_sorted = [sorted(row.astype('int')) for row in input_transposed]

# Calculate sum
total = sum([abs(a - b) for a, b in zip(input_sorted[0], input_sorted[1])])
print(f"Total distance is: {total}")

# Create and fill dictionary
counts = {}
for value in input_sorted[1]:
    if value in counts:
        counts[value] += 1
    else:
        counts[value] = 1

# Calculate similarity score
similarity_score = 0
for value in input_sorted[0]:
    # .get(value, 0) returns 0 if key does not exist
    similarity_score += value * counts.get(value, 0)
print(f"Similarity score is: {similarity_score}")
