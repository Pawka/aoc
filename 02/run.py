def read(name):
    data = []
    with open('data.txt', 'r') as reader:
        for line in reader.readlines():
            data.append(line)
    return data



def solve(data):
    valid = 0
    for line in data:
        parts = line.split()
        min_count = int(parts[0].split('-')[0])
        max_count = int(parts[0].split('-')[1])
        letter = parts[1][0]
        password = parts[2]

        count = 0
        for l in password:
            if l == letter:
                count += 1

        if count >= min_count and count <= max_count:
            valid += 1

    return valid


def solve2(data):
    valid = 0
    for line in data:
        parts = line.split()
        pos1 = int(parts[0].split('-')[0])-1
        pos2 = int(parts[0].split('-')[1])-1
        letter = parts[1][0]
        password = parts[2]

        if (password[pos1] == letter and password[pos2] != letter or
                password[pos1] != letter and password[pos2] == letter):
            valid += 1

    return valid


if __name__ == "__main__":
    lines = read('data.txt')
    print(solve(lines))
    print(solve2(lines))
