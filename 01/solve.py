from functools import reduce
from itertools import permutations
from os import path
from typing import Optional, Set, Tuple


def get_input() -> Set[int]:
    with open(path.join(path.dirname(__file__), 'input')) as input_fh:
        return set(map(int, input_fh.readlines()))


def find_addends(sum_: int, addends_cnt: int) -> Optional[Tuple[int, ...]]:
    input = get_input()
    for addends in permutations(input, addends_cnt):
        if sum(addends) == sum_:
            return addends
    return None


def solve(sum: int, addends_cnt: int) -> Optional[int]:
    addends = find_addends(sum, addends_cnt)
    if addends is not None:
        return reduce(lambda a, b: a * b, addends)
    return None


if __name__ == '__main__':
    solution_part1 = solve(2020, 2)
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve(2020, 3)
    print(f'solution part 2: {solution_part2}')
