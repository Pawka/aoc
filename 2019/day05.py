from util import Intcode


if __name__ == "__main__":
    cpu = Intcode()
    cpu.load("data/day05.txt")
    cpu.stdin(1)
    cpu.run()
