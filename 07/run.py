import re


def read(filename):
    data = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data


def parse_bags(line):
    key_match = re.match("^(\w+ \w+) bags contain ", line)
    key = key_match.groups()[0]
    content = line[key_match.end():]
    if content == "no other bags.":
        return (key, [])

    parts = content.split(",")
    contents = []
    for part in parts:
        content_match = re.match("^(\d+) (\w+ \w+)", part.strip())
        groups = content_match.groups()
        contents.append(
            (groups[1], int(groups[0]))
        )
    return (key, contents)


assert ("bright aqua", [
    ("plaid magenta", 5),
    ("muted lavender", 5),
    ("dim turquoise", 4),
    ("shiny turquoise", 1)
    ]) == parse_bags((
        "bright aqua bags contain 5 plaid magenta bags, "
        "5 muted lavender bags, 4 dim turquoise bags, 1 shiny turquoise bag.")
        )

assert ("pale chartreuse", []) == parse_bags(
        "pale chartreuse bags contain no other bags.")


def build_parents(lines):
    parents = {}
    for line in lines:
        bag, contents = parse_bags(line)
        for inner_bag, _ in contents:
            if inner_bag not in parents:
                parents[inner_bag] = set()
            parents[inner_bag].add(bag)
    return parents


def solve(lines):
    parents = build_parents(lines)
    gold = "shiny gold"
    visited = set()

    to_visit = set([gold])
    while len(to_visit) > 0:
        current = to_visit.pop()
        visited.add(current)
        for bag in parents.get(current, []):
            if bag not in visited:
                to_visit.add(bag)
    return len(visited)-1


def build_graph(lines):
    graph = {}
    for line in lines:
        bag, contents = parse_bags(line)
        for inner_bag, count in contents:
            if bag not in graph:
                graph[bag] = {}
            graph[bag][inner_bag] = count
    return graph


def walk(graph, key):
    total = 1
    subgraph = graph.get(key, {})
    if len(subgraph) == 0:
        return total

    for bag in subgraph:
        count = subgraph[bag]
        total += count * walk(graph, bag)
    return total


def assert_walk():
    lines = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
    graph = build_graph(lines.split("\n"))
    result = walk(graph, "shiny gold") - 1
    assert 126 == result


assert_walk()


def solve2(lines):
    graph = build_graph(lines)
    return walk(graph, "shiny gold") - 1


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
