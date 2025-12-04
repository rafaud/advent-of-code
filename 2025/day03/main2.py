# Created by rafaud@icloud.com
# Day 3 but with animations


import argparse
import curses
import os.path
import random
import time

BANK_BOTTOM_SPACING = 3
BANK_VERTICAL_OFFSET = 3

def show_banks(banks, stdscr, interval=0.1):
    height, width = stdscr.getmaxyx()
    for index, bank in enumerate(banks):
        if index + BANK_VERTICAL_OFFSET + BANK_BOTTOM_SPACING > height:
            break
        bank.show_to_screen(stdscr)
        stdscr.refresh()
        sleep(args, stdscr, interval)

def show_sum(banks, stdscr, x, y):
    height, width = stdscr.getmaxyx()
    if y > height:
        y = height - 1

    total_joltage = 0
    for bank in banks:
        total_joltage += bank.power
    stdscr.addstr(y, x, f"Total Joltage: {total_joltage}")

def sleep(_args, stdscr, _time):
    if _args.verbose:
        stdscr.getkey()
    else:
        time.sleep(_time)

class DataBank:
    def __init__(self,
                 cells,
                 mask,
                 selected,
                 bank_index):
        self.cells = cells
        self.mask = mask
        self.selected = selected
        self.index = bank_index
        self.cell_count = len(cells)

    def show_to_screen(self, scr):
        scr.addstr(self.index + BANK_VERTICAL_OFFSET, 0, "[")
        for index, cell in enumerate(self.cells):

            scr.addstr(self.index + BANK_VERTICAL_OFFSET, index + 1, str(cell), curses.color_pair(
                1 if self.cell_count - self.mask <= index else
                2 if index in self.selected else
                1 if index < max(self.selected, default=-1) else
                1 if self.mask == -1 else
                0))
        scr.addstr(self.index + BANK_VERTICAL_OFFSET, len(self.cells) + 1, "]")
        scr.addstr(self.index + BANK_VERTICAL_OFFSET, len(self.cells) + 5, f"Cell Joltage: ")
        scr.addstr(f"{self.power}", curses.color_pair(
            2 if self.mask == -1 else
            0,
            ))

    def select_max_value_with_mask(self):
        masked_cells = self.cells[0:self.cell_count - self.mask]
        if self.selected:
            masked_cells[0:max(self.selected)+1] = [0] * (max(self.selected) + 1)
        max_index = masked_cells.index(max(masked_cells))
        self.selected.append(max_index)

    @property
    def power(self):
        return_value = 0
        for i, index in enumerate(self.selected):
            return_value += self.cells[index] * pow(10, len(self.selected) - 1 - i)
        return return_value

def run(stdscr, args):
    height, width = stdscr.getmaxyx()

    curses.curs_set(0)
    curses.use_default_colors()

    GRAY_INDEX = 8
    R = G = B = 500  # Values range from 0–1000 (this is mid-gray)
    curses.init_color(GRAY_INDEX, R, G, B)
    curses.init_pair(1, GRAY_INDEX, -1) # mask
    curses.init_pair(2, curses.COLOR_GREEN, -1)  # selected


    # Check if given file exists
    if not os.path.isfile(args.file):
        print("Input file does not exist")
        return

    with open(args.file, "r") as file:
        raw_input = file.read()

    if not os.path.isfile(args.file):
        print("Input file does not exist")
        return

    with open(args.file, "r") as file:
        raw_input = file.read()

    banks = [DataBank([int(cell) for cell in bank], 0, [], index) for index, bank in enumerate(raw_input.strip().split("\n"))]

    stdscr.clear()

    stdscr.addstr(0, 0, "Collecting cell banks")
    stdscr.refresh()

    sleep(args, stdscr, 0.5)
    stdscr.addstr(".")
    stdscr.refresh()

    sleep(args, stdscr, 0.5)
    stdscr.addstr(".")
    stdscr.refresh()
    sleep(args, stdscr, 0.5)

    stdscr.addstr(".")
    stdscr.refresh()
    sleep(args, stdscr, 0.5)

    stdscr.addstr(1, 0, f"Found {len(banks)} banks, each with {banks[0].cell_count} cells")
    stdscr.refresh()
    sleep(args, stdscr, 0.5)

    show_banks(banks, stdscr, interval=0.01)
    sleep(args, stdscr, 0.5)

    digits = 12
    for index, bank in enumerate(banks):
        bank.mask = digits -1
        show_banks(banks, stdscr, interval=0)
        sleep(args, stdscr, 0 if index + BANK_VERTICAL_OFFSET + BANK_BOTTOM_SPACING > height else 0.01)

    banks_todo = list(range(len(banks)))
    while banks_todo:
        choice = random.choice(banks_todo)
        banks[choice].select_max_value_with_mask()
        banks[choice].mask -= 1
        if banks[choice].mask == -1:
            banks_todo.remove(choice)

        show_banks(banks, stdscr, interval=0)
        show_sum(banks, stdscr, y=len(banks) + 4, x=0)
        sleep(args, stdscr, 0 if choice + BANK_VERTICAL_OFFSET + BANK_BOTTOM_SPACING > height else 0.01)

    # for i in range(digits-1, -1, -1):
    #     for bank in banks:
    #         bank.mask = i
    #         bank.select_max_value_with_mask()
    #     show_banks(banks, stdscr, interval=0)
    #     show_sum(banks, stdscr, y=len(banks) + 4, x=0)
    #     sleep(args, stdscr, 0.5)

    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input file name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    if not args.file:
        args.file = "input_test.txt"


    print(args)

    if "TERM_PROGRAM" in os.environ:
        curses.wrapper(run, args)
    else:
        args.verbose = True


