from collections import namedtuple
from os import path
from typing import List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return fh.readlines()


class Tile:

    @classmethod
    def from_raw_lines(cls, lines: List[str]) -> "Tile":
        trees = [
            [char == '#' for char in line.strip()]
            for line in lines
        ]
        return cls(trees)

    def __init__(self, trees: List[List[bool]]) -> None:
        self.trees = trees
        self.height = len(self.trees)
        self.width = len(self.trees[0])


Position = namedtuple('Position', ['x', 'y'])


class Map:

    def __init__(self, tile: Tile) -> None:
        self.tile = tile
        self.pos = Position(0, 0)

    def step(self, x, y) -> None:
        new_pos = Position(self.pos.x + x, self.pos.y + y)
        if new_pos.y >= self.tile.height:
            raise ValueError('stepped out')
        self.pos = new_pos

    def pos_has_tree(self) -> bool:
        tile_pos = Position(self.pos.x % self.tile.width, self.pos.y)
        return self.tile.trees[tile_pos.y][tile_pos.x]


def solve(step_x, step_y) -> int:
    map_ = Map(Tile.from_raw_lines(get_input()))
    tree_count = 0
    while True:
        try:
            map_.step(step_x, step_y)
            tree_count += 1 if map_.pos_has_tree() else 0
        except ValueError:
            return tree_count


if __name__ == '__main__':
    solution_part1 = solve(3, 1)
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve(1, 1) * solve(3, 1) * solve(5, 1) * solve(7, 1) * solve(1, 2)
    print(f'solution part 2: {solution_part2}')
