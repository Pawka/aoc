
def read(name):
    data = []
    with open(name) as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data


def solve(data, calc):
    total = 0
    for line in data:
        res = calc(line)
        total += res
    return total


def exec_op(a, b, op):
    if op == "+":
        return a + b
    if op == "*":
        return a * b


def is_op(token):
    return token in "+*"


def tokenize(data):
    result = []
    for char in data:
        if char == ' ':
            continue
        if char.isnumeric():
            char = int(char)
        result.append(char)

    return result


assert tokenize("1 + 1") == [1, '+', 1]
assert tokenize("1 + ((1 * 3))") == [1, '+', '(', '(', 1, '*', 3, ')', ')']

def calc(data):
    tokens = tokenize(data)
    ops = []
    numbers = []
    for token in tokens:
        if type(token) == int:
            numbers.append(token)
            while len(ops) and is_op(ops[-1]):
                op = ops.pop()
                a = numbers.pop()
                b = numbers.pop()
                numbers.append(exec_op(a, b, op))
        elif is_op(token) or token == '(':
            ops.append(token)
        elif token == ')':
            if ops[-1] == '(':
                ops.pop()
            while len(ops) and is_op(ops[-1]):
                op = ops.pop()
                a = numbers.pop()
                b = numbers.pop()
                numbers.append(exec_op(a, b, op))

    return numbers.pop()


assert calc("1 + 2 * 3 + 4 * 5 + 6") == 71
assert calc("1 + (2 * 3)") == 7
assert calc("1 + (2 * 3) + (4 * (5 + 6))") == 51


PRIORITIES = {
    "(": 3,
    "*": 1,
    "+": 2,
}


def calc2(data):
    tokens = tokenize(data)
    ops = []
    numbers = []
    # n 1 1
    # o +
    for token in tokens:
        if type(token) == int:
            numbers.append(token)
        elif token == '(':
            ops.append(token)
        elif is_op(token):
            if (len(ops) and is_op(ops[-1])
                    and len(numbers) > 1
                    and PRIORITIES[token] <= PRIORITIES[ops[-1]]):
                op = ops.pop()
                a = numbers.pop()
                b = numbers.pop()
                numbers.append(exec_op(a, b, op))
            ops.append(token)
        elif token == ')':
            while ops[-1] != '(':
                op = ops.pop()
                a = numbers.pop()
                b = numbers.pop()
                # print(numbers, ops)
                numbers.append(exec_op(a, b, op))
            op = ops.pop()
    while len(ops) and is_op(ops[-1]):
        op = ops.pop()
        a = numbers.pop()
        b = numbers.pop()
        numbers.append(exec_op(a, b, op))
    return numbers.pop()


assert calc2("1 + 2 * 3 + 4 * 5 + 6") == 231
assert calc2("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert calc2("2 * 3 + (4 * 5)") == 46
assert calc2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data, calc))
    print(solve(data, calc2))
