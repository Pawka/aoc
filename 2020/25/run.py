def solve():
    card_key = 13316116
    door_key = 13651422
    card_loops = find_loops(card_key)
    return pub_key(door_key, card_loops)


def find_loops(key):
    res = 1
    loops = 1
    while True:
        res = (res * 7) % 20201227
        if res == key:
            return loops
        loops += 1


def pub_key(number, loops):
    res = 1
    for _ in range(loops):
        res = (res * number) % 20201227
    return res


if __name__ == "__main__":
    print(solve())
