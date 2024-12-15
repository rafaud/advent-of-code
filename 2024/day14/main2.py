# made with knowledge from the vast internet
import math
import os
import re
from time import sleep

import numpy as np
import curses


def step(_t):
    return [((_px + _vx * _t) % w, (_py + _vy * _t) % h) for (_px, _py, _vx, _vy) in robots]

def ide_run():

    q = [0, 0, 0, 0]
    half_x = (w - 1) // 2
    half_y = (h - 1) // 2

    for rx, ry in step(100):
        if rx < half_x and ry < half_y: q[0] += 1
        elif rx > half_x and ry < half_y: q[1] += 1
        elif rx < half_x and ry > half_y: q[2] += 1
        elif rx > half_x and ry > half_y: q[3] += 1

    print("Safety factor: ", q[0] * q[1] * q[2] * q[3])

    bx, bx_var, by, by_var = 0, math.inf, 0, math.inf
    for t in range(max(w, h)):
        px, py = zip(*step(t))

        if (x_var := np.var(px)) < bx_var: bx, bx_var = t, x_var
        if (y_var := np.var(py)) < by_var: by, by_var = t, y_var

    print("Answer p2: ", bx + ((pow(w, -1, h) * (by - bx)) % h) * w)

def terminal_run(stdscr):
    stdscr.clear()
    # robot color ■
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    fps = 60
    frame_time = 1 / fps
    run_time = 5 # in seconds
    frames = fps * run_time
    key_frame = 6577

    for i in range(key_frame - frames, key_frame + 1):
        frame = step(i)

        stdscr.erase()
        print_frame(stdscr, frame)
        stdscr.refresh()

        sleep(frame_time)

    stdscr.getkey()

def print_frame(stdscr, frame):
    for robot in frame:
        x, y = robot
        stdscr.addstr(y, x*2, "██", curses.color_pair(1))

if __name__ == "__main__":
    w, h = 101, 103
    data = open('input.txt', 'r').read()

    # put robots in tuple with
    robots = [[int(a) for a in re.findall(r"(-?\d+)", line)] for line in data.split("\n")]

    if "TERM_PROGRAM" in os.environ:
        curses.wrapper(terminal_run)
    else:
        ide_run()




