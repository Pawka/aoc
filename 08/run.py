from collections import namedtuple, deque


def read(filename):
    data = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data


Op = namedtuple('Op', 'op a')


class CPU():
    def __init__(self):
        self.memory = []
        self.orig_memory = []
        self.pc = 0
        self.last_pc = 0
        self.acc = 0
        self.ops = {
            'acc': self._acc,
            'jmp': self._jmp,
            'nop': self._nop,
        }

    def load_memory(self, lines):
        self.memory = []
        for line in lines:
            op, value = line.split(' ')
            self.memory.append(Op(op, int(value)))
        self.orig_memory = self.memory.copy()

    def run(self):
        self.pc = 0
        seen = set()
        while True:
            if self.pc in seen:
                return self.acc
            seen.add(self.pc)
            op = self.memory[self.pc]
            self.ops[op.op](op.a)

    def run2(self):
        self.pc = 0
        seen = set()
        first_run = True
        broken_candidates = deque()

        def fix_op(pc):
            op = self.memory[pc]
            new_operation = 'jmp'
            if op.op == 'jmp':
                new_operation = 'nop'
            new_op = Op(new_operation, a=op.a)
            self.memory[pc] = new_op

        while self.pc < len(self.memory):
            if self.pc in seen:
                first_run = False
                # reset
                seen = set()
                self.memory = self.orig_memory.copy()
                self.acc = 0
                self.pc = 0
                fix_op(broken_candidates.pop())
                continue

            seen.add(self.pc)
            op = self.memory[self.pc]
            if first_run and op.op in ['nop', 'jmp']:
                broken_candidates.append(self.pc)

            self.ops[op.op](op.a)
        return self.acc

    def _acc(self, a):
        self.acc += a
        self.pc += 1

    def _jmp(self, a):
        self.pc += a

    def _nop(self, a):
        self.pc += 1


def solve(lines):
    cpu = CPU()
    cpu.load_memory(lines)
    return cpu.run()


def solve2(lines):
    cpu = CPU()
    cpu.load_memory(lines)
    return cpu.run2()


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    data = read('input.txt')
    print(solve2(data))
