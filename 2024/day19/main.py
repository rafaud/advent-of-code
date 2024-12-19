from collections import defaultdict
from functools import cache

with open("input.txt") as f:
    data = f.read()

towels, _, *patterns = data.split("\n")
towels = towels.split(", ")

@cache
def test_pattern(p: str):
    if p=="": return 1
    return_array = []
    for prefix in towels:
        if p.startswith(prefix):
            return_array.append(
                test_pattern(p.removeprefix(prefix))
            )
    return sum(return_array)

result = list(map(test_pattern, patterns))
print("Possible patterns:", sum(map(bool, result)))
print("Possible combinations:", sum(result))
