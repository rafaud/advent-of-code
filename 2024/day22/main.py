from collections import defaultdict
from functools import cache

with open("input.txt") as input_file:
    start_numbers = [int(foo) for foo in input_file.read().splitlines()]

@cache
def mix(number_1, number_2):
    return number_1 ^ number_2

@cache
def prune(number_1):
    return number_1 % 16777216 # 1 000 000 000 000 000 000 000 000 in binary

@cache
def step_1(number_1):
    result = number_1 * 64
    number_1 = mix(number_1, result)
    number_1 = prune(number_1)
    return number_1

@cache
def step_2(number_1):
    result = number_1 // 32
    number_1 = mix(number_1, result)
    number_1 = prune(number_1)
    return number_1

@cache
def step_3(number_1):
    result = number_1 * 2048
    number_1 = mix(number_1, result)
    number_1 = prune(number_1)
    return number_1

@cache
def get_new_number(number_1):
    number_1 = step_1(number_1)
    number_1 = step_2(number_1)
    number_1 = step_3(number_1)
    return number_1

def difference(number_1, number_2):
    return number_1 - number_2

secret_numbers = start_numbers
steps = 2000
prices = [[foo % 10 for foo in secret_numbers]]
price_changes = []
patterns = [{} for _ in range(len(start_numbers))]
for i in range(steps):
    print(f"Step {i+1} of {steps}")
    secret_numbers = list(map(get_new_number, secret_numbers))
    prices.append([foo % 10 for foo in secret_numbers])
    price_changes.append(list(map(difference, prices[-1], prices[-2])))
    if len(price_changes) >= 4:
        last_changes = price_changes[-4:]
        for j in range(len(start_numbers)):
            changes = "".join([str(sublist[j]) for sublist in last_changes])
            if changes not in patterns[j].keys():
                patterns[j][changes] = prices[-1][j]

gains = defaultdict(int)

for monkey in range(len(patterns)):
    for key, value in patterns[monkey].items():
        gains[key] += value

secret_numbers = list(secret_numbers)

print(f"Sum of all numbers after {steps} steps is {sum(secret_numbers)}")
print("Most bananas that can be gained:", max(gains.values()))