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

        # Calculate:
        # new_position_relative - position on infinite dial with negative numbers
        # new_position_absolute - position on 0 - 99 dial
        # full_rotations - how many full rotations there were

        new_position_relative = position + rotation
        full_rotations, new_position_absolute = divmod(new_position_relative, DIAL_SIZE)

        if args.verbose:
            print(f"\tFull rotations: {abs(full_rotations)}")

        # Modulo "hides" crossing exactly zero, but only for 0 itself and negative numbers so we need to add that one rotation
        # Start at 50; rotate 100 left; land on -50; divmod(-50, 100)=(-1, 50); One crossing (abs(-1)) and land on 50.      Correct answer
        # Start at 50; rotate 150 left; land on -100; divmod(-100, 100)=(-1, 0); One crossing (abs(-1)) and land on 0.      Incorrect answer
        # Start at 50; rotate 151 left; land on -101; divmod(-101, 100)=(-2, 99); Two crossings (abs(-2)) and land on 99.   Correct answer
        if new_position_absolute == 0 and new_position_relative <= 0:
            if args.verbose:
                print(f"\tLanded on zero.")
            zeros_counter += 1

        # Starting rotation to the left from zero results in one additional "crossing" due to the nature of modulo, we need to eliminate this
        # Start at 0; rotate 2 left; land on -2; divmod(-2, 100)=(-1, 98); One crossing (abs(-1)) and land on 98.           Incorrect answer
        if position == 0 and new_position_relative < 0:
            if args.verbose:
                print(f"\tStarted left rotation from zero.")
            zeros_counter -= 1

        # Add full rotations and update position
        zeros_counter += abs(full_rotations)
        position = new_position_absolute

        # Part 1, just count landings on zero
        if new_position_absolute == 0:
            if args.verbose:
                print(f"\t[P1] Landed on zero.")
            zero_stops += 1

        # Brute Force
        # if position == 0 and rotation < 0:
        #     position += DIAL_SIZE
        #
        # position += rotation
        # while position > DIAL_SIZE:
        #     if args.verbose:
        #         print("\tOver 100, one 0 crossing")
        #     position -= DIAL_SIZE
        #     zeros_counter += 1
        # if position == DIAL_SIZE:
        #     position = 0
        #
        # while position < 0:
        #     if args.verbose:
        #         print("\tUnder 100, one 0 crossing")
        #     position += DIAL_SIZE
        #     zeros_counter += 1
        #
        # if position == 0:
        #     if args.verbose:
        #         print("\tLanded on 0")
        #     zeros_counter += 1
        #     zero_stops += 1

        if args.verbose:
            print(f"The dial was rotated {"R" if rotation > 0 else "L"}{abs(rotation)} to point at {position}, total zero crossings: {zeros_counter}.\n")
    # Results should be 1026 and 5923
    print(f"Dial stopped at 0 total of {zero_stops} times.")
    print(f"Dial pointed at 0 total of {zeros_counter} times.")

if __name__ == "__main__":
    main()