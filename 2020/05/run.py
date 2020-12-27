def read(filename):
    data = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data


def seat_number(code):
    row = int(code[:7].replace('B', '1').replace('F', '0'), 2)
    col = int(code[7:].replace('R', '1').replace('L', '0'), 2)
    return row * 8 + col


assert seat_number('BFFFBBFRRR') == 567
assert seat_number('FFFBBBFRRR') == 119


def solve(lines):
    return max([seat_number(seat) for seat in lines])


def solve2(lines):
    highest = solve(lines)
    all_seats = ([seat_number(seat) for seat in lines])
    last_missing = 0
    for i in range(1, highest):
        if i not in all_seats:
            if abs(i - last_missing) <= 1:
                last_missing = i
                continue
            return i


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
