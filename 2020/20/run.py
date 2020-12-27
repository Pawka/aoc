import re
import math
import numpy as np

from pprint import pprint
from collections import defaultdict


def read(name):
    result = []
    with open(name) as reader:
        doc = reader.read().strip()
        for line in doc.split("\n\n"):
            n = Node(line.strip().split("\n"))
            result.append(n)
    return result


class Node():
    def __init__(self, lines):
        self.matrix = []
        self.number = int(re.match(r'Tile (\d+):', lines[0]).group(1))
        for line in lines[1:]:
            self.matrix.append(
                    [x for x in line.replace(".", "0").replace("#", "1")])
        self.matrix = np.transpose(self.matrix)

    def flip(self):
        self.matrix = np.transpose(self.matrix)

    def rotate(self):
        self.matrix = np.rot90(self.matrix)

    def top(self):
        return int(''.join(self.matrix[0]), 2)

    def bottom(self):
        return int(''.join(self.matrix[-1]), 2)

    def left(self):
        return int(''.join(
            [self.matrix[j][0] for j in range(len(self.matrix))]), 2)

    def right(self):
        return int(''.join(
            [self.matrix[j][-1] for j in range(len(self.matrix))]), 2)




def solve(nodes):
    reverse = defaultdict(set)
    nmap = {}
    lefts = defaultdict(set)
    tops = defaultdict(set)
    for n in nodes:
        nmap[n.number] = n
        for i in range(4):
            key = n.number
            n.rotate()
            reverse[n.top()].add(key)
            reverse[n.right()].add(key)
            reverse[n.bottom()].add(key)
            reverse[n.left()].add(key)
            lefts[n.left()].add(key)
            tops[n.top()].add(key)

    edges = defaultdict(int)
    for k in reverse:
        if len(reverse[k]) == 1:
            edges[list(reverse[k])[0]] += 1

    result = 1
    corners = []
    sides = []
    for k in edges:
        if edges[k] == 4:
            result *= k
            corners.append(k)
        else:
            sides.append(k)

    conns = {}
    for k in reverse:
        if len(reverse[k]) > 1:
            conns[k] = reverse[k]

    # Build picture
    size = int(math.sqrt(len(nodes)))
    picture = [[0 for x in range(size)] for y in range(size)]
    for row in range(size):
        for col in range(size):
            if row == 0 and col == 0:
                picture[0][0] = nmap[corners[0]]
                while (picture[0][0].right() not in conns
                        or picture[0][0].bottom() not in conns):
                    picture[0][0].rotate()
            elif col > 0:
                left = picture[row][col-1]
                refs = conns[left.right()]
                refs.remove(left.number)
                key = refs.pop()
                found = configure(nmap[key], left=left.right())
                picture[row][col] = found
            elif col == 0 and row > 0:
                top = picture[row-1][col]
                refs = conns[top.bottom()]
                refs.remove(top.number)
                key = refs.pop()
                found = configure(nmap[key], top=top.bottom())
                picture[row][col] = found

    joined = join_picture(picture)
    solution2 = mark_monsters(joined)
    return result, solution2


def join_picture(picture):
    size = len(picture)
    joined = [[0 for x in range(size)] for y in range(size)]

    for row in range(size):
        for col in range(size):
            m = picture[row][col].matrix
            msize = len(m)
            newm = []
            for i in range(1, msize-1):
                newm.append(''.join(m[i][1:-1]))
            joined[row][col] = newm

    merged = []
    for row in range(size):
        for irow in range(len(joined[0][0])):
            line = ""
            for col in range(size):
                line += joined[row][col][irow]
            merged.append(line)
    return merged


def modify_picture(picture, rotate=True):
    expanded = []
    for line in picture:
        expanded.append([int(x) for x in list(line)])
    if rotate:
        expanded = np.rot90(expanded)
    else:
        expanded = np.transpose(expanded)
    joined = []
    for line in expanded:
        joined.append(''.join([str(x) for x in line]))
    return joined


def mark_monsters(picture):
    MONSTER = [
        '00000000000000000010',
        '10000110000110000111',
        '01001001001001001000'
    ]
    monster = [int(m, 2) for m in MONSTER]

    found = 0
    it = 0
    while found == 0:
        size = len(picture)
        msize = len(MONSTER[1])
        for row in range(1, size-1):
            for col in range(1, size):
                candidate = picture[row][col:col+msize]
                if int(candidate, 2) & monster[1] == monster[1]:
                    top = picture[row-1][col:col+msize]
                    bottom = picture[row+1][col:col+msize]
                    if (int(top, 2) & monster[0] == monster[0]
                            and int(bottom, 2) & monster[2] == monster[2]):
                        found += 1

        if it == 4:
            picture = modify_picture(picture, False)
        else:
            picture = modify_picture(picture)
        it += 1

    total = 0
    for line in picture:
        total += len(line.replace('0', ''))

    MONSTER_SIZE = 15  # number of "1"s in the monster.
    return total - found * MONSTER_SIZE


def configure(node, left=None, top=None):
    for j in range(2):
        for i in range(5):
            if left:
                if node.left() == left:
                    return node
            if top:
                if node.top() == top:
                    return node
            node.rotate()
        node.flip()


if __name__ == "__main__":
    nodes = read('input.txt')
    print(solve(nodes))
