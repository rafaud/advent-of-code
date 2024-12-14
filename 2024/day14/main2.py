# made with knowledge from the vast internet

import re
import numpy as np

w, h = 101, 103
data = open('input.txt', 'r').read()

# put robots in tuple with
robots = [[int(a) for a in re.findall(r"(-?\d+)", line)] for line in data.split("\n")]


def step(_t):
    return [((_px + _vx * _t) % w, (_py + _vy * _t) % h) for (_px, _py, _vx, _vy) in robots]


q = [0, 0, 0, 0]
half_x = (w - 1) // 2
half_y = (h - 1) // 2

for rx, ry in step(100):
    if rx < half_x and ry < half_y: q[0] += 1
    elif rx > half_x and ry < half_y: q[1] += 1
    elif rx < half_x and ry > half_y: q[2] += 1
    elif rx > half_x and ry > half_y: q[3] += 1

print("Safety factor: ", q[0] * q[1] * q[2] * q[3])

bx, bx_var, by, by_var = 0, 999_999, 0, 999_999
for t in range(max(w, h)):
    px, py = zip(*step(t))

    if (x_var := np.var(px)) < bx_var: bx, bx_var = t, x_var
    if (y_var := np.var(py)) < by_var: by, by_var = t, y_var

print("Answer p2: ", bx + ((pow(w, -1, h) * (by - bx)) % h) * w)



