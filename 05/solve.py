from os import path
from re import compile as re_compile
from typing import List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return [line.rstrip('\n') for line in fh.readlines()]


def _int_from_tree(line: str, lower: str) -> int:
    range_ = (0, 2 ** len(line) - 1)
    for char in line:
        delta_half = (range_[1] - range_[0]) // 2
        range_ = (range_[0], range_[0] + delta_half) if char == lower else (range_[1] - delta_half, range_[1])
    return range_[0]


class Seat:

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    @property
    def id(self) -> int:
        return self.row * 8 + self.col

    __LINE_RE = re_compile(r'^([FB]+)([LR]+)$')

    @classmethod
    def from_line(cls, line: str) -> "Seat":
        match = cls.__LINE_RE.match(line)
        assert match
        row, col = match.groups()
        return cls(cls.__row_from_line(row), cls.__col_from_line(col))

    @staticmethod
    def __row_from_line(line: str) -> int:
        return _int_from_tree(line, 'F')

    @staticmethod
    def __col_from_line(line: str) -> int:
        return _int_from_tree(line, 'L')


def solve1() -> int:
    seats = [Seat.from_line(line) for line in get_input()]
    return max(seat.id for seat in seats)


def solve2() -> int:
    taken_ids = set(Seat.from_line(line).id for line in get_input())
    all_ids = set(range(min(taken_ids), max(taken_ids)))
    free_ids = all_ids - taken_ids
    return list(free_ids)[0]


if __name__ == '__main__':
    solution_part1 = solve1()
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve2()
    print(f'solution part 2: {solution_part2}')
