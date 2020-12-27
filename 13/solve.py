from collections import namedtuple
from os import path
from typing import List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return fh.read().splitlines()


def solve1() -> int:
    lines = get_input()
    arrival = int(lines[0])
    busses = set(map(int, filter(lambda b: b != 'x', lines[1].split(','))))
    departures = {bus - (arrival % bus): bus for bus in busses}
    min_wait = min(departures.keys())
    bus_to_take = departures[min_wait]
    return min_wait * bus_to_take


def solve2() -> int:
    lines = get_input()
    _Bus = namedtuple('_Bus', ['number', 'pos'])
    busses = [_Bus(int(bus), pos) for pos, bus in enumerate(lines[1].split(',')) if bus != 'x']

    def next_possible_time(time_: int, again_: int, bus: _Bus) -> int:
        while (time_ + bus.pos) % bus.number != 0:
            time_ += again_
        return time_

    again = 1
    time = 0
    for bus in busses:
        time = next_possible_time(time, again, bus)
        if all(0 == ((time + bus.pos) % bus.number) for bus in busses):
            return time
        again *= bus.number
    return 0


if __name__ == '__main__':
    solution_part1 = solve1()
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve2()
    print(f'solution part 2: {solution_part2}')
