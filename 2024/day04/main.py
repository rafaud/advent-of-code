import aoc_helper
import numpy as np

# DEBUG = True
DEBUG = False

input_data = aoc_helper.ged_data(DEBUG)

# remove new lines
matrix = [line.strip() for line in input_data]

# split letters
matrix = [[letter for letter in line] for line in matrix]
matrix = np.array(matrix)


def check_vector(vector, searched_word):
    vector_total = 0
    for i in range(len(vector) - len(searched_word) + 1):
        word = vector[i:i + len(searched_word)]
        word = "".join(word)
        if word in searched_word: vector_total += 1

        word = vector[-1-i:-1-i-len(searched_word):-1]
        word = "".join(word)
        if word in searched_word: vector_total += 1

    return vector_total

SEARCHED_WORD = "XMAS"
total = 0
part_total = 0

# Check Rows
for row in matrix:
    total_tmp = check_vector(row, SEARCHED_WORD)
    part_total += total_tmp

total += part_total
part_total = 0

#Check Columns
for column in matrix.transpose():
    total_tmp = check_vector(column, SEARCHED_WORD)
    part_total += total_tmp

total += part_total
part_total = 0

# check diagonals
for i in range(len(matrix)):
    total_tmp = check_vector(matrix.diagonal(offset=i), SEARCHED_WORD)
    part_total += total_tmp
    if i == 0: continue
    total_tmp = check_vector(matrix.diagonal(offset=-i), SEARCHED_WORD)
    part_total += total_tmp

total += part_total
part_total = 0

# check anti diagonals
for i in range(len(matrix)):
    flipped = np.fliplr(matrix)
    total_tmp = check_vector(flipped.diagonal(offset=i), SEARCHED_WORD)
    part_total += total_tmp
    if i == 0: continue
    total_tmp = check_vector(flipped.diagonal(offset=-i), SEARCHED_WORD)
    part_total += total_tmp

total += part_total
part_total = 0

print(f"Total \'xmas\' in the matrix: {total}")

def check_slice(_slice) -> bool:
    if (_slice[0, 0] == "M" and
            _slice[0, 2] == "S" and
            _slice[1, 1] == "A" and
            _slice[2, 0] == "M" and
            _slice[2, 2] == "S"):
        return True
    else:
        return False

total = 0
for row in range(len(matrix)):
    for col in range(len(matrix[row])):
        slice = matrix[row:row+3, col:col+3]
        if slice.size == 9:
            if check_slice(slice): total += 1
            if check_slice(np.rot90(slice)): total += 1
            if check_slice(np.rot90(slice, k=2)): total += 1
            if check_slice(np.rot90(slice, k=3)): total += 1


print(f"Total x-\'mas\' in the matrix: {total}")
