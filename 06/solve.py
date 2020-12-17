from os import path
from typing import List, Callable, Set, Optional

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return [line.rstrip('\n') for line in fh.readlines()]


_Answers = Set[str]
_AnswerOperation = Callable[[_Answers, _Answers], _Answers]


def from_raw_lines(lines: List[str], op: _AnswerOperation) -> List[_Answers]:
    groups = []
    group_answers: Optional[_Answers] = None
    line_index_max = len(lines) - 1
    for line_index, line in enumerate(lines):
        if line == '':
            if group_answers is not None:
                groups.append(group_answers)
            group_answers = None
            continue
        group_answers = op(group_answers, set(line)) if group_answers is not None else set(line)
        if line_index == line_index_max:
            groups.append(group_answers)
    return groups


def solve(op: _AnswerOperation) -> int:
    groups = from_raw_lines(get_input(), op)
    return sum(len(group) for group in groups)


if __name__ == '__main__':
    solution_part1 = solve(set.__or__)
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve(set.__and__)
    print(f'solution part 2: {solution_part2}')
