import aoc_helper

# DEBUG = True
DEBUG = False

input_data = [input_data.strip() for input_data in aoc_helper.get_data(DEBUG)]

def line_to_dict(line):
    total, values = line.split(": ")
    return {"total": int(total), "values": values}

eq = [line_to_dict(line) for line in input_data]

def get_total_values_sign(values: [str], sign: str):
    # 0 - addition
    # 1 - multiplication
    # 2 - concatenation
    a, b = values
    a = int(a)
    b = int(b)
    if sign == "0":
        _total = a + b
        return _total
    elif sign == "1":
        _total = a * b
        return _total
    elif sign == "2":
        _total = int(f"{a}{b}")
        return _total

def get_sign_map(value: int, total_signs: int, base: int = 2):
    if base == 2:
        return f"{value:0{total_signs}b}"
    else:
        values = []
        while value:
            value, reminder = divmod(value, base)
            values.append(str(reminder))
        return "0" * (total_signs - len(values)) + "".join(reversed(values))


def get_possible_totals(values, base: int = 2):
    values = values.split(" ")
    total_signs = len(values) - 1
    total_combinations = base ** total_signs
    totals = []

    for i in range(total_combinations):
        sign_map = get_sign_map(i, total_signs, base)
        _total = get_total_values_sign(values[:2], sign_map[0])
        for j, sign in enumerate(sign_map[1:]):
            _total = get_total_values_sign([_total, values[j + 2]], sign)
        totals.append({"total": _total, "signs": sign_map})
    return totals

results = []
for index, line in enumerate(eq):
    print(f"Processing line {(index + 1):03d} of {len(eq)}")
    possible_values_add_mul = get_possible_totals(line["values"])
    possible_values_add_mul_con = get_possible_totals(line["values"], base=3)
    results.append({"eq": line,
                    "possible_values_add_mul": possible_values_add_mul,
                    "possible_values_add_mul_con": possible_values_add_mul_con})

total_add_mul = 0
total_add_mul_con = 0
for result in results:
    if result["eq"]["total"] in [pv["total"] for pv in result["possible_values_add_mul"]]:
        total_add_mul += result["eq"]["total"]
    if result["eq"]["total"] in [pv["total"] for pv in result["possible_values_add_mul_con"]]:
        total_add_mul_con += result["eq"]["total"]

print(f"Sum of all possible equations (add, mul): {total_add_mul}")
print(f"Sum of all possible equations (add, mul, con): {total_add_mul_con}")


