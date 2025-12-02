#!/bin/bash

# Check if exactly two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <year> <day>"
    exit 1
fi

# Assign parameters to variables
year=$1
day=$2

# Validate that year is a four-digit number
if ! [[ $year =~ ^[0-9]{4}$ ]]; then
    echo "Error: Year must be a four-digit number."
    exit 1
fi

# Validate that day is a positive integer
if ! [[ $day =~ ^[0-9]+$ ]] || [ "$day" -le 0 ]; then
    echo "Error: Day must be a positive integer."
    exit 1
fi

# Format day with leading zero if needed
day=$(printf "%02d" $day)

# Construct the directory path
dir_path="$year/day$day"

# Create the directory
mkdir -p "$dir_path"

# Create the files in the directory
touch "$dir_path/input.txt" "$dir_path/input_test.txt"
cp python_template.py "$dir_path/main.py"

# Provide feedback to the user
echo "Created directory and files:"
echo "$dir_path"
echo "$dir_path/input.txt"
echo "$dir_path/input_test_1.txt"
echo "$dir_path/main.py"
