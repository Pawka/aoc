def find(target, data):
    size = len(data)
    for i in range(size):
        j = size-1

        while j > i:
            s = data[i] + data[j]
            if s > target:
                j -= 1
            elif s < target:
                break
            else:
                return data[i]*data[j]


def find2(target, data):
    size = len(data)
    for i in range(size):
        j = size-1

        while j > i:
            s = data[i] + data[j]
            if s < target:
                k = i+1
                while k < j:
                    s2 = s + data[k]
                    if s2 == target:
                        return data[i] * data[j] * data[k]
                    k += 1
            j -= 1


if __name__ == "__main__":
    data = []
    with open('data.txt', 'r') as reader:
        for line in reader.readlines():
            data.append(int(line))
    data = sorted(data)

    target = 2020
    print(find(target, data))
    print(find2(target, data))
