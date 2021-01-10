from collections import namedtuple, defaultdict
from enum import IntEnum

ParamMode = namedtuple('ParamMode', 'opcode params')


class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1


class Memory(list):
    def get(self, position, param=Mode.POSITION):
        """Return value from given position by param mode.

        If param is 0 then value in position is pointer to other memory place.
        If param is 1 then actual value is stored at position.
        """
        if param == Mode.IMMEDIATE:
            return self[position]
        if param == Mode.POSITION:
            return self[self[position]]


class Intcode():
    ram = Memory()
    ops = {}
    pc = 0

    # Run program while True
    run = True

    def __init__(self):
        self.ops = {
            1: self._add,
            2: self._mul,
            3: self._input,
            4: self._output,
            99: self._end
        }

    def load(self, filename):
        with open(filename) as reader:
            self.ram = Memory(map(int, reader.read().rstrip().split(',')))

    def loadStr(self, data):
        self.ram = Memory(map(int, data.split(',')))

    def reset(self):
        self.pc = 0
        self.run = True

    def run(self):
        self.reset()
        while self.run and self.pc < len(self.ram):
            self._eval(self.pc)

    def _eval(self, pc):
        """Evaluate opcode at program counter (pc)."""
        opcode = self.ram[pc]
        params = defaultdict(int)
        if opcode not in self.ops:
            pm = self._parse_parameters(opcode)
            if pm.opcode not in self.ops:
                raise Exception("Opcode %d is not supported" % opcode)
            opcode, params = pm
        self.ops[opcode](params)

    def _parse_parameters(self, code):
        """Parse parameter mode into opcode and parameters"""
        opcode = code % 100
        params = defaultdict(int)
        for k, param in enumerate(list(map(int, str(code)[-3::-1]))):
            params[k] = param
        return ParamMode(opcode, params)

    def _add(self, params):
        a = self.ram.get(self.pc+1, params[0])
        b = self.ram.get(self.pc+2, params[1])
        self.ram[self.ram[self.pc+3]] = a + b
        self.pc += 4

    def _mul(self, params):
        a = self.ram.get(self.pc+1, params[0])
        b = self.ram.get(self.pc+2, params[1])
        self.ram[self.ram[self.pc+3]] = a * b
        self.pc += 4

    def _input(self, params):
        a = int(input("$ "))
        self.ram[self.ram[self.pc+1]] = a
        self.pc += 2

    def _output(self, params):
        a = self.ram.get(self.pc+1, params[0])
        print(">", a)
        self.pc += 2

    def _end(self, params):
        self.run = False
        self.pc += 1
