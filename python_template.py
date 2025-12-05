# Created by rafaud@icloud.com


import argparse
import curses
import os.path

VERBOSE = False

def main(input_data, _args):
    # solution goes here
    None

def run (stdscr, input_data, _args):
    height, width = stdscr.getmaxyx()
    curses.curs_set(0)                      # set cursor invisible
    curses.use_default_colors()             # use default colors (-1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input file name", default="input_test.txt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("-c", "--curses", action="store_true", help="Enable curses mode")
    parser.add_argument("-p", "--part", help="Select part (1 or 2)", action="store", type=int, default=[1], nargs="+")
    args = parser.parse_args()
    VERBOSE = args.verbose

    # Check if given file exists
    if not os.path.isfile(args.file):
        print("Input file does not exist")
        exit()

    with open(args.file, "r") as file:
        raw_input = file.read()

    parsed_input = raw_input.split("\n")

    if "TERM_PROGRAM" in os.environ and args.curses:
        curses.wrapper(run, parsed_input, args)
    else:
        if os.environ.get("PYCHARM_HOSTED"): # Check if run in PyCharm
            VERBOSE = True
        main(parsed_input, args)