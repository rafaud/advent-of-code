"""
    pointer starts at 0, increases by 2 after each operation

    0:adv - division: A // <combo operand> => A;
    1:bxl - bitwise XOR: B XOR <literal operand> => B;
    2:bst - modulo: <combo operand> % 8 => B;
    3:jnz - jump: if A == 0, do not jump; else, jump to <literal operand>, pointer does not increase after jump;
    4:bxc - bitwise XOR: B XOR C => B, (reads an operand but ignores it);
    5:out - out: <combo operand> % 8, and prints output;
    6:bdv - division: A // <combo operand> => B;
    7:cdv - division: A // <combo operand> => C;

    <literal operand> - just a number
    <combo operand> -
        0 - 3:  numbers
        4:      register A
        5:      register B
        6:      register C
        7:      does not appear in valid programs


    2,4, A % 8 => B     - leaves last 3 bits
    1,1, B XOR 1 => B   - flips last bit        B = 3 bits(0 - 7)
    7,5, A // B => C    -
    0,3, A // 3 => A
    1,4, B XOR A => B
    4,0, B XOR C => B
    5,5, print( B % 8 )
    3,0
"""
from time import sleep


def dv(register: int, operand: int):
    global a, b, c
    value = a // pow(2, get_combo_operand_value(operand))
    if register == 0: a = value
    if register == 1: b = value
    if register == 2: c = value

def jnz(operand: int):
    global pointer
    if a == 0: pointer += 2
    else: pointer = operand
with open("input.txt") as f:
    lines = f.readlines()

def execute_operation(opcode: int, operand: int):
    global b, c, pointer, output
    match opcode:
        case 0: dv(0, operand)
        case 1: b = b ^ operand
        case 2: b = get_combo_operand_value(operand) % 8
        case 3: jnz(operand)
        case 4: b = b ^ c
        case 5:
            output.append(get_combo_operand_value(operand) % 8)
        case 6: dv(1, operand)
        case 7: dv(2, operand)
    if opcode != 3: pointer += 2

def get_combo_operand_value(operand:int):
    if operand == 4: return a
    if operand == 5: return b
    if operand == 6: return c
    else: return operand

lines = [line.strip().split(" ") for line in lines]
a, b, c = int(lines[0][2]), int(lines[1][2]), int(lines[2][2])
program = [int(value) for value in lines[4][1].split(",")]
pointer = 0
output = []

while pointer < len(program):
    execute_operation(program[pointer], program[pointer + 1])

print("Answer part I: ", ",".join([str(foo) for foo in output]))

# https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2gkd6m/

exponents = list(range(len(program)))
factors = [0] * len(exponents)
search_factor = len(factors) - 1
base = 8
next_a = sum([f * pow(base, e) for f, e in zip(factors, exponents)])

while True:
    factors[search_factor] += 1
    next_a = sum([f * pow(base, e) for f, e in zip(factors, exponents)])
    a, b, c = next_a, 0, 0
    pointer = 0
    output = []
    while pointer < len(program):
        execute_operation(program[pointer], program[pointer+1])
    if output == program:
        print("Answer part II: ", next_a)
        break
    for i in range(len(factors)-1,-1,-1):
        if output[i] != program[i]:
            search_factor = i
            break

