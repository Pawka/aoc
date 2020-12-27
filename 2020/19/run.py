import re

from collections import defaultdict
from pprint import pprint


def read(name):
    parts = []
    with open(name) as reader:
        parts = reader.read().split("\n\n")

    parts[0] = parts[0].strip().split("\n")
    parts[1] = parts[1].strip().split("\n")
    return parts


def parse(rules, visited=set()):
    result = defaultdict(list)
    for rule in rules:
        index, rule = rule.split(":")
        key = int(index)
        for part in rule.split(" | "):
            part = part.strip()
            if '"' in part:
                part = part.replace('"', '')
                result[key] = part
            else:
                result[key].append([int(x) for x in part.split(' ')])
    return result


assert parse(['1: "a"']) == {1: "a"}
assert parse(['3: 4 5 | 5 4']) == {3: [[4, 5], [5, 4]]}


def solve(data):
    rules, tasks = data
    rules = parse(rules)
    pprint(rules)

    rule = tree(rules, 0)
    pprint(rule)
    valid = 0
    for task in tasks:
        r = "^" + rule + "$"
        if re.match(r, task) is not None:
            valid += 1
    return valid


def tree(rules, root=0, depth=0):
    if depth == 20:
        return ""
    if type(rules[root]) == str:
        return rules[root]

    branches = []
    for b, branch in enumerate(rules[root]):
        sub = ""
        for k in branch:
            sub += tree(rules, k, depth + 1)
        branches.append(sub)
    return "(" + "|".join(branches) + ")"


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    data2 = read('input3.txt')
    print(solve(data2))
