# Created by rafaud@icloud.com
# The task is to scan several numeric ID ranges and identify every number that consists of a two repeated sequence of digits
# (like 55, 6464, or 123123), then sum all such “invalid” IDs across all ranges.


import argparse
import os.path


def split_string_equal_parts(s, part_length):
    if len(s) % part_length == 0:
        return [s[i:i + part_length] for i in range(0, len(s), part_length)]
    else:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input file name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    # Check if given file exists
    if not os.path.isfile(args.file):
        print("Input file does not exist")
        return

    with open(args.file, "r") as file:
        raw_input = file.read()

    ranges = [
        (int(b1), int(b2))
        for bounds in raw_input.split(",")
        for b1, b2 in [bounds.split("-")]
        ]

    invalid_ids_p1 = p1(args, ranges)
    invalid_ids_p2 = p2(args, ranges)

    if args.verbose:
        print(f"[p1] Found {len(invalid_ids_p1)} invalid ids: {', '.join([str(_id) for _id in invalid_ids_p1])}")
    print(f"[p1] Sum of all invalid IDs is: {sum(invalid_ids_p1)}")

    if args.verbose:
        print(f"[p2] Found {len(invalid_ids_p2)} invalid ids: {', '.join([str(_id) for _id in invalid_ids_p2])}")
    print(f"[p2] Sum of all invalid IDs is: {sum(invalid_ids_p2)}")




def p1(args, ranges):
    if args.verbose:
        print("\n\n==== Starting with part 1 ====\n\n")
    invalid_ids = []

    for b1, b2 in ranges:
        if args.verbose:
            print(f"Checking range {b1}-{b2}")
        for i in range(b1, b2 +1, 1):
            q, r = divmod(len(str(i)), 2)
            if r == 0:
                id_parts = split_string_equal_parts(str(i), q)
                if id_parts:
                    if int(id_parts[0]) == int(id_parts[1]):
                        invalid_id = ''.join(id_parts)
                        invalid_ids.append(int(invalid_id))
                        if args.verbose:
                            print(f"\tFound invalid id: {invalid_id}")
    return invalid_ids

def p2(args, ranges):
    if args.verbose:
        print("\n\n==== Starting with part 2 ====\n\n")
    invalid_ids = []

    for b1, b2 in ranges:
        if args.verbose:
            print(f"Checking range {b1}-{b2}")
        for i in range(b1, b2 +1, 1):
            max_sequence_length, r = divmod(len(str(i)), 2)
            for sequence_length in range(1, max_sequence_length+1, 1):
                q, r = divmod(len(str(i)), sequence_length)
                if r == 0 and len(str(i)) != sequence_length:
                    id_parts = split_string_equal_parts(str(i), sequence_length)
                    if id_parts:
                        if len(set(id_parts)) == 1:
                            invalid_id = ''.join(id_parts)
                            invalid_ids.append(int(invalid_id))
                            if args.verbose:
                                print(f"\tFound invalid id: {invalid_id}")
                                print(f"\t{id_parts}")
    return list(set(invalid_ids))

if __name__ == "__main__":
    main()