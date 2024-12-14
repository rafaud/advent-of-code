import random
import re

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import aoc_helper

# DEBUG = True
DEBUG = False

area_size = (101, 103) if not DEBUG else (11, 7)
input_data = [line.strip() for line in aoc_helper.get_data(DEBUG)]

class Robot:
    def __init__(self, pos: (int, int), vel: (int, int)) -> None:
        self.pos = pos
        self.vel = vel

    def add_robot_to_area(self, _area: np.ndarray) -> np.ndarray:
        _area[self.pos[1], self.pos[0]] += 1
        return _area

    def step(self, _area_size: (int, int)):
        new_pos_x = self.pos[0] + self.vel[0]
        if new_pos_x < 0:
            new_pos_x += area_size[0]
        if new_pos_x > area_size[0] - 1:
            new_pos_x -= area_size[0]

        new_pos_y = self.pos[1] + self.vel[1]
        if new_pos_y < 0:
            new_pos_y += area_size[1]
        if new_pos_y > area_size[1] - 1:
            new_pos_y -= area_size[1]

        self.pos = (new_pos_x, new_pos_y)

def get_string_for_area(_area):
    max_value = _area.argmax()
    max_value_length = len(str(max_value))
    lines = []
    for line in _area:
        l = [str(num).zfill(max_value_length) for num in line]
        lines.append(" ".join(l))
    return "\n".join(lines)

def get_area_for_robots(_area_size, _robots):
    area = np.array([[0 for _ in range(_area_size[0])] for _ in range(_area_size[1])])
    for _robot in _robots:
        area = _robot.add_robot_to_area(area)
    return area

def save_area_as_jpg(_area, output):
    _area = np.array([[255 if value > 0 else 0 for value in line] for line in _area], dtype=np.uint8)
    Image.fromarray(_area).save(output)
    save_array_jpg(_area, output)

def save_array_jpg(_array, output):
    im = Image.fromarray(_array, mode="L")
    im.save(output)

def get_quarter(index, _area):
    area_height, area_width = _area.shape
    multiplier_x = 0 if index == 1 or index == 3 else 1
    multiplier_y = 0 if index == 1 or index == 2 else 1
    width = (area_width - 1) // 2
    height = (area_height - 1) // 2
    start_point_x = 0 + multiplier_x * (width + 1)
    start_point_y = 0 + multiplier_y * (height + 1)
    return _area[start_point_y:start_point_y + height, start_point_x:start_point_x + width]

def get_x_variance(_robots):
    return_value = []
    for _robot in _robots:
        return_value.append(_robot.pos[0])

    return np.var(return_value)

def get_y_variance(_robots):
    return_value = []
    for _robot in _robots:
        return_value.append(_robot.pos[1])

    return np.var(return_value)


robots = []
for line in input_data:
    regex = r"p=(-?\d+),(-?\d+)\sv=(-?\d+),(-?\d+)"
    capture_groups = re.search(regex, line).groups()
    pos_x, pos_y, vel_x, vel_y = (int(value) for value in capture_groups)
    robot = Robot((pos_x, pos_y), (vel_x, vel_y))
    robots.append(robot)

steps_count = max(area_size)
variances = []
# variances.append((get_x_variance(robots), get_y_variance(robots)))
for i in range(steps_count):
    for robot in robots:
        robot.step(area_size)
    # print(f"Second {i}")
    area = get_area_for_robots(area_size, robots)
    variances.append((get_x_variance(robots), get_y_variance(robots)))
    # if i == 3926:
    #     save_area_as_jpg(area, f"output/{i}.jpg")
    # with open(f"output/{i}.txt", "w") as output_file:
        # output_file.write(get_string_for_area(get_area_for_robots(area_size, robots)).replace("0", " "))

area = get_area_for_robots(area_size, robots)

quarters = []
for i in range(4):
    quarters.append(get_quarter(i + 1, area).sum())

safety_factor = 1
for num in quarters:
    safety_factor *= num

print(f"Safety factor: {safety_factor}")

x_values = [x for x, _ in variances]
y_values = [y for _, y in variances]
bx = x_values.index(min(x_values))
by = y_values.index(min(y_values))
h = area_size[0]
w = area_size[1]
x_values[bx] = 999
y_values[by] = 999
t = bx + w * ((pow(w, -1, h) * (by - bx)) % h)
print(bx, by)
print(w, h)
print("Part 2:", bx+((pow(h, -1, w)*(by-bx)) % h)*w)
print(t)


