from itertools import groupby


def read(filename):
    data = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data


def get_groups(lines):
    groups = []
    g = []
    for line in lines:
        if line == "":
            groups.append(g)
            g = []
            continue
        g.append(line)
    groups.append(g)
    return groups


def solve(lines):
    groups = get_groups(lines)
    result = 0
    for g in groups:
        result += len(set("".join(g)))
    return result


def solve2(lines):
    groups = get_groups(lines)
    answers = []
    result = 0
    for g in groups:
        people_count = len(g)
        answers = sorted(list("".join(g)))
        freq = [len(list(group)) for key, group in groupby(answers)]
        result += sum([1 for x in freq if x == people_count])

    return result


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
