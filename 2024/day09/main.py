import copy
import re

import aoc_helper
from BlockMap import BlockMap

# DEBUG = True
DEBUG = False
DE_FRAG_V1 = True
DE_FRAG_V2 = True

disk_map = aoc_helper.get_data(DEBUG)[0]
# input_data = [[value for value in line.strip()] for line in input_data]

original_block_map = BlockMap()
is_file = True
file_id = 0
block = 0
for value in disk_map:
    if is_file:
        for _ in range(int(value)):
            original_block_map.add_block(file_id)
        file_id += 1
        is_file = False
    else:
        for _ in range(int(value)):
            original_block_map.add_block()
        is_file = True

print(f"Disk map:                  {disk_map}")
print(f"Original block map:        {original_block_map}")
with open("output_original.txt", "w") as f:
    f.write(str(disk_map))

if DE_FRAG_V1:
    de_fragmented_block_map_v1 = copy.deepcopy(original_block_map)

    free_block_index = de_fragmented_block_map_v1.get_first_free_block_index()
    file_block_index = de_fragmented_block_map_v1.get_last_file_index()

    while free_block_index < file_block_index:
        de_fragmented_block_map_v1.swap_blocks(free_block_index, file_block_index)
        free_block_index = de_fragmented_block_map_v1.get_first_free_block_index()
        file_block_index = de_fragmented_block_map_v1.get_last_file_index()

    print(f"De-fragmented disk map v1: {de_fragmented_block_map_v1}")
    print(f"De-fragmented disk map v1 check-sum: {de_fragmented_block_map_v1.check_sum}")
    with open("output_v1.txt", "w") as f:
        f.write(str(de_fragmented_block_map_v1))

if DE_FRAG_V2:
    de_fragmented_block_map_v2 = copy.deepcopy(original_block_map)

    file_id = de_fragmented_block_map_v2.last_file_id
    file_slice = de_fragmented_block_map_v2.get_file_slice(file_id)
    free_slices = de_fragmented_block_map_v2.get_free_slices()

    while next(iter(free_slices)) < file_slice["index"]:
        for index, size in free_slices.items():
            if index > file_slice["index"]:
                break
            if size >= file_slice["size"]:
                de_fragmented_block_map_v2.move_file_slice(file_slice, index)
                break
        file_id -= 1
        file_slice = de_fragmented_block_map_v2.get_file_slice(file_id)
        free_slices = de_fragmented_block_map_v2.get_free_slices()

    print(f"De-fragmented disk map v2: {de_fragmented_block_map_v2}")
    print(f"De-fragmented disk map v2 check-sum: {de_fragmented_block_map_v2.check_sum}")
    with open("output_v2.txt", "w") as f:
        f.write(str(de_fragmented_block_map_v2))
