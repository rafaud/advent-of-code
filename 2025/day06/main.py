# Created by rafaud@icloud.com


import argparse
import curses
import os.path
from types import SimpleNamespace

import numpy as np

VERBOSE = False

def parse_for_part_1(input_data):
    parsed_input = np.transpose(
        np.array(
            [[char
              for char in line.split(" ")
              if char not in ("", " ")
              ]
             for line in raw_input.split("\n")
             ],
            ),
        )

    values = np.array([[ int(value)
        for value in line
        ]
        for line in parsed_input[:,:-1]
        ])
    operations = np.transpose(parsed_input[:,-1:])[0]

    return values, operations

def perform_opeartions(values, operations, _args):
    total_sum = 0
    for i, line in enumerate(values):
        if operations[i] == "+":
            if VERBOSE:
                print(f"Calculating '{operations[i]}' for line: {line}.")
            result = sum(line)
            if VERBOSE:
                print(f"\tResult: {result}")
        elif operations[i] == "*":
            if VERBOSE:
                print(f"Calculating '{operations[i]}' for line: {line}.")
            result = 1
            for value in line:
                result *= value
            if VERBOSE:
                print(f"\tResult: {result}")
        else:
            result = 0
        total_sum += result

    return total_sum

def console_part_1(input_data, _args):
    values, operations = parse_for_part_1(input_data)
    total_sum = perform_opeartions(values, operations, _args)
    print(total_sum)

def parse_for_part_2(input_data):
    unpadded_lines = (
        [
            list(line)
            for line in input_data.split("\n")
            ]
    )

    max_length = max(map(len, unpadded_lines))
    padded_lines = [
        line + [" "] * (max_length - len(line))
        for line in unpadded_lines
        ]

    lines = np.rot90(np.array(padded_lines))
    values = [ "".join(line)
        for line in lines[:, :-1]
        ]
    split_list = []
    for i, value in enumerate(values):
        if not value.strip():
            split_list.append(i)

    values = np.split(values, split_list)

    values = [ [ int(value.strip())
        for value in line
        if value.strip()
        ]
               for line in values
        ]

    operations = [ v
        for v in np.transpose(lines[:, -1:])[0]
                   if v not in ("", " ")
        ]
    return values, operations

def console_part_2(input_data, _args):

    values, operations = parse_for_part_2(input_data)
    total_sum = perform_opeartions(values, operations, _args)
    print(total_sum)

def main(input_data, _args):

    # if 1 in _args.part:
    #     if VERBOSE:
    #         print(f"Solving part 1")
    #     console_part_1(input_data, _args)

    if 2 in _args.part:
        console_part_2(input_data, _args)

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



    if "TERM_PROGRAM" in os.environ and args.curses:
        curses.wrapper(run, raw_input, args)
    else:
        if os.environ.get("PYCHARM_HOSTED"): # Check if run in PyCharm
            VERBOSE = True
        main(raw_input, args)