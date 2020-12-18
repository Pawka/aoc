from pprint import pprint
from collections import namedtuple

Dimmensions = namedtuple('Dimmensions', 'size height width')


def read(name):
    data = []
    with open(name) as reader:
        for line in reader.readlines():
            data.append([int(c) for c in
                        line.strip().replace('.', '0').replace('#', '1')])
    return data


def solve(data):
    cube = [data]

    for _ in range(6):
        dimm = Dimmensions(len(cube), len(cube[0]), len(cube[0][0]))

        new_cube = []
        for depth in range(0, dimm.size+1):
            new_row = []
            for row in range(-1, dimm.height+1):
                new_col = []
                for col in range(-1, dimm.width+1):
                    active = is_active(cube, row, col, depth, dimm)
                    new_col.append(int(active))
                new_row.append(new_col)
            new_cube.append(new_row)
        cube = new_cube

    total_cubes = sum([val for sublist in cube[0] for val in sublist])
    total_cubes += 2 * sum([val for z in cube[1:] for r in z for val in r])
    return total_cubes


def get_friends(cube, row, col, depth, dimmensions):
    size, height, width = dimmensions
    count = 0
    for z in range(depth-1, 1+min(depth+1, size-1)):
        z_tocheck = z
        if z < 0:
            if size == 1:
                continue
            z_tocheck = min(1, size-1)

        inclusive = not z == depth
        count += get_flat_friends(
                cube[z_tocheck], row, col, dimmensions, inclusive)
    return count


def get_flat_friends(matrix, row, col, dimmensions, inclusive=False):
    _, height, width = dimmensions

    count = 0
    for i in range(max(0, row-1), 1+min(height-1, row+1)):
        for j in range(max(0, col-1), 1+min(width-1, col+1)):
            if matrix[i][j] == 1:
                if row == i and col == j and inclusive is False:
                    continue
                count += 1
    return count


"""
.#.
..#
###
"""
test_case = read('input2.txt')
test_dimmensions = Dimmensions(1, 3, 3)
assert get_flat_friends(test_case, 0, 0, test_dimmensions) == 1
assert get_flat_friends(test_case, 0, 1, test_dimmensions) == 1
assert get_flat_friends(test_case, 1, 0, test_dimmensions) == 3
assert get_flat_friends(test_case, 0, 1, test_dimmensions, True) == 2
assert get_flat_friends(test_case, 1, 1, test_dimmensions) == 5
assert get_flat_friends(test_case, 2, 2, test_dimmensions) == 2
assert get_flat_friends(test_case, -1, -1, test_dimmensions) == 0
assert get_flat_friends(test_case, -1, 0, test_dimmensions) == 1
assert get_flat_friends(test_case, 3, 1, test_dimmensions) == 3

assert get_friends([test_case], 0, 0, 0, test_dimmensions) == 1
assert get_friends([test_case], 1, 1, 0, test_dimmensions) == 5
assert get_friends([test_case], 0, 0, 1, test_dimmensions) == 1
assert get_friends([test_case], 1, 0, 0, test_dimmensions) == 3
assert get_friends([test_case, test_case], 1, 1, 0, Dimmensions(2, 3, 3)) == 15
assert get_friends([test_case, test_case], 1, 1, 1, Dimmensions(2, 3, 3)) == 10


def is_active(cube, row, col, depth, dimmensions):
    size, height, width = dimmensions

    friends = get_friends(cube, row, col, depth, dimmensions)

    if (row < 0 or row >= height or col < 0 or col >= width or depth >= size or
            cube[depth][row][col] == 0):
        return friends == 3
    return (cube[depth][row][col] == 1 and friends in [2, 3])


assert is_active([test_case], 1, 0, 0, test_dimmensions) is True


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
