import sys


def read(name):
    with open(name) as r:
        return [int(l.strip()) for l in r.readlines()]


def solve(data):
    total = 0
    for mass in data:
        total += divmod(mass, 3)[0] - 2
    return total


def solve2(data):
    total = 0
    for mass in data:
        tmass = mass
        while tmass > 0:
            tmass = divmod(tmass, 3)[0] - 2
            if tmass > 0:
                total += tmass
    return total


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
