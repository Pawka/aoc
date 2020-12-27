from pprint import pprint
from collections import defaultdict

def read(name):
    with open(name) as reader:
        return reader.read().strip().split("\n")

def solve(lines):
    words = []
    alergens = []
    for line in lines:
        words.append(set(line.split('(')[0].strip().split(' ')))
        alergens.append(
            line.split('(contains ')[1].replace(')', '').split(', '))

    alergens_positions = defaultdict(list)
    for k, items in enumerate(alergens):
        for alergen in items:
            alergens_positions[alergen].append(k)

    known = find_possible_alergens(words, alergens_positions)

    total = 0
    al = set(known.values())
    for reciepe in words:
        total += len(reciepe.difference(al))

    order = sorted(known.keys())
    names = []
    for k in order:
        names.append(known[k])
    return total, ','.join(names)


def find_possible_alergens(words, positions):
    candidates = defaultdict(list)
    for alergen in positions:
        intersection = words[positions[alergen][0]]
        for pos in positions[alergen]:
            reciepe = words[pos]
            intersection = intersection.intersection(reciepe)
        candidates[alergen] = list(intersection)

    reverse = defaultdict(list)
    for k in candidates:
        for word in candidates[k]:
            reverse[word].append(k)

    known = defaultdict(str)
    for alergen in candidates:
        if len(candidates[alergen]) == 1:
            known[alergen] = candidates[alergen][0]
    for word in reverse:
        if len(reverse[word]) == 1:
            known[reverse[word][0]] = word

    while len(known) < len(candidates):
        for alergen in candidates:
            if alergen not in known:
                c = set(candidates[alergen])
                result = c.difference(set(known.values()))
                if len(result) == 1:
                    known[alergen] = result.pop()
    return known









if __name__ == "__main__":
    lines = read('input.txt')
    print(solve(lines))
