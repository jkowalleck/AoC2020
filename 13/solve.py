from os import path
from typing import List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return fh.read().splitlines()


def solve() -> int:
    input = get_input()
    arrival = int(input[0])
    busses = set(map(int, filter(lambda b: b != 'x', input[1].split(','))))
    departures = dict()
    for bus in busses:
        last = arrival % bus
        wait = bus - last
        departures[wait] = bus
        pass
    min_wait = min(departures.keys())
    bus_to_take = departures[min_wait]
    return min_wait * bus_to_take


if __name__ == '__main__':
    solution_part1 = solve()
    print(f'solution part 1: {solution_part1}')
    #solution_part2 = solve()
    #print(f'solution part 2: {solution_part2}')
