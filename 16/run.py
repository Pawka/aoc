from pprint import pprint
from collections import namedtuple


def read(name):
    with open(name) as reader:
        return reader.read().split("\n\n")


Rule = namedtuple('Rule', 'left right')


def parse(data):
    constraints = {}
    for line in data[0].split("\n"):
        key, values = line.split(":")
        for val in values.split(" or "):
            f, to = val.split("-")
            constraints.setdefault(key, []).append(Rule(int(f), int(to)))
    your_ticket = [int(i) for i in data[1].split("\n")[1].split(",")]

    tickets = []
    for line in data[2].strip().split("\n")[1:]:
        tickets.append([int(i) for i in line.split(",")])

    return (constraints, your_ticket, tickets)


def solve(data):
    rules, your_ticket, tickets = data
    result1 = 0
    valid_tickets = []
    for ticket in tickets:
        validation = validate(rules, ticket)
        result1 += validation
        if validation == 0:
            valid_tickets.append(ticket)

    candidates = {}
    for name in rules:
        rule = rules[name]
        valid_columns = find_valid_columns(valid_tickets, rule)
        candidates[name] = valid_columns
    pprint(candidates)

    rules_map = {}
    while len(rules_map) != len(candidates):
        found = None
        for k in candidates:
            if len(candidates[k]) == 1:
                found = candidates[k].pop()
                rules_map[k] = found
        for k in candidates:
            if found in candidates[k]:
                candidates[k].remove(found)

    result2 = 1
    for k in rules_map:
        if k.split(" ")[0] == "departure":
            result2 *= your_ticket[rules_map[k]]
    return result1, result2


def validate(rules, line):
    result = 0
    for item in line:
        valid = False
        for name in rules:
            r = rules[name]
            if (item >= r[0].left and item <= r[0].right
                    or item >= r[1].left and item <= r[1].right):
                valid = True
                break
        if valid is False:
            result += item
    return result


def find_valid_columns(tickets, rule):
    result = []
    for col in range(len(tickets[0])):
        valid = True
        for row in range(len(tickets)):
            item = tickets[row][col]
            if (item < rule[0].left or
                    item > rule[0].right and item < rule[1].left or
                    item > rule[1].right):
                valid = False
                break
        if valid:
            result.append(col)
    return result


if __name__ == "__main__":
    lines = read('input.txt')
    data = parse(lines)
    print(solve(data))
