from collections import defaultdict

with open("input.txt") as f:
    codes = f.read().split("\n")
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
number_pad = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
    "X": (3, 0), "0": (3, 1), "A": (3, 2)
}

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

arrow_pad = {
    "X": (0, 0), "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2),
}

def find_all_paths(key_map):
    return_lut = {}
    invalid_key = key_map["X"]
    for key, (r1, c1) in key_map.items():
        for key2, (r2, c2) in key_map.items():
            if key == "X" or key2 == "X": continue
            path = '<' * (c1 - c2) +  'v' * (r2 - r1) + '^' * (r1 - r2) + '>' * (c2 - c1)
            if invalid_key == (r2, c1) or invalid_key == (r1, c2):
                path = path[::-1]
            return_lut[(key, key2)] = path
    return return_lut

def expand_path(from_key, to_key, lut) -> str:
    return lut[(from_key, to_key)]

def expand_chunk(_chunk, lut) -> [str]:
    return_path = defaultdict(int)
    prev = "A"
    for ch in _chunk:
        return_path[expand_path(prev, ch, lut) + "A"] += 1
        prev = ch
    return return_path

def calc_complex(_paths):
    lengths = []
    for key, value in _paths.items():
        length = 0
        for _key, _value in value.items():
            length += len(_key) * _value
        lengths.append(length * int(key[:-1]))
    return lengths

def print_paths(_paths):
    for key, value in _paths.items():
        print(f"{key}: {"".join(value)}")

number_pad_paths = find_all_paths(number_pad)
arrow_pad_paths = find_all_paths(arrow_pad)

paths = {}

for code in codes:
    paths[code] = expand_chunk(code, number_pad_paths)

depth = 26
for i in range(depth - 1):
    for key, value in paths.items():
        new_chunks = defaultdict(int)
        for chunk, number in value.items():
            tmp_chunks = expand_chunk(chunk, arrow_pad_paths)
            for tmp_key, tmp_value in tmp_chunks.items():
                new_chunks[tmp_key] += number * tmp_value
        paths[key] = new_chunks
print("Total complexity: ", sum(calc_complex(paths)))