from collections import deque


def read(name):
    players = []
    with open(name) as reader:
        parts = reader.read().split("\n\n")
        for i in range(2):
            players.append([int(x) for x in parts[i].strip().split("\n")[1:]])
    p1 = deque()
    p2 = deque()
    p1.extendleft(players[0])
    p2.extendleft(players[1])
    return (p1, p2)


def solve(data):
    p1, p2 = data
    while len(p1) and len(p2):
        c1 = p1.pop()
        c2 = p2.pop()
        if c1 > c2:
            p1.extendleft([c1, c2])
        elif c1 < c2:
            p2.extendleft([c2, c1])

    winner = p1 if len(p1) else p2
    return result(winner)


def combat(p1, p2):
    prev_p1 = set()
    prev_p2 = set()

    while len(p1) and len(p2):
        # 1
        h1 = tuple(p1)
        h2 = tuple(p2)
        if h1 in prev_p1 or h2 in prev_p2:
            return (p1, p2, 1)
        prev_p1.add(h1)
        prev_p2.add(h2)

        # 2
        c1 = p1.pop()
        c2 = p2.pop()

        # 3
        if len(p1) >= c1 and len(p2) >= c2:
            # Recursive combat
            cp1 = deque(list(p1.copy())[-c1:])
            cp2 = deque(list(p2.copy())[-c2:])
            _, _, winner = combat(cp1, cp2)
            if winner == 1:
                p1.extendleft([c1, c2])
            else:
                p2.extendleft([c2, c1])
        else:
            if c1 > c2:
                p1.extendleft([c1, c2])
            elif c1 < c2:
                p2.extendleft([c2, c1])

    # game = "%d.1" % depth
    # print("Game %s: " % game, depth, len(p1), len(p2), p1, p2)
    winner = 1 if len(p1) > 0 else 2
    return (p1, p2, winner)


def solve2(data):
    p1, p2 = data
    r1, r2, winner = combat(p1, p2)
    winner = r1 if winner == 1 else r2
    return result(winner)


def result(winner):
    result = 0
    for i in range(len(winner)):
        top = winner.popleft()
        result += (i+1) * top
    return result


if __name__ == "__main__":
    data = read('input.txt')
    # print(solve(data))
    print(solve2(data))
