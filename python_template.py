# Created by rafaud@icloud.com


import argparse
import os.path


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

    # solution goes here

if __name__ == "__main__":
    main()