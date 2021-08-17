import operator

from collections import namedtuple, defaultdict, deque
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
        self._stdin = deque()
        self._stdout = []
        self.ops = {
            1: self._add,
            2: self._mul,
            3: self._input,
            4: self._output,
            5: self._jump_if_true,
            6: self._jump_if_false,
            7: self._less_than,
            8: self._equal,
            99: self._end
        }

    def load(self, filename):
        with open(filename) as reader:
            self.ram = Memory(map(int, reader.read().rstrip().split(',')))

    def stdin(self, value):
        """Write value to stdin for reading.

        If value exists in stdin then opcode will read from the stdin instead
        of user input.
        """
        self._stdin.appendleft(int(value))

    def loadStr(self, data):
        self.ram = Memory(map(int, data.split(',')))

    def reset(self):
        self.pc = 0
        self.run = True

    def run(self):
        self.reset()
        while self.run and self.pc < len(self.ram):
            self._eval(self.pc)
        return self._stdout

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
        if len(self._stdin) > 0:
            a = self._stdin.pop()
        else:
            a = int(input("$ "))
        self.ram[self.ram[self.pc+1]] = a
        self.pc += 2

    def _output(self, params):
        a = self.ram.get(self.pc+1, params[0])
        print(">", a)
        self._stdout.append(a)
        self.pc += 2

    def _jump_if_true(self, params):
        self.__op_jump_if(params, operator.ne)

    def _jump_if_false(self, params):
        self.__op_jump_if(params, operator.eq)

    def __op_jump_if(self, params, operator):
        a = self.ram.get(self.pc+1, params[0])
        if operator(a, 0):
            self.pc = self.ram.get(self.pc+2, params[1])
            return
        self.pc += 3

    def _less_than(self, params):
        self.__op_compare(params, operator.lt)

    def _equal(self, params):
        self.__op_compare(params, operator.eq)

    def __op_compare(self, params, op):
        a = self.ram.get(self.pc+1, params[0])
        b = self.ram.get(self.pc+2, params[1])
        value = 0
        if op(a, b):
            value = 1
        self.ram[self.ram[self.pc+3]] = value
        self.pc += 4

    def _end(self, params):
        self.run = False
        self.pc += 1
