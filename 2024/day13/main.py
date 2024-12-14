import re
import numpy as np
import aoc_helper

# DEBUG = True
DEBUG = False

token_cost = {"A": 3, "B": 1}

input_data = aoc_helper.get_data(DEBUG)
claw_machines_strings = []
for i in range(0, len(input_data), 4):
    claw_machines_strings.append([line.strip() for line in input_data[i:i + 3]])

measurement_error = 10000000000000
# measurement_error = 0

claw_machines = []
for claw_machine in claw_machines_strings:
    coefficients_capture_button_A = re.search(r"X([+-]\d+).*Y([+-]\d+)", claw_machine[0])
    coefficients_capture_button_B = re.search(r"X([+-]\d+).*Y([+-]\d+)", claw_machine[1])
    coefficients_capture_prize = re.search(r"X=(\d+).*Y=(\d+)", claw_machine[2])

    coefficients_movement = np.array([[int(a) for a  in coefficients_capture_button_A.groups()], [int(b) for b in coefficients_capture_button_B.groups()]])
    coefficients_prize = np.array([[int(p) + measurement_error] for p in coefficients_capture_prize.groups()])

    coefficients_movement_inverted = np.linalg.inv(coefficients_movement.transpose())
    moves = np.matmul(coefficients_movement_inverted, coefficients_prize).transpose()[0]
    moves = [int(round(moves[0], 0)), int(round(moves[1], 0))]

    claw_machines.append({
        "movement": coefficients_movement,
        "prize": coefficients_prize.transpose()[0],
        "movement_inverted": coefficients_movement_inverted,
        "moves": moves
    })

total_cost = 0
for claw_machine in claw_machines:
    moves = claw_machine["moves"]
    buttons = claw_machine["movement"]
    prize = claw_machine["prize"]
    end_point = [moves[0] * buttons[0] + moves[1] * buttons[1]]
    # print(end_point)
    # print(prize)
    truth_table = end_point == prize
    if truth_table.all():
        total_cost += moves[0] * token_cost["A"] + moves[1] * token_cost["B"]

print(total_cost)
