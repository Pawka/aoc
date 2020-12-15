import math


def read(name):
    with open(name) as reader:
        return [l.strip() for l in reader.readlines()]


def parse(data):
    result = []
    for line in data:
        if line[:3] == "mas":
            result.append(line.split(" ")[-1])
        elif line[:3] == "mem":
            pos = int(line[4:].split("]")[0])
            val = int(line.split(" ")[-1])
            result.append((pos, val))
    return result


def solve(data):
    mem = {}
    masks = None
    for line in data:
        if type(line) == str:
            masks = (
                int(line.replace('X', '0'), 2),
                int(line.replace('X', '1'), 2),
            )
        else:
            pos, value = line
            value |= masks[0]
            value &= masks[1]
            mem[pos] = value

    return sum(mem.values())


from pprint import pprint


def solve2(data):
    mem = {}
    mask = ""
    for line in data:
        if type(line) == str:
            mask = line
        else:
            pos, value = line
            addresses = get_addr(mask)
            for addr in addresses:
                m = mask.replace('0', '1').replace('X', '0')
                a = pos & int(m, 2)
                a |= int(addr, 2)
                mem[a] = value
    return sum(mem.values())


def get_addr(mask):
    result = []
    sp = list(mask)
    positions = []
    for k, v in enumerate(sp):
        if v == 'X':
            positions.append(k)

    i = 0
    fmt = "0" + str(len(positions)) + "b"
    while i < math.pow(2, len(positions)):
        mask_copy = sp
        bw_repr = format(i, fmt)
        for k, v in enumerate(bw_repr):
            mask_copy[positions[k]] = v
        result.append("".join(mask_copy))
        i += 1
    return result


assert get_addr('111X') == ['1110', '1111']
assert get_addr('X110') == ['0110', '1110']
assert get_addr('X11X') == ['0110', '0111', '1110', '1111']
assert len(get_addr('XX1X')) == 8
assert len(get_addr('XX1XXXXXXX')) == 512

if __name__ == "__main__":
    lines = read("input.txt")
    data = parse(lines)
    print(solve(data))
    print(solve2(data))
