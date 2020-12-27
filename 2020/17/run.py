from pprint import pprint
from collections import namedtuple

Dimmensions = namedtuple('Dimmensions', 'time size height width')


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
        dimm = Dimmensions(1, len(cube), len(cube[0]), len(cube[0][0]))

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

    return cube_sum(cube)


def cube_sum(cube):
    total_cubes = sum([val for sublist in cube[0] for val in sublist])
    total_cubes += 2 * sum([val for z in cube[1:] for r in z for val in r])
    return total_cubes


def solve2(data):
    hcube = [[data]]
    for _ in range(6):
        dimm = Dimmensions(
                len(hcube),
                len(hcube[0]),
                len(hcube[0][0]),
                len(hcube[0][0][0]))
        new_hcube = []
        for time in range(0, dimm.time+1):
            new_cube = []
            for depth in range(0, dimm.size+1):
                new_row = []
                for row in range(-1, dimm.height+1):
                    new_col = []
                    for col in range(-1, dimm.width+1):
                        active = is_hactive(hcube, row, col, depth, time, dimm)
                        new_col.append(int(active))
                    new_row.append(new_col)
                new_cube.append(new_row)
            new_hcube.append(new_cube)
        hcube = new_hcube

    total_cubes = 0
    for k, cube in enumerate(hcube):
        multiplier = 1
        if k > 0:
            multiplier = 2
        total_cubes += multiplier * cube_sum(cube)

    return total_cubes


def get_hfriends(hcube, row, col, depth, time, dimm):
    count = 0
    for t in range(time-1, 1+min(time+1, dimm.time-1)):
        t_tocheck = t
        if t < 0:
            if dimm.time == 1:
                continue
            t_tocheck = min(1, dimm.time-1)

        inclusive = not t == time
        friends = get_friends(
                hcube[t_tocheck], row, col, depth, dimm, inclusive)
        count += friends
    return count


def get_friends(cube, row, col, depth, dimm, inc=False):
    count = 0
    for z in range(depth-1, 1+min(depth+1, dimm.size-1)):
        z_tocheck = z
        if z < 0:
            if dimm.size == 1:
                continue
            z_tocheck = min(1, dimm.size-1)

        inclusive = inc or not z == depth
        count += get_flat_friends(
                cube[z_tocheck], row, col, dimm, inclusive)
    return count


def get_flat_friends(matrix, row, col, dimm, inclusive=False):
    count = 0
    for i in range(max(0, row-1), 1+min(dimm.height-1, row+1)):
        for j in range(max(0, col-1), 1+min(dimm.width-1, col+1)):
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
test_dimmensions = Dimmensions(1, 1, 3, 3)
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
assert get_friends(
        [test_case, test_case], 1, 1, 0, Dimmensions(1, 2, 3, 3)) == 15
assert get_friends(
        [test_case, test_case], 1, 1, 1, Dimmensions(1, 2, 3, 3)) == 10

assert get_hfriends(
        [[test_case, test_case]], 1, 1, 1, 1, Dimmensions(1, 2, 3, 3)) == 10
test_hcube = [
    [
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
    ],
    [
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    ],
]
assert get_hfriends(test_hcube, 1, 1, 0, 0, Dimmensions(2, 2, 3, 3)) == 56
test_hcube2 = [
    [
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ],
    [
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ],
]
assert get_hfriends(test_hcube2, 1, 1, 0, 0, Dimmensions(2, 2, 3, 3)) == 2


def is_active(cube, row, col, depth, dimm):
    friends = get_friends(cube, row, col, depth, dimm)
    if (row < 0 or row >= dimm.height or col < 0 or col >= dimm.width
            or depth >= dimm.size
            or cube[depth][row][col] == 0):
        return friends == 3
    return (cube[depth][row][col] == 1 and friends in [2, 3])


assert is_active([test_case], 1, 0, 0, test_dimmensions) is True


def is_hactive(hcube, row, col, depth, time, dimm):
    friends = get_hfriends(hcube, row, col, depth, time, dimm)
    if (row < 0 or row >= dimm.height
            or col < 0 or col >= dimm.width
            or depth < 0 or depth >= dimm.size
            or time >= dimm.time
            or hcube[time][depth][row][col] == 0):
        return friends == 3
    return (hcube[time][depth][row][col] == 1 and friends in [2, 3])


assert is_hactive([[test_case]], 1, 0, 0, 0, test_dimmensions) is True
assert is_hactive(test_hcube2, 1, 1, 0, 0, Dimmensions(2, 2, 3, 3)) is True

if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
