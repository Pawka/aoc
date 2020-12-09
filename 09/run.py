import array

LENGTH = 25


def read(filename):
    data = array.array('Q')
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(int(line))
    return data


def solve(numbers):
    preamble = array.array('Q', numbers[:LENGTH])
    for number in numbers[LENGTH:]:
        if find_sum(preamble, number) is False:
            return number
        preamble.pop(0)
        preamble.append(number)


def find_sum(preamble, number):
    for i in range(0, LENGTH-1):
        for j in range(i, LENGTH):
            if number == preamble[i] + preamble[j]:
                return True
    return False


def solve2(numbers, target):
    for i in range(0, len(numbers)-1):
        for j in range(i+2, len(numbers)):
            preamble = numbers[i:j]
            if sum(preamble) == target:
                return min(preamble) + max(preamble)
            elif sum(preamble) > target:
                break


if __name__ == "__main__":
    numbers = read('input.txt')
    invalid_number = solve(numbers)

    print(invalid_number)
    print(solve2(numbers, invalid_number))
