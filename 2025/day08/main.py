# Created by rafaud@icloud.com


import argparse
import curses
import os.path

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import KDTree

VERBOSE = False

def get_closest_neighbors(points, number_of_neighbors):
    # Build KDTree
    tree = KDTree(points)

    points_neighbors_data = []

    if VERBOSE:
        print("Finding closest neighbors")
    # For each point, query the nearest neighbors
    for i, point in enumerate(points):
        points_neighbors_data.append(tree.query(point, k=number_of_neighbors+1))  # first is self, second is nearest, and so on

    distances_data = set()

    if VERBOSE:
        print("Creating distance list of neighbors")

    print(points_neighbors_data)
    for distances, point_indexes in points_neighbors_data:
        print(f"Processing point: {point_indexes[0]}")
        for index, (distance, point_index) in enumerate(zip(distances[1:], point_indexes[1:])):
            print(point_index, point_indexes[0])
            if point_indexes[0] < point_index:
                ia = point_indexes[0]
                ib = point_index
            else:
                ia = point_index
                ib = point_indexes[0]

            pa = points[ia]
            pb = points[ib]

            distance_data = (float(distance),
                             (tuple(pa), tuple(pb)),
                             (int(ia), int(ib)))
            distances_data.add(distance_data)
    distances_data = list(distances_data)

    if VERBOSE:
        print("Sorting list")
    distances_data.sort(key=lambda x: x[0])

    return distances_data

def draw_points(ax, points):
    # Scatter the points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='blue')

    # Labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Points with Connecting Lines")

    ax.set_xlim(min(points[:, 0]), max(points[:, 0]))
    ax.set_ylim(min(points[:, 1]), max(points[:, 1]))
    ax.set_zlim(min(points[:, 2]), max(points[:, 2]))

def draw_lines(ax, pairs):
    for pair in pairs:
        x = [pair[0][0], pair[1][0]]
        y = [pair[0][1], pair[1][1]]
        z = [pair[0][2], pair[1][2]]
        ax.plot(x, y, z, color='red')


def main(input_data, _args):
    distance_data = get_closest_neighbors(input_data, _args.neighbors)


    G = nx.Graph()
    G.add_edges_from(
        (indexes
         for _, _, indexes in distance_data[:_args.connections]
         )
        )

    components = list(nx.connected_components(G))
    sizes = (len(component)
             for component in components)
    # print(sorted(sizes, reverse=True)[:3])

    total = 1
    for size in sorted(sizes, reverse=True)[:3]:
        total *= size
    print(total)


    # Create 3D figure
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # draw_points(ax, np.array(input_data))
    # draw_lines(ax, (points
    #     for _, points, _ in distance_data[:_args.connections]
    # ))
    # plt.show()


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

    parsed_input = [list(map(int, line.split(",")))
        for line in raw_input.split("\n")
        ]

    if args.file == "input.txt":
        args.connections = 1000
    else:
        args.connections = 10

    args.neighbors = min(20, len(parsed_input) - 1)

    if "TERM_PROGRAM" in os.environ and args.curses:
        curses.wrapper(run, parsed_input, args)
    else:
        if os.environ.get("PYCHARM_HOSTED"): # Check if run in PyCharm
            VERBOSE = True
        main(parsed_input, args)