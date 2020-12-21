from collections import Counter
from os import path
from typing import Generator, List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return fh.read().splitlines()


def diffs(adapters: List[int]) -> Generator[int, int, None]:
    yield adapters[0]
    for a, adapter in enumerate(adapters[1:]):
        yield adapter - adapters[a]


def solve1() -> int:
    adapters = sorted(map(int, get_input()))
    counts = Counter(diffs(adapters))
    return counts[1] * (counts[3] + 1)  # build in adapter has given diff of 3


def solve2() -> int:
    # TODO
    raise NotImplementedError()


if __name__ == '__main__':
    solution_part1 = solve1()
    print(f'solution part 1: {solution_part1}')
    #solution_part2 = solve2()
    #print(f'solution part 2: {solution_part2}')
