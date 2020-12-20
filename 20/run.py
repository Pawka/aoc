import re
import math
import numpy as np

from pprint import pprint


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


from collections import Counter, defaultdict


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
            edges[reverse[k].pop()] += 1

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
    pprint(conns)

    # Build picture
    size = int(math.sqrt(len(nodes)))
    picture = [[0 for x in range(size)] for y in range(size)]
    pprint(lefts)
    for row in range(1):
        for col in range(size):
            print("(%d,%d)" % (row, col))
            if row == 0 and col == 0:
                picture[0][0] = nmap[corners[1]]
                print("(0,0): %d" % picture[0][0].number)
                while (picture[0][0].right() not in lefts
                        or picture[0][0].bottom() not in tops):
                    picture[0][0].rotate()
            elif col > 0:
                left = picture[row][col-1]
                refs = conns[left.right()]
                print("Refs:", refs, "right:", left.right())
                refs.remove(left.number)
                key = refs.pop()
                found = nmap[key]
                while (left.right() != found.left()):
                    found.rotate()
                picture[row][col] = found
            # elif col == 0 and row > 0:
            #     top = picture[row-1][col]
            #     refs = conns[top.bottom()]
            #     refs.remove(top.number)
            #     key = refs.pop()
            #     picture[row][col] = nmap[key]
            #     while (picture[row][col].top() != top.bottom()):
            #         picture[row][col].rotate()



    return result




if __name__ == "__main__":
    nodes = read('input.txt')
    print(solve(nodes))
