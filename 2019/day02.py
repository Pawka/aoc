from util import Intcode


if __name__ == "__main__":

    def init(noun=12, verb=2):
        cpu = Intcode()
        cpu.load("data/day02.txt")
        cpu.ram[1] = noun
        cpu.ram[2] = verb
        return cpu
    cpu = init()
    cpu.run()
    print(cpu.ram[0])

    for noun in range(100):
        for verb in range(100):
            cpu2 = init(noun, verb)
            cpu2.run()
            if cpu2.ram[0] == 19690720:
                print(100 * noun + verb)
