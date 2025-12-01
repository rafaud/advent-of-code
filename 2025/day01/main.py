# Created by rafaud@icloud.com
# You’re given a series of left/right dial rotations from an initial position on a circular dial,
# you must count how many times the dial ends up pointing at 0 after applying each rotation.
# x 6958

import argparse
import os.path

START_POSITION = 50
DIAL_SIZE = 100

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    # Check if given file exists
    if not os.path.isfile(args.input):
        print("Input file does not exist")
        return

    with open(args.input, "r") as file:
        raw_input = file.read()


    rotations = [int(rotation.replace("R", "").replace("L", "-")) for rotation in raw_input.split("\n")]

    zeros_counter = 0
    zero_stops = 0
    position = START_POSITION

    if args.verbose:
        print(f"The dial starts by pointing at: {position}")

    for index, rotation in enumerate(rotations):
        # rotation - how far it should move
        # position - current pointing direction
        # zeros_counter - how many zeros were hit

        if args.verbose:
            print(f"{index}. The dial will be rotated {"R" if rotation > 0 else "L"}{abs(rotation)} from {position}.")

        # Brute Force
        # TODO: Make a better version of this

        if position == 0 and rotation < 0:
            position += DIAL_SIZE

        position += rotation
        while position > DIAL_SIZE:
            if args.verbose:
                print("\tOver 100, one 0 crossing")
            position -= DIAL_SIZE
            zeros_counter += 1
        if position == DIAL_SIZE:
            position = 0

        while position < 0:
            if args.verbose:
                print("\tUnder 100, one 0 crossing")
            position += DIAL_SIZE
            zeros_counter += 1

        if position == 0:
            if args.verbose:
                print("\tLanded on 0")
            zeros_counter += 1
            zero_stops += 1

        if args.verbose:
            print(f"The dial was rotated {"R" if rotation > 0 else "L"}{abs(rotation)} to point at {position}, total zero crossings: {zeros_counter}.\n")
    print(f"Dial stopped at 0 total of {zero_stops} times.")
    print(f"Dial pointed at 0 total of {zeros_counter} times.")

if __name__ == "__main__":
    main()