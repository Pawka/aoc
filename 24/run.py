import re
from pprint import pprint


def read(name):
    result = []
    with open(name) as reader:
        for line in reader.readlines():
            coords = [
                x for x in re.split("(se|sw|nw|ne|w|e)", line.strip())
                if len(x)]
            result.append(coords)
    return result


def get_grid(size=100, color=1):
    grid = [[0 for _ in range(size)] for _ in range(size)]

    for row in range(size):
        for col in range(size):
            if (row + col) % 2 == 0:
                grid[row][col] = color

    return grid


MAP = {
    "se": (1, 1),
    "sw": (1, -1),
    "ne": (-1, 1),
    "nw": (-1, -1),
    "w": (0, -2),
    "e": (0, 2),
}


def get_coordinations(name):
    return MAP[name]


def solve(data):
    size = 250
    grid = get_grid(size)

    start = (int(size/2), int(size/2))
    if grid[start[0]][start[1]] != 1:
        return "Something wrong"
    for path in data:
        current = start
        for step in path:
            row, col = get_coordinations(step)
            current = (current[0] + row, current[1] + col)
            if grid[current[0]][current[1]] == 0:
                return "Something wrong"
        grid[current[0]][current[1]] *= -1
    return grid


def count(grid):
    return len([x for row in grid for x in row if x == -1])


def get_blacks(grid, row, col):
    total = 0
    for k in MAP:
        drow, dcol = MAP[k]
        if grid[row+drow][col+dcol] == -1:
            total += 1
    return total


def solve2(grid):
    size = len(grid)
    for day in range(100):
        updates = []
        for row in range(size-1):
            # TODO: this can be optimized with step of 2.
            for col in range(size-2):
                color = grid[row][col]
                if color != 0:
                    blacks = get_blacks(grid, row, col)
                    if color == -1 and (blacks == 0 or blacks > 2):
                        updates.append((row, col))
                    elif color == 1 and blacks == 2:
                        updates.append((row, col))
        for row, col in updates:
            grid[row][col] *= -1
    return count(grid)


if __name__ == "__main__":
    data = read("input.txt")
    grid = solve(data)
    result1 = count(grid)
    print(result1)
    print(solve2(grid))
