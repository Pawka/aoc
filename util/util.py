def read(filename):
    data = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data
