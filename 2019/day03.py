def read(name):
    with open(name) as r:
        return [line.strip().split(',') for line in r.readlines()]


def draw(line):
    points = []
    current = (0, 0)
    for part in line:
        direction, distance = part[0], int(part[1:])
        last = None
        if direction == 'R':
            for i in range(current[0] + 1, current[0] + distance + 1, 1):
                last = (i, current[1])
                points.append(last)
        elif direction == 'L':
            for i in range(current[0] - 1, current[0] - distance - 1, -1):
                last = (i, current[1])
                points.append(last)
        elif direction == 'U':
            for i in range(current[1] + 1, current[1] + distance + 1, 1):
                last = (current[0], i)
                points.append(last)
        elif direction == 'D':
            for i in range(current[1] - 1, current[1] - distance - 1, -1):
                last = (current[0], i)
                points.append(last)

        current = last
    return points


def solve(data):
    line1 = draw(data[0])
    line2 = draw(data[1])
    sline1 = set(line1)
    sline2 = set(line2)
    intersections = sline1.intersection(sline2)
    distance = min([abs(a[0]) + abs(a[1]) for a in intersections])
    steps = None
    for point in intersections:
        index1 = line1.index(point)
        index2 = line2.index(point)
        candidate = index1 + index2 + 2
        if steps is None or candidate < steps:
            steps = candidate

    return distance, steps


if __name__ == "__main__":
    data = read('data/day03.txt')
    print(solve(data))
