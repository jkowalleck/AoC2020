from itertools import permutations
from os import path
from typing import Iterable, List, Tuple

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return fh.read().splitlines()


def is_valid(sum_: int, numbers: Iterable[int]) -> bool:
    return any(sum(pair) == sum_ for pair in permutations(numbers, 2))


def first_invalid(numbers: List[int], preamble: int = 25) -> Tuple[int, int]:
    offset = preamble
    while is_valid(numbers[offset], numbers[offset - preamble:offset]):
        offset += 1
    return numbers[offset], offset


def continuous_set(sum_: int, numbers: List[int]) -> List[int]:
    numbers_len = len(numbers)
    for offset in range(numbers_len):
        for length in range(numbers_len - offset):
            addends = numbers[offset:offset + length]
            addends_sum = sum(addends)
            if addends_sum == sum_:
                return addends
            if addends_sum >= sum_:
                break
    return []


def solve1() -> int:
    numbers = list(map(int, get_input()))
    number, _ = first_invalid(numbers)
    return number


def solve2() -> int:
    numbers = list(map(int, get_input()))
    number, offset = first_invalid(numbers)
    addends = continuous_set(number, numbers[0: offset])
    return min(addends) + max(addends)


if __name__ == '__main__':
    solution_part1 = solve1()
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve2()
    print(f'solution part 2: {solution_part2}')
