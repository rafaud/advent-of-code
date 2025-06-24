with open("input.txt") as f:
     raw_input_values, raw_gates = (section.split("\n") for section in f.read().split("\n\n"))

wires = {}
for input_value in raw_input_values:
    wire, value = input_value.split(": ")
    wires[wire] = int(value)

gates = []
for gate in raw_gates:
    gates.append(tuple(gate.replace(" -> ", " ").split(" ")))

def perform_operation(value1, value2, _operation):
    if _operation == "AND":
        return value1 and value2
    if _operation == "OR":
        return value1 or value2
    if _operation == "XOR":
        return value1 ^ value2


some_skipped = True
while some_skipped:
    some_skipped = False
    for wire1, operation, wire2, output in gates:
        if wire1 not in wires or wire2 not in wires:
            some_skipped = True
            continue
        v1 = wires[wire1]
        v2 = wires[wire2]
        wires[output] = perform_operation(v1, v2, operation)

output_bits = [ str(val[1])
                for val in
                sorted({k: v for k, v in wires.items() if k[0] == "z"}.items(),
                       key=lambda item: int(item[0][1:]),
                       reverse=True)]
print(output_bits)
number = int("".join(output_bits), 2)
print(number)

