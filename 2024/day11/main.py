from time import time

import aoc_helper

# DEBUG = True
DEBUG = False

starting_stones = [int(stone) for stone in input_reader.ged_data(DEBUG)[0].split(" ")]

lookup_table = {}
stones = []

for stone in starting_stones:
    stones += [(stone, 1)]

print(starting_stones)
print(stones)

def compile_stone_blink(_stone: int) -> [int]:
    if _stone == 0:
        return [1]
    if len(str(_stone)) % 2 == 0:
        stone_str = str(_stone)
        left_stone = stone_str[:int(len(stone_str) / 2)]
        right_stone = stone_str[int(len(stone_str) / 2):]
        return [int(left_stone), int(right_stone)]
    return [_stone * 2024]

def mutate_stone(_stone):
    _result_stones = []
    if _stone[0] not in lookup_table:
        lookup_table[_stone[0]] = compile_stone_blink(_stone[0])

    for result in lookup_table[_stone[0]]:
        _result_stones += ((result, _stone[1]),)

    return _result_stones

def consolidate_stones(_stones):
    _consolidated_stones = {}
    for _stone in _stones:
        if _stone[0] in _consolidated_stones:
            _consolidated_stones[_stone[0]] += _stone[1]
        else:
            _consolidated_stones[_stone[0]] = _stone[1]
    return [(key, value) for key, value in _consolidated_stones.items()]

def count_stones(_stones):
    total = 0
    for _stone in _stones:
        total += _stone[1]
    return total

if __name__ == "__main__":
    blinks = 75

    time_start = time()
    for i in range(blinks):
        print(f"Blink {i}")
        new_stones = []
        for stone in stones:
            new_stones += mutate_stone(stone)
        stones = consolidate_stones(new_stones)

    time_stop = time()
    run_time = time_stop - time_start
    print(input_reader.format_time(run_time))
    print(f"Total stones: {count_stones(stones)}")
