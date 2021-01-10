from .intcode import Intcode, ParamMode


def test_parse_parameters():
    cpu = Intcode()
    assert ParamMode(2, {0: 0, 1: 1}) == cpu._parse_parameters(1002)
    assert ParamMode(12, {0: 1, 1: 0, 2: 1}) == cpu._parse_parameters(10112)


def test_integration():
    """Executes most previous parameters"""
    day2 = Intcode()
    day2.load("data/day02.txt")
    day2.ram[1] = 12
    day2.ram[2] = 2
    day2.run()
    assert 3716250 == day2.ram[0]

    negative_numbers = Intcode()
    negative_numbers.loadStr("1101,100,-1,4,0")
    negative_numbers.run()
    assert 99 == negative_numbers.ram[4]
