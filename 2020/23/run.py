class Item:
    val = 0
    next = None

    def __init__(self, val, next):
        self.val = val
        self.next = next


def solve(data):
    values = [int(x) for x in list(data)]

    values_map = {}
    current = None
    last = None
    for val in reversed(values):
        item = Item(val, None)
        values_map[val] = item
        if current is not None:
            item.next = current
        if last is None:
            last = item
        current = item
    last.next = current
    playgame(current, values_map)
    return result(values_map[1], '')[1:]


def playgame(it, values_map, n=100):
    current = it
    destination = None
    max_val = max(values_map.keys())
    for i in range(n):
        pickup = current.next
        pickup_val = set()
        for _ in range(3):
            pickup_val.add(current.next.val)
            current.next = current.next.next
        dest_val = current.val - 1
        while dest_val == 0 or dest_val in pickup_val:
            dest_val -= 1
            if dest_val < 1:
                dest_val = max_val
        destination = values_map[dest_val]
        current.next = pickup.next.next.next
        pickup.next.next.next = destination.next
        destination.next = pickup
        current = current.next


def solve2(data):
    values = [int(x) for x in list(data)]

    values_map = {}
    current = None
    last = None
    for val in reversed(values):
        item = Item(val, None)
        values_map[val] = item
        if current is not None:
            item.next = current
        if last is None:
            last = item
        current = item

    size = 1000000
    loops = 10000000
    max_val = max(values_map.keys())
    # size = 20
    # loops = 10
    for i in range(max_val, size):
        new = Item(i+1, None)
        last.next = new
        last = last.next
        values_map[i+1] = new
    last.next = current
    playgame(current, values_map, loops)

    first = values_map[1]
    print(
            first.next.val,
            first.next.next.val,
            first.next.val * first.next.next.val)


def result(current, separator=','):
    it = current
    values = []
    first = it
    while it.next != first:
        values.append(it.val)
        it = it.next
    values.append(it.val)
    return (separator.join([str(x) for x in values]))


if __name__ == "__main__":
    data = "624397158"
    data2 = "389125467"
    res1 = solve(data)
    print(res1)
    assert res1 == "74698532"
    solve2(data)
