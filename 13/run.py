def read(filename):
    with open(filename, 'r') as reader:
        return [line.strip() for line in reader.readlines()]


def solve(data):
    ts = int(data[0])
    numbers = [int(x) for x in data[1].split(',') if x != 'x']

    nearest = {}
    for num in numbers:
        nearest[num] = ts+num-ts % num

    earliest = min(nearest.values())
    for k in nearest:
        if earliest == nearest[k]:
            return k * (earliest-ts)


def solve2(data):
    parts = [int(x) if x.isnumeric() else 0 for x in data[1].split(',')]

    diffs = {}
    for k, p in enumerate(parts):
        if p > 0:
            diffs[p] = k
    highest = max(parts)

    ts = 0
    while True:
        ts += highest
        print(ts)
        if check(diffs, ts, highest):
            return ts - diffs[highest]


def check(diffs, ts, highest):
    fixed_ts = ts - diffs[highest]
    for bus in diffs:
        if (fixed_ts % bus + diffs[bus]) % bus != 0:
            return False
    return True


if __name__ == "__main__":
    data = read('input.txt')
    # print(solve(data))
    print(solve2(data))
