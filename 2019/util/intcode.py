class Intcode():
    ram = []
    ops = {}
    pc = 0

    # Run program while True
    run = True

    def __init__(self):
        self.ops = {
            1: self._add,
            2: self._mul,
            99: self._end
        }

    def load(self, filename):
        with open(filename) as reader:
            self.ram = [int(num) for num in reader.read().rstrip().split(',')]

    def reset(self):
        self.pc = 0
        self.run = True

    def run(self):
        self.reset()
        while self.run:
            self._eval(self.pc)

    def _eval(self, pc):
        """Evaluate opcode at program counter (pc)."""
        opcode = self.ram[pc]
        if opcode not in self.ops:
            raise Exception("Opcode %d is not supported" % opcode)
        self.ops[opcode]()

    def _add(self):
        a = self.ram[self.ram[self.pc+1]]
        b = self.ram[self.ram[self.pc+2]]
        self.ram[self.ram[self.pc+3]] = a + b
        self.pc += 4

    def _mul(self):
        a = self.ram[self.ram[self.pc+1]]
        b = self.ram[self.ram[self.pc+2]]
        self.ram[self.ram[self.pc+3]] = a * b
        self.pc += 4

    def _end(self):
        self.run = False
        self.pc += 1
