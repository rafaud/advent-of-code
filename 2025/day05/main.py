# Created by rafaud@icloud.com
# You’re given a list of fresh ingredient ID ranges and a list of available ingredient IDs.
# Your task is to count how many of the available IDs fall within any of the fresh ID ranges (inclusive).


import argparse
import curses
import os.path
from types import SimpleNamespace

VERBOSE = False

def console_p1(input_data, _args):
    if VERBOSE:
        print("Part 1: Checking list for fresh ids...", end="")
    valid_ids_from_ingredient_list = 0
    for _id in input_data.ids:
        if VERBOSE:
            print(f"\n\tChecking id: {_id}...", end="")
        for rng in input_data.ranges:
            if rng[0] <= _id <= rng[1]:
                if VERBOSE:
                    print(f" Fresh!", end="")
                valid_ids_from_ingredient_list += 1
                break
    if VERBOSE:
        print()
    print(f"Total valid ids: {valid_ids_from_ingredient_list}")

def console_p2(input_data, _args):
    if VERBOSE:
        print("Part 1: Finding all valid ids...", end="")
    redundant_ranges = []
    sorted_ranges = sorted(input_data.ranges, key=lambda rng: rng[0])
    for i in range(len(sorted_ranges)):
        if i < len(sorted_ranges):
            for index, rng in enumerate(sorted_ranges[i+1:]):
                first_range_index = i
                second_range_index = index + i + 1
                first_range = sorted_ranges[first_range_index]
                second_range = sorted_ranges[second_range_index]
                print(first_range_index, second_range_index, first_range, second_range)
                if first_range[1] >= second_range[0]:
                    if VERBOSE:
                        print(f"\tFound overlap in ranges: {first_range} and {second_range}")
                    if first_range[1] < second_range[1]:
                        if VERBOSE:
                            print(f"\tExpanding range: ({first_range[0]}, {second_range[1]})")
                        sorted_ranges[first_range_index] = (first_range[0], second_range[1])
                    if VERBOSE:
                        print(f"\tMarking range {second_range_index} for removal.")
                    redundant_ranges.append(second_range_index)

    for i in sorted(set(redundant_ranges), reverse=True):
        del sorted_ranges[i]

    total_valid_ids = 0
    for rng in sorted_ranges:
        total_valid_ids += rng[1] - rng[0] + 1

    print(f"Total valid ids: {total_valid_ids}")




def main(input_data, _args):

    if 1 in _args.part:
        console_p1(input_data, _args)
    if 2 in _args.part:
        console_p2(input_data, _args)





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

    ranges_raw, ids_raw = raw_input.split("\n\n")
    ranges = (
        (int(r1), int(r2))
        for rng in ranges_raw.split("\n")
        for r1, r2 in [rng.split("-")]
        )

    _ids = (int(i) for i in ids_raw.split("\n"))
    parsed_input = SimpleNamespace(ranges=list(ranges), ids=list(_ids))
    # fresh_ids = {}
    # for rng in ranges_raw:


    if "TERM_PROGRAM" in os.environ and args.curses:
        curses.wrapper(run, parsed_input, args)
    else:
        if os.environ.get("PYCHARM_HOSTED"): # Check if run in PyCharm
            VERBOSE = True
        main(parsed_input, args)