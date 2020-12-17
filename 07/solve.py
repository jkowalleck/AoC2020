from collections import namedtuple
from itertools import chain
from os import path
from re import compile as re_compile
from typing import List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return [line.rstrip('\n') for line in fh.readlines()]


_Colour = str

_Content = namedtuple('_Content', ['amount', 'colour'])


class Rule:

    def __init__(self, colour: _Colour, contains: List[_Content]) -> None:
        self.colour = colour
        self.contains = contains

    __BAG_RE = re_compile(r'^(.+?) bags contain(.+)$')
    __CONTAIN_RE = re_compile(r' (\d+) (.+?) bags?[,\.]')

    @classmethod
    def from_line(cls, line: str) -> "Rule":
        matches = cls.__BAG_RE.match(line)
        assert matches
        colour = matches.group(1)
        contains = [_Content(int(c_number), c_colour)
                    for c_number, c_colour
                    in cls.__CONTAIN_RE.findall(matches.group(2))]
        return cls(colour=colour, contains=contains)


def solve1(my_bag: _Colour) -> int:
    rules = {rule.colour: {contain.colour for contain in rule.contains}
             for rule
             in map(Rule.from_line, get_input())
             if rule.contains and rule.colour != my_bag}
    bags_levels = [{my_bag, }]
    while True:
        colours = {
            colour
            for colour, contain
            in rules.items()
            if bags_levels[-1] & contain}
        if not colours:
            break
        bags_levels.append(colours)
    bags = set(chain.from_iterable(bags_levels[1:]))
    return len(bags)


def solve2(my_bag: _Colour) -> int:
    rules = {rule.colour: rule.contains
             for rule
             in map(Rule.from_line, get_input())}

    def in_it(bag: _Colour) -> int:
        contains = rules[bag]
        return sum(
            number + number * in_it(colour)
            for number, colour
            in contains
        ) if contains else 0

    return in_it(my_bag)


if __name__ == '__main__':
    solution_part1 = solve1('shiny gold')
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve2('shiny gold')
    print(f'solution part 2: {solution_part2}')
