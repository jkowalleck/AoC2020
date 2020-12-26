from enum import Enum, auto
from os import path
from typing import List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return fh.read().splitlines()


class Direction(Enum):
    North = 0
    East = 90
    South = 180
    West = 270


class Position:
    def __init__(self, pos_east: int, pos_north: int, direction: Direction):
        self.pos_east = pos_east
        self.pos_north = pos_north
        self.direction = direction

    def __str__(self) -> str:
        longitude = f'{"west" if self.pos_east < 0 else "east"} {abs(self.pos_east)}'
        latitude = f'{"south" if self.pos_north < 0 else "north"} {abs(self.pos_north)}'
        return f'{longitude} {latitude} - direction: {self.direction.name}'

    def move_north(self, value: int):
        self.pos_north += value

    def move_east(self, value: int):
        self.pos_east += value

    def move_south(self, value: int):
        self.pos_north -= value

    def move_west(self, value: int):
        self.pos_east -= value

    def rotate_right(self, value: int):
        deg = (self.direction.value + value) % 360
        self.direction = Direction(deg)

    def rotate_left(self, value: int):
        deg = (self.direction.value - value) % 360
        self.direction = Direction(360 - deg if deg < 0 else deg)

    _MOVE_FORWARD_DIRECTIONS = {
            Direction.North: move_north,
            Direction.East: move_east,
            Direction.South: move_south,
            Direction.West: move_west,
        }

    def move_forward(self, value: int):
        self._MOVE_FORWARD_DIRECTIONS[self.direction](self, value)

    def manhattan_distance(self) -> int:
        return abs(self.pos_north) + abs(self.pos_east)


_INSTRUCTIONS = {
    'F': Position.move_forward,
    'N': Position.move_north,
    'E': Position.move_east,
    'S': Position.move_south,
    'W': Position.move_west,
    'R': Position.rotate_right,
    'L': Position.rotate_left,
}


def solve() -> int:
    ship = Position(0, 0, Direction.East)
    for line in get_input():
        action, value = line[0], int(line[1:])
        _INSTRUCTIONS[action](ship, value)
    return ship.manhattan_distance()


if __name__ == '__main__':
    solution_part1 = solve()
    print(f'solution part 1: {solution_part1}')
    #solution_part2 = solve()
    #print(f'solution part 2: {solution_part2}')
