from collections import Counter
from os import path
from re import compile as re_compile
from typing import Callable, List


class Entry:
    _LINE_FORMAT = re_compile(r'^(\d+)\-(\d+) (\w)\: (\w+)$')

    def __init__(self, line_raw: str) -> None:
        parts = self._LINE_FORMAT.match(line_raw)
        if parts is None:
            raise ValueError()
        self.a = int(parts[1])
        self.b = int(parts[2])
        self.char = str(parts[3])
        self.word = str(parts[4])


def get_input() -> List[Entry]:
    with open(path.join(path.dirname(__file__), 'input')) as input_fh:
        return list(map(Entry, input_fh.readlines()))


_SolveFilter = Callable[[Entry], bool]


def solve(filter_: _SolveFilter) -> int:
    input = get_input()
    valids = list(filter(filter_, input))
    return len(valids)


def is_valid1(line: Entry) -> bool:
    counter = Counter(line.word)
    char_count = counter.get(line.char, 0)
    return line.a <= char_count <= line.b


def is_valid2(line: Entry) -> bool:
    match_a = line.word[line.a - 1] == line.char
    match_b = line.word[line.b - 1] == line.char
    return match_a != match_b


if __name__ == '__main__':
    solution_part1 = solve(is_valid1)
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve(is_valid2)
    print(f'solution part 2: {solution_part2}')
