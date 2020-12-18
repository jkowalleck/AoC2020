from collections import namedtuple
from os import path
from re import compile as re_compile
from typing import List, Optional, Tuple

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return [line.rstrip('\n') for line in fh.readlines()]


_Instruction = Tuple[str, int]

MachineChange = namedtuple('MachineChange', ['inst', 'acc'])


class MachineLoop(BaseException):
    def __init__(self, accumulator: int) -> None:
        self.accumulator = accumulator


class Machine:

    def __init__(self, instructions: List[_Instruction]) -> None:
        self.instructions = instructions

    def clone(self) -> "Machine":
        return Machine(self.instructions.copy())

    __LINE_FORMAT = re_compile(r'^(\w{3}) ([+-]\d+)$')

    @classmethod
    def from_lines(cls, lines: List[str]) -> "Machine":
        machine = cls([])
        for line in lines:
            matches = cls.__LINE_FORMAT.match(line)
            assert matches
            machine.instructions.append((matches.group(1), int(matches.group(2))))
        return machine

    @staticmethod
    def _do_acc(val: int) -> MachineChange:
        return MachineChange(1, val)

    @staticmethod
    def _do_nop(_: int) -> MachineChange:
        return MachineChange(1, 0)

    @staticmethod
    def _do_jmp(val: int) -> MachineChange:
        return MachineChange(val, 0)

    def run_instructions(self) -> int:
        accumulator = 0
        last = len(self.instructions) - 1
        inst = 0
        visited = set()
        while inst <= last:
            if inst in visited:
                raise MachineLoop(accumulator)
            visited.add(inst)
            op, val = self.instructions[inst]
            change: MachineChange = getattr(self, f'_do_{op}')(val)
            inst += change.inst
            accumulator += change.acc
        return accumulator


def solve1() -> Optional[int]:
    machine = Machine.from_lines(get_input())
    try:
        machine.run_instructions()
    except MachineLoop as ex:
        return ex.accumulator
    return None


def solve2() -> Optional[int]:
    machine = Machine.from_lines(get_input())
    replace = {'jmp': 'nop', 'nop': 'jmp', }
    for inst in range(len(machine.instructions)):
        fixed = machine.clone()
        instruction = fixed.instructions[inst]
        if instruction[0] not in replace:
            continue
        fixed.instructions[inst] = (replace[instruction[0]], instruction[1])
        try:
            return fixed.run_instructions()
        except MachineLoop:
            continue
    return None


if __name__ == '__main__':
    solution_part1 = solve1()
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve2()
    print(f'solution part 2: {solution_part2}')
