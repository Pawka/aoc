from itertools import permutations
from util import Intcode


def signal(seq, datafile):
    inpt = 0
    for value in seq:
        cpu = Intcode()
        cpu.load(datafile)
        cpu.stdin(value)
        cpu.stdin(inpt)
        result = cpu.run()
        inpt = result.pop()
    return inpt


if __name__ == "__main__":
    # assert 43210 == value([4, 3, 2, 1, 0],  "data/day07.1.txt")
    # assert 54321 == value([0, 1, 2, 3, 4],  "data/day07.2.txt")
    # assert 65210 == value([1, 0, 4, 3, 2],  "data/day07.3.txt")

    max_val = 0
    for seq in permutations(range(5)):
        val = signal(seq, "data/day07.txt")
        if val > max_val:
            max_val = val
    print(max_val)
