# Created by rafaud@icloud.com


import argparse
import curses
import os.path
from copy import deepcopy
from functools import cache

from contourpy import calc_chunk_sizes

VERBOSE = False

def console_p1(input_data, _args):
    print(input_data[0])
    split_counter = 0
    for line_index, line in enumerate(input_data[1:], start=1):
        for char_index, char in enumerate(line):
            if char == "." and input_data[line_index-1][char_index] in ("S", "|"):
                input_data[line_index][char_index] = "|"
            elif char == "^" and input_data[line_index-1][char_index] in ("S", "|"):
                input_data[line_index][char_index-1] = "|"
                input_data[line_index][char_index+1] = "|"
                split_counter += 1
        print(line)
    print(split_counter)

@cache
def aa(input_data, start):
    total_paths = 0
    if start[0] == len(input_data)-1:
        if VERBOSE:
            print(f"Finished path, returning {total_paths + 1}")
        return 1
    else:
        if VERBOSE:
            print("Path not finished")
        if input_data[start[0]+1][start[1]] == ".":
            if VERBOSE:
                print("Found empty space, propagating down.")
            return aa(input_data, (start[0]+1, start[1]))
        elif input_data[start[0]+1][start[1]] == "^":
            if VERBOSE:
                print(f"Found splitter, propagating down in two directions.")
                print(f"\tPath 1, with total paths: {total_paths}")
            total_paths += aa(input_data, (start[0]+1, start[1]-1))
            if VERBOSE:
                print(f"\tPath 2, with total paths: {total_paths}")
            return total_paths + aa(input_data, (start[0]+1, start[1]+1))
        else:
            if VERBOSE:
                print("Something went wrong!")
            return 0


def console_p2(input_data, _args):
    start_index = (0, input_data[0].index("S"))
    total_paths = 0
    total_paths += aa(input_data, start_index)
    print(total_paths)


def main(input_data, _args):
    # if 1 in _args.part:
    #     console_p1(deepcopy(input_data), _args)
    if 2 in _args.part:
        console_p2(deepcopy(input_data), _args)


def run (stdscr, input_data, _args):
    height, width = stdscr.getmaxyx()
    curses.curs_set(0)                      # set cursor invisible
    curses.use_default_colors()             # use default colors (-1)

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

    parsed_input = tuple(tuple(
        str(char)
        for char in line
        )
        for line in raw_input.split("\n")
    )

    if "TERM_PROGRAM" in os.environ and args.curses:
        curses.wrapper(run, parsed_input, args)
    else:
        if os.environ.get("PYCHARM_HOSTED"): # Check if run in PyCharm
            VERBOSE = True
        main(parsed_input, args)