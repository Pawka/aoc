from collections import defaultdict, deque


def read(name):
    result = []
    with open(name) as r:
        result = [tuple(line.strip().split(')')) for line in r.readlines()]
    return result


def solve(data):
    graph = defaultdict(list)
    bidirectional = defaultdict(list)

    for edge in data:
        a, b = edge
        graph[a].append(b)
        bidirectional[a].append(b)
        bidirectional[b].append(a)

    def walk(root, depth=0):
        distance = 1
        for node in graph[root]:
            distance += depth + walk(node, depth+1)
        return distance
    result1 = walk('COM') - 1

    def solve2(target='SAN'):
        dist = defaultdict(int)
        seen = set()
        visit = deque(['YOU'])

        while True:
            current = visit.pop()
            if current in seen:
                continue
            seen.add(current)
            for node in bidirectional[current]:
                visit.appendleft(node)
                dist[node] = dist[current] + 1
                if node == target:
                    return dist[target] - 2

    result2 = solve2()
    return result1, result2


if __name__ == "__main__":
    data = read("data/day06.txt")
    print(solve(data))
