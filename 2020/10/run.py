def read(filename):
    with open(filename, 'r') as reader:
        return sorted([int(line) for line in reader.readlines()])


def solve(adapters):
    diffs = {
        1: 0,
        2: 0,
        3: 1,
    }
    jolts = 0
    for i in adapters:
        diff = i-jolts
        diffs[diff] += 1
        jolts += diff

    return (diffs[1] * diffs[3], jolts)


def solve2(adapters, target):
    adapters.extend([0, target])
    adapters.sort()
    paths = {}
    for i in range(len(adapters)):
        paths[adapters[i]] = [
            x for x in adapters[i+1:i+4] if x - adapters[i] <= 3]

    results = {target: 1}
    rev = sorted(adapters, reverse=True)
    for i in rev[1:]:
        total = 0
        for n in paths[i]:
            total += results[n]
        results[i] = total
    return results[0]


if __name__ == "__main__":
    data = read('input.txt')
    result1, jolts = solve(data)
    print(result1)
    print(solve2(data, jolts+3))
