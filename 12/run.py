import collections


def read(filename):
    with open(filename, 'r') as reader:
        return [line.strip() for line in reader.readlines()]


def solve(lines):
    vertical = 0
    horizontal = 0
    face = 'E'

    for l in lines:
        code, value = l[0], int(l[1:])
        if code in "ESWN":
            horizontal, vertical = new_coordinates(
                    horizontal, vertical, code, value)
        elif code == "L" or code == "R":
            face = set_face(face, l)
        elif code == "F":
            horizontal, vertical = new_coordinates(
                    horizontal, vertical, face, value)

    return abs(vertical) + abs(horizontal)


def new_coordinates(horizontal, vertical, code, value):
    if code == "E":
        horizontal += value
    elif code == "W":
        horizontal -= value
    elif code == "N":
        vertical += value
    elif code == "S":
        vertical -= value
    return (horizontal, vertical)


def set_face(current, code):
    shift = int(code[1:])/90
    shift %= 4
    if code[0] == "L":
        shift *= -1
    seq = "ESWN"
    now = int(seq.find(current))
    return seq[(now+int(shift)) % 4]


assert set_face("E", "R90") == "S"
assert set_face("E", "R180") == "W"
assert set_face("E", "R270") == "N"
assert set_face("E", "R360") == "E"
assert set_face("E", "R450") == "S"
assert set_face("W", "R90") == "N"
assert set_face("W", "L90") == "S"
assert set_face("N", "R90") == "E"

Point = collections.namedtuple('Point', 'x y')


def solve2(lines):
    waypoint = Point(10, 1)
    ship = Point(0, 0)

    for l in lines:
        code, value = l[0], int(l[1:])
        if code in "ESWN":
            x, y = new_coordinates(
                    waypoint.x, waypoint.y, code, value)
            waypoint = Point(x, y)

        elif code == "L" or code == "R":
            waypoint = rotate_waypoint(waypoint, code, value)
        elif code == "F":
            x = ship.x + waypoint.x * value
            y = ship.y + waypoint.y * value
            ship = Point(x, y)

    return abs(ship.x) + abs(ship.y)


def rotate_waypoint(point, code, value):
    times = int(value/90)
    x, y = point.x, point.y
    for i in range(times):
        if code == "R":
            x, y = y, x * -1
        elif code == "L":
            x, y = y * -1, x
    return Point(x, y)


assert rotate_waypoint(Point(1, 5), "R", 90) == Point(5, -1)
assert rotate_waypoint(Point(1, 5), "R", 180) == Point(-1, -5)
assert rotate_waypoint(Point(1, 5), "R", 270) == Point(-5, 1)
assert rotate_waypoint(Point(1, 5), "R", 360) == Point(1, 5)
assert rotate_waypoint(Point(1, 5), "L", 270) == Point(5, -1)


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
