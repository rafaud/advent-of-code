import curses
import os
from time import sleep

from Map import Map

def run(stdscr):
    # Clear screen
    stdscr.clear()
    # Walls color
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)

    # Boxes color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    # Robot color
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Text color
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    step = 1
    while warehouse_map.moves_left:
        stdscr.erase()
        # warehouse_map.print_map(stdscr)
        warehouse_map.move()
        stdscr.addstr("\n")
        stdscr.addstr(f"Step: {step:04d} / {warehouse_map.total_moves}, Total: {warehouse_map.total:020d}")
        stdscr.refresh()
        step += 1
        # sleep(0.1)

    stdscr.erase()
    warehouse_map.print_map(stdscr)
    stdscr.getkey()

warehouse_map = Map.load_from_file("input.txt", part=2)
if "TERM_PROGRAM" in os.environ:
    curses.wrapper(run)
else:
    for i in range(100):
        print("Step: ", i)
        print(warehouse_map.map_string)
        warehouse_map.move()
        # sleep(1)
print("Total: ", warehouse_map.total)






