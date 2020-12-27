import collections


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
    numbers = []
    for k, p in enumerate(parts):
        if p > 0:
            diffs[p] = k
            numbers.append(p)

    idiffs = collections.OrderedDict({
        numbers[0]: diffs[numbers[0]],
        numbers[1]: diffs[numbers[1]],
    })
    ts = 0
    increase = numbers[0]
    while True:
        if check(idiffs, ts):
            if len(idiffs) == len(numbers):
                return ts
            increase = 1
            for k in idiffs:
                increase *= k
            next_bus = numbers[len(idiffs)]
            idiffs[next_bus] = diffs[next_bus]
        ts += increase

    return ts


def check(diffs, ts):
    for bus in diffs:
        if (ts % bus + diffs[bus]) % bus != 0:
            return False
    return True


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
