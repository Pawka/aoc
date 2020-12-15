from pprint import pprint


def read(name):
    with open(name) as reader:
        return [l.strip() for l in reader.readlines()]


def solve(data):
    positions = {}

    for k, d in enumerate(data):
        if k == len(data) - 1:
            break
        positions[d] = k

    i = len(data)
    current = data[-1]
    while i < 2020:
        last = positions.get(current, None)
        positions[current] = i-1
        if last is None:
            current = 0
        else:
            current = i - 1 - last
        i += 1

    return current


def solve2(data):
    pass


if __name__ == "__main__":
    input1 = [12, 1, 16, 3, 11, 0]
    input2 = [0, 3, 6]
    print(solve(input1))
    # print(solve2(data))
