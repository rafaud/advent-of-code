import curses
import heapq
import os
from time import sleep

import numpy as np

def map_for_bytes(_bytes_count: int, _bytes_list: [(int, int)]) -> np.ndarray:
    plan = np.full((h, w), ".")
    for i, coord in enumerate(bytes_list):
        if i == bytes_count: break
        plan[*coord] = "#"
    return plan

def find_path( _plan: np.ndarray, _start: (int, int), _stop:(int, int)):
    _directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    _h, _w = _plan.shape

    _queue = [(0, _start)]
    _distances = {_start: 0}

    _predecessors = {}

    while _queue:
        _cost, _current_position = heapq.heappop(_queue)
        _y, _x = _current_position
        if _current_position == _stop:
            _path = []
            while _current_position is not None:
                _path.append(_current_position)
                _current_position = _predecessors.get(_current_position, None)
            return _cost, _path[::-1]

            # return result

        for _dy, _dx in _directions:
            _ny, _nx = _y + _dy, _x + _dx

            if 0 <= _ny < _h and 0 <= _nx < _w and _plan[_ny, _nx] == ".":
                _new_cost = _cost + 1
                _neighbour = (_ny, _nx)
                if _neighbour not in _distances or _new_cost < _distances[_neighbour]:
                    _distances[_neighbour] = _new_cost
                    _predecessors[_neighbour] = _current_position
                    heapq.heappush(_queue, (_new_cost, _neighbour))
    return -1, -1

def run(stdscr):
    global bytes_count
    # Clear screen
    stdscr.clear()
    # Corrupted tile
    curses.init_pair(1, curses.COLOR_WHITE, 125)

    # Path tile
    curses.init_pair(2, 155, 155)

    # Background tile
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)

    # Last tile
    curses.init_pair(4, curses.COLOR_WHITE, 201)


    _is_path_possible = 1

    while _is_path_possible != -1:
        stdscr.erase()
        bytes_count += 1
        _plan = map_for_bytes(bytes_count, bytes_list)
        _is_path_possible, _new_path = find_path(_plan, start, stop)
        if _new_path != -1: _path = _new_path
        for row, line in enumerate(_plan):
            for col, tile in enumerate(line):
                stdscr.addstr(row, col*2, tile*2, curses.color_pair(1 if tile == "#" else 3))
        for row, col in _path:
                stdscr.addstr(row, col*2, "o"*2, curses.color_pair(2))
        if _new_path == -1:
            last_row, last_col = bytes_list[bytes_count -1]
            stdscr.addstr(last_row, last_col*2, "X"*2, curses.color_pair(4))
        stdscr.addstr(h + 1, 0, f"Byte: {bytes_count}, position: {bytes_list[bytes_count -1]}\n")
        stdscr.refresh()
        sleep(0.002)


    stdscr.addstr(f"Path not found", curses.color_pair(1))
    stdscr.getkey()


if __name__ == "__main__":

    # w, h = 7, 7
    w, h = 71, 71
    start = (0, 0)
    stop = (w - 1, h - 1)
    bytes_count = 0

    with open("input.txt") as f:
        lines = [line.split(",") for line in f.readlines()]

    bytes_list = [(int(y), int(x)) for x, y in lines]

    step_count = 0

    if "TERM_PROGRAM" in os.environ:
        curses.wrapper(run)
    else:
        is_path_possible = 1

        while is_path_possible != -1:
            bytes_count += 1
            plan = map_for_bytes(bytes_count, bytes_list)
            is_path_possible, _ = find_path(plan, start, stop)
            print("Bytes count: ", bytes_count)
            print("Is path possible: ", is_path_possible, "\n")

        print(bytes_list[bytes_count - 1])

    plan = map_for_bytes(bytes_count, bytes_list)
    step_count = find_path(plan, start, stop)
    print("[Part I] Step count: ", step_count)


