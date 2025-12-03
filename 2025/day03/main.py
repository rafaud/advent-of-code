# Created by rafaud@icloud.com
# You’re given several banks of battery joltages, each represented as a line of digits.
# For each bank, you must choose two digits in order (without rearranging) to form the largest possible two-digit number,
# and then sum the maximums from all banks to get the total output joltage.

import argparse
import os.path
from copy import deepcopy


def get_bank_max_joltage_p1(_bank):
    max_index = _bank.index(max(_bank))
    max_value = _bank[max_index]

    if max_index == len(_bank) - 1:
        _bank[max_index] = 0
        second_index = _bank.index(max(_bank))
        max_joltage = _bank[second_index] * 10 + max_value
    else:
        _bank[0:max_index + 1] = [0] * (max_index + 1)
        second_index = _bank.index(max(_bank))
        max_joltage = max_value * 10 + _bank[second_index]
    return max_joltage

def get_max_value_with_mask(_bank, mask, args):
    masked_bank = _bank[0:len(_bank) - mask]

    if args.verbose:
        print(f"\t\tGetting max value for bank {_bank} with mask {mask}")
        print(f"\t\tMasked bank:               {masked_bank}")
    max_index = masked_bank.index(max(masked_bank))
    max_value = masked_bank[max_index]
    if args.verbose:
        print(f"\t\tmax_index: {max_index}, max_value: {max_value}")
    return max_index, max_value

def get_bank_max_joltage_p2(_bank, digits, args):
    bank_max_joltage = 0
    for i in range(digits-1, -1, -1):
        max_index, max_value = get_max_value_with_mask(_bank, i, args)
        bank_max_joltage += max_value * pow(10, i)
        _bank[0:max_index + 1] = [0] * (max_index + 1)
        if args.verbose:
            print(f"\tMax joltage for bank after finding {12 - i} digits: {bank_max_joltage}")
    return bank_max_joltage

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

    banks = [[int(v) for v in list(bank)] for bank in raw_input.strip().split("\n")]

    # for bank in banks:
    #     p1_joltage = get_bank_max_joltage_p1(deepcopy(bank))
    #     p2_joltage = get_bank_max_joltage_p2(deepcopy(bank), 2, args)
    #     print(f"P1: {p1_joltage}, P2: {p2_joltage}")
    #     if p1_joltage != p2_joltage:
    #         break



    p1(args, deepcopy(banks))
    p2(args, deepcopy(banks), 2)
    p2(args, deepcopy(banks), 12)



def p1(args, banks):

    maximum_joltage = 0

    for bank in banks:
        maximum_joltage += get_bank_max_joltage_p1(bank)

    print(f"Maximum joltage is {maximum_joltage} J.")

def p2(args, banks, digits):


    maximum_joltage = 0
    for index, bank in enumerate(banks):
        maximum_joltage += get_bank_max_joltage_p2(bank, digits, args)
        if args.verbose:
            print(f"Joltage for bank {index}: {maximum_joltage}")


    print(f"Maximum joltage is {maximum_joltage} J.")

if __name__ == "__main__":
    main()