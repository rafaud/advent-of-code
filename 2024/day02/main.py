import re
import numpy as np

# DEBUG = True
DEBUG = False

# Load test data or task data, depending on the debug variable
if DEBUG:
    input_values = []
    with open("input_test.txt", 'r') as f:
        while line :=  f.readline():
            input_values.append([int(i) for i in re.findall(r"(\d+)\s+", line)])
else:
    input_values = []
    with open("input.txt", 'r') as f:
        while line :=  f.readline():
            input_values.append([int(i) for i in re.findall(r"(\d+)\s+", line)])


def check_values(values, dampener=False):

    # negative value for decreasing;
    # positive value for increasing;
    #              0 for undetermined
    list_order = values[1] - values[0]

    # Check if first values are different if not remove one and repeat procedure
    if list_order == 0 and dampener:
        # trigger dampener
        values_copy = values[:]
        values_copy.pop(0)
        if check_values(values_copy, dampener=False):
            print(f"\t is safe after removing value with index 0")
            return True
        print(f"\t is not safe")
        return False
    elif list_order == 0 and not dampener:
        print(f"\t is not safe [repeated values]")
        return False

    # If numbers are different, reverse if list is decreasing, it doesn't matter in the end
    # if list_order < 0: values.reverse()

    # Iterate over the list
    for i in range(len(values) - 1):

        # Check sorting
        if (values[i] > values[i + 1] and list_order > 0) or (values[i] < values[i + 1] and list_order < 0):
            print("\tSorting check")
            if dampener:
                values_copy = values[:]
                values_copy.pop(i)
                print(f"\t removing index {i}")
                if check_values(values_copy, dampener=False):
                    print(f"\t is safe after removing value with index {i}")
                    return True
                else:
                    values_copy = values[:]
                    values_copy.pop(i+1)
                    print(f"\t removing index {i+1}")
                    if check_values(values_copy, dampener=False):
                        print(f"\t is safe after removing value with index {i+1}")
                        return True
                    # edge chase {48 46 47 49 51 54 56}, from first two values order is expected to be decreasing;
                    # but unsafe list will be detected between indexes 1 and 2, we need to remove first index to
                    # change expected list order,
                    elif i > 0:
                        values_copy = values[:]
                        values_copy.pop(i - 1)
                        print(f"\t removing index {i - 1}")
                        if check_values(values_copy, dampener=False):
                            print(f"\t is safe after removing value with index {i - 1}")
                            return True
            print(f"\t is not safe [not sorted at index {i}]")
            return False

        diff = abs(values[i + 1] - values[i])
        if diff < 1 or diff > 3:
            print("\tGradient check")
            if dampener:
                values_copy = values[:]
                values_copy.pop(i)
                print(f"\t removing index {i}")
                if check_values(values_copy, dampener=False):
                    print(f"\t is safe after removing value with index {i}")
                    return True
                else:
                    values_copy = values[:]
                    values_copy.pop(i+1)
                    print(f"\t removing index {i+1}")
                    if check_values(values_copy, dampener=False):
                        print(f"\t is safe after removing value with index {i+1}")
                        return True
            print(f"\t is unsafe [gradient too big at index {i}]")
            return False
    print(f"\t is safe")
    return True


safe_reports = 0
for values in input_values:
    print(f"Checking {values}")
    if check_values(values, dampener=False): safe_reports += 1
print(f"Safe reports: {safe_reports}\n\n\n")

safe_reports = 0
for values in input_values:
    print(f"Checking {values}")
    if check_values(values, dampener=True): safe_reports += 1

print(f"Safe reports with dampener: {safe_reports}")