def read(name):
    data = []
    with open(name) as f:
        for line in f.readlines():
            items = []
            for i in line.strip():
                items.append(0 if i == "." else 1)
            data.append(items)
    return data


def solve(data):
    height = len(data)
    width = len(data[0])

    # Already 1 because the first run will take all seats.
    times = 1

    while True:
        changes = []
        # visited = [[0 for i in range(width)] for j in range(height)]
        for row in range(height):
            for col in range(width):
                if data[row][col] != 0:
                    _taken = adjacent(data, row, col, width, height)
                    size = len(_taken)
                    if data[row][col] == 1 and size >= 4:
                        changes.append((row, col))
                    elif data[row][col] == -1 and size == 0:
                        changes.append((row, col))

        for t in changes:
            data[t[0]][t[1]] *= -1

        if len(changes) == 0:
            return sum([sum(filter(lambda a: a == 1, row)) for row in data])
        times += 1


def adjacent(data, row, col, width, height):
    adj = []
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if i >= 0 and i < height:
                if j >= 0 and j < width:
                    if (i == row and col == j) is False and data[i][j] == 1:
                        adj.append((i, j))
    return adj


test_data = [
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 0],
]

assert adjacent(test_data, 0, 0, 3, 3) == [(1, 0), (1, 1)]
assert adjacent(test_data, 0, 2, 3, 3) == [(1, 1), (1, 2)]
assert adjacent(test_data, 2, 1, 3, 3) == [(1, 0), (1, 1), (1, 2)]

def solve2(data):
    height = len(data)
    width = len(data[0])

    # Already 1 because the first run will take all seats.
    times = 1

    while True:
        changes = []
        # visited = [[0 for i in range(width)] for j in range(height)]
        for row in range(height):
            for col in range(width):
                if data[row][col] != 0:
                    size = adjacent2(data, row, col, width, height)
                    if data[row][col] == 1 and size >= 5:
                        changes.append((row, col))
                    elif data[row][col] == -1 and size == 0:
                        changes.append((row, col))

        for t in changes:
            data[t[0]][t[1]] *= -1

        if len(changes) == 0:
            return sum([sum(filter(lambda a: a == 1, row)) for row in data])
        times += 1


def adjacent2(data, row, col, width, height):
    ocupied = 0

    # Right
    i = col + 1
    while i < width:
        if data[row][i] == -1:
            break
        if data[row][i] == 1:
            ocupied += 1
            break
        i += 1

    # Left
    i = col - 1
    while i >= 0:
        if data[row][i] == -1:
            break
        if data[row][i] == 1:
            ocupied += 1
            break
        i -= 1

    # up
    i = row - 1
    while i >= 0:
        if data[i][col] == -1:
            break
        if data[i][col] == 1:
            ocupied += 1
            break
        i -= 1

    # down
    i = row + 1
    while i < height:
        if data[i][col] == -1:
            break
        if data[i][col] == 1:
            ocupied += 1
            break
        i += 1

    # right-up
    i = col + 1
    j = row - 1
    while i < width and j >= 0:
        if data[j][i] == -1:
            break
        if data[j][i] == 1:
            ocupied += 1
            break
        i += 1
        j -= 1

    # right-down
    i = col + 1
    j = row + 1
    while i < width and j < height:
        if data[j][i] == -1:
            break
        if data[j][i] == 1:
            ocupied += 1
            break
        i += 1
        j += 1

    # left-down
    i = col - 1
    j = row + 1
    while i >= 0 and j < height:
        if data[j][i] == -1:
            break
        if data[j][i] == 1:
            ocupied += 1
            break
        i -= 1
        j += 1

    # left-up
    i = col - 1
    j = row - 1
    while i >= 0 and j >= 0:
        if data[j][i] == -1:
            break
        if data[j][i] == 1:
            ocupied += 1
            break
        i -= 1
        j -= 1

    return ocupied


test01 = [
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
]

assert adjacent2(test01, 2, 2, 5, 5) == 8


if __name__ == "__main__":
    data = read("input.txt")
    print(solve(data))
    print(solve2(data))
