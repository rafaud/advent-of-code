# Created by rafaud@icloud.com
# You’re given a grid representing rolls of paper (@) and empty space (.),
# and need to determine which rolls are accessible by forklifts.
# A roll is accessible if fewer than four of its eight adjacent cells also contain rolls,
# and your task is to count all such accessible rolls.


import argparse
import curses
import os.path
import time

import numpy as np

VERBOSE = False

def print_frame(shape, scr, offset):

    # Top and bottom edge
    for x in range(shape[1]):
        scr.addstr(offset[0], offset[1] + x, "═")
        scr.addstr(offset[0] + shape[0] -1, offset[1] + x, "═")

    # Left and right edge
    for y in range(shape[0]):
        scr.addstr(offset[0] + y, offset[1], "║")
        scr.addstr(offset[0] + y, offset[1] + shape[1] -1, "║")

    # Corners
    scr.addstr(offset[0], offset[1], "╔")
    scr.addstr(offset[0] + shape[0] - 1, offset[1], "╚")
    scr.addstr(offset[0], offset[1] + shape[1] -1, "╗")
    scr.addstr(offset[0] + shape[0] - 1, offset[1] + shape[1] -1, "╝")

def print_map(scr, map_array, counter_array, offset, highlight=False):
    for y, row in enumerate(map_array):
        for x, val in enumerate(row):
            if highlight:
                if val == "@" and counter_array[y+1, x+1] <= 3:
                    scr.addstr(offset[0] + y, offset[1] + x, val, curses.color_pair(1))
                elif val == ",":
                    scr.addstr(offset[0] + y, offset[1] + x, ".", curses.color_pair(2))
                elif val == ".":
                    scr.addstr(offset[0] + y, offset[1] + x, " ")
                elif val == "@":
                    scr.addstr(offset[0] + y, offset[1] + x, "@")
                else:
                    scr.addstr(offset[0] + y, offset[1] + x, "?")


            else:
                scr.addstr(y + offset[0], x + offset[1], " " if val == "," or val == "." else val)

def print_full_map(scr, map_array, counter_array, offset, render_shape, highlight=False):
    print_frame((render_shape[0] + 2, render_shape[1] + 2),
                scr,
                (offset[0] - 1, offset[1] - 1))
    print_map(scr, map_array[0:render_shape[0], 0:render_shape[1]], counter_array, offset=offset, highlight=highlight)
    scr.refresh()
    time.sleep(0.5)


def get_count_array(shape):
    return np.pad(np.zeros(shape), pad_width=1, mode="constant", constant_values=0)

def get_adjacency_array():
    adjacency_array = np.ones((3, 3))
    adjacency_array[1, 1] = 0
    return adjacency_array

def add_array_at(a1, a2, y, x):
    a1[y:y + a2.shape[0],
        x:x + a2.shape[1]] += a2
    return a1

def compute_adjacent(map_array, counter_array, mask_array):
    for y, row in enumerate(map_array):
        for x, val in enumerate(row):
            if val == ",":
                map_array[y, x] = "."
            if val == "@":
                if VERBOSE:
                    print(f"Found roll at ({y}, {x})")
                add_array_at(counter_array, mask_array, y, x)
    return map_array, counter_array

def check_adjacent(map_array, counter_array):
    accessible_rolls = 0
    for y, row in enumerate(map_array):
        for x, val in enumerate(row):
            if val == "@" and counter_array[y+1, x+1] <= 3:
                accessible_rolls += 1
                map_array[y, x] = ","

    return accessible_rolls, map_array

def main(input_data, _args):

    # Create empty array to count adjacent rolls
    count_array = get_count_array(input_data.shape)
    adjacency_array = get_adjacency_array()

    accessible_count = 0
    total_removed = 0
    removable_at_start = 0

    while accessible_count != 0 or total_removed == 0:
        input_data, counter_array = compute_adjacent(input_data, count_array, adjacency_array)
        accessible_count, input_data = check_adjacent(input_data, counter_array)
        if total_removed == 0:
            removable_at_start = accessible_count
        total_removed += accessible_count
        counter_array.fill(0)

    if 1 in _args.part:
        print(f"Removable at first step: {removable_at_start}")

    if 2 in _args.part:
        print(f"Total removable rolls: {total_removed}")

def run (stdscr, input_data, _args):
    height, width = stdscr.getmaxyx()
    print(height, width)
    curses.curs_set(0)                      # set cursor invisible
    curses.use_default_colors()             # use default colors (-1)


    curses.init_pair(1, curses.COLOR_GREEN, -1) # selected
    curses.init_pair(2, curses.COLOR_RED, -1)  # deleted

    render_height = min(height, input_data.shape[0])
    render_width = min(width, input_data.shape[1])

    count_array = get_count_array(input_data.shape)
    adjacency_array = get_adjacency_array()

    accessible_count = 0
    total_removed = 0
    removable_at_start = 0

    # print_frame((2,3), stdscr, 1, 3)
    map_offset = (1, 1)

    while accessible_count != 0 or total_removed == 0:
        input_data, counter_array = compute_adjacent(input_data, count_array, adjacency_array)

        print_full_map(stdscr, input_data, counter_array, map_offset, (render_height - map_offset[0] - 1, render_width - map_offset[1] - 1), True)

        accessible_count, input_data = check_adjacent(input_data, counter_array)

        print_full_map(stdscr, input_data, counter_array, map_offset, (render_height - map_offset[0] - 1, render_width - map_offset[1] - 1), True)

        if total_removed == 0:
            removable_at_start = accessible_count
        total_removed += accessible_count
        stdscr.addstr(2, render_width + map_offset[1], f"Removed rolls: {total_removed}")
        stdscr.refresh()
        counter_array.fill(0)

    stdscr.refresh()
    stdscr.getkey()



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input file name", default="input_test.txt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-c", "--curses", action="store_true", help="Enable curses mode")
    parser.add_argument("-p", "--part", help="Select part (1 or 2)", action="store", type=int, default=[1, 2], nargs="+")
    args = parser.parse_args()
    VERBOSE = args.verbose

    # Check if given file exists
    if not os.path.isfile(args.file):
        print("Input file does not exist")
        exit()

    with open(args.file, "r") as file:
        raw_input = file.read()

    parsed_input = np.array([list(line)for line in raw_input.split("\n")])

    if "TERM_PROGRAM" in os.environ and args.curses:
        curses.wrapper(run, parsed_input, args)
    else:
        if os.environ.get("PYCHARM_HOSTED"):
            VERBOSE = True
        main(parsed_input, args)