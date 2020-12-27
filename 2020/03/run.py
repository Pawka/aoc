def read(filename):
    data = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data


def solve(data, right=3, down=1):
    trees = 0
    i = right
    line = down
    width = len(data[0])
    while line < len(data):
        if data[line][i % width] == '#':
            trees += 1
        i += right
        line += down
    return trees


def solve2(data):
    a1 = solve(data, 1, 1)
    a2 = solve(data, 3, 1)
    a3 = solve(data, 5, 1)
    a4 = solve(data, 7, 1)
    a5 = solve(data, 1, 2)
    return a1 * a2 * a3 * a4 * a5


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
