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


if __name__ == "__main__":
    data = []
    with open('data.txt', 'r') as reader:
        for line in reader.readlines():
            data.append(int(line))
    data = sorted(data)

    target = 2020
    print(find(target, data))
