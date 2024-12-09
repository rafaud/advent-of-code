from collections import defaultdict

class BlockMap:
    def __init__(self):
        self.blocks = {}

    def add_block(self, file_id: int = -1):
        self.blocks[self.size] = file_id

    def get_first_free_block_index(self):
        for index in range(len(self.blocks)):
            if self.blocks[index] == -1:
                return index

    def get_last_file_index(self):
        for index in range(len(self.blocks)-1, -1, -1):
            if self.blocks[index] != -1:
                return index

    def swap_blocks(self, first_index: int, second_index: int):
        self.blocks[first_index], self.blocks[second_index] = self.blocks[second_index], self.blocks[first_index]

    def get_file_slice(self, file_id: int):
        slice_size = 0
        file_index = -1
        for index in range(len(self.blocks)):
            if self.blocks[index] == file_id:
                slice_size += 1
                if file_index == -1:
                    file_index = index
        return {"size": slice_size,
                "file_id": file_id,
                "index": file_index}

    def get_free_slices(self):
        free_slices = defaultdict(int)
        new_block = True
        free_slice_id = 0
        for index in range(len(self.blocks)):
            block = self.blocks[index]
            if block == -1:
                if new_block:
                    free_slice_id = index
                    new_block = False
                free_slices[free_slice_id] += 1
            else:
                new_block = True
        return free_slices

    def move_file_slice(self, file_slice, destination):
        for i in range(file_slice["size"]):
            self.swap_blocks(file_slice["index"] + i, destination + i)


    @property
    def check_sum(self):
        check_sum = 0
        for index in range(len(self.blocks)):
            file_id = self.blocks[index]
            if file_id != -1:
                value = file_id * index
                check_sum += value
        return check_sum

    @property
    def size(self):
        return len(self.blocks)

    @property
    def last_file_id(self):
        for index in range(len(self.blocks)-1, -1, -1):
            if self.blocks[index] != -1:
                return self.blocks[index]


    def __str__(self):
        _tmp = ""
        for block in self.blocks.values():
            if block == -1:
                _tmp += "."
            else:
                _tmp += str(block)
        return  _tmp