from collections import Counter


def solve(a, b, second=False):
    total1, total2 = 0, 0
    for password in range(a, b+1):
        data = str(password)
        counts = Counter(data)
        if len(counts) == len(data):
            continue
        if list(data) != sorted(data):
            continue
        total1 += 1
        if 2 in counts.values():
            total2 += 1

    return total1, total2


if __name__ == "__main__":
    print(solve(284639, 748759))
