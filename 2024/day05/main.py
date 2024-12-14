from collections import defaultdict
from math import floor

import aoc_helper
import re

# DEBUG = True
DEBUG = False

input_data = aoc_helper.get_data(DEBUG)

rules = defaultdict(list)
prints = []

for line in input_data:
    capture = re.findall(r"(\d+)", line)
    if "," in line:
        prints.append([int(i) for i in capture])

    if "|" in line:
        # key: a page
        # values:pages that can't appear before {key} page
        rules[int(capture[0])].append(int(capture[1]))

print(rules)
correct_prints = []
incorrect_prints = []

def check_pages(values):
    is_correct = True
    for i in range(1, len(values)):
        b_pages = values[0:i]
        for before_page in b_pages:
            if before_page in rules[values[i]]:
                print(f"{values}, breaks rule {values[i]}:{rules[values[i]]} at index {i}")
                is_correct = False
                break
    return is_correct

for pages in prints:
    if check_pages(pages):
        correct_prints.append(pages)
    else:
        incorrect_prints.append(pages)

print(f"Correct prints: {correct_prints}")
print(f"Incorrect prints: {incorrect_prints}")

total = 0
for correct_pages in correct_prints:
    total += correct_pages[floor(len(correct_pages) / 2)]

print(f"Sum of medians of correct prints: {total}")

for pages in incorrect_prints:
    for i in range(1, len(pages)):
        before_pages = pages[0:i]
        for j in range(len(before_pages)):
            if before_pages[j] in rules[pages[i]]:
                pages[i], pages[j] = pages[j], pages[i]

for pages in incorrect_prints:
    check_pages(pages)

total = 0
for correct_pages in incorrect_prints:
    total += correct_pages[floor(len(correct_pages) / 2)]

print(f"Sum of medians of sorted incorrect prints: {total}")