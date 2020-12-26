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
    def __init__(self, pos_east: int, pos_north: int) -> None:
        self.pos_east = pos_east
        self.pos_north = pos_north

    def __str__(self) -> str:
        longitude = f'{"west" if self.pos_east < 0 else "east"} {abs(self.pos_east)}'
        latitude = f'{"south" if self.pos_north < 0 else "north"} {abs(self.pos_north)}'
        return f'{longitude} {latitude}'

    def move_north(self, value: int) -> None:
        self.pos_north += value

    def move_east(self, value: int) -> None:
        self.pos_east += value

    def move_south(self, value: int) -> None:
        self.pos_north -= value

    def move_west(self, value: int) -> None:
        self.pos_east -= value

    def manhattan_distance(self) -> int:
        return abs(self.pos_north) + abs(self.pos_east)


class Ship(Position):
    def __init__(self, pos_east: int, pos_north: int, direction: Direction) -> None:
        super().__init__(pos_east, pos_north)
        self.direction = direction

    def __str__(self) -> str:
        return f'{super().__str__()} - direction: {self.direction.name}'

    def rotate_right(self, value: int) -> None:
        self.direction = Direction((self.direction.value + value) % 360)

    def rotate_left(self, value: int) -> None:
        self.direction = Direction((self.direction.value - value) % 360)

    def move_towards(self, vector: Position, factor: int) -> None:
        self.pos_east += factor * vector.pos_east
        self.pos_north += factor * vector.pos_north

    _MOVE_FORWARD_DIRECTIONS = {
        Direction.North: Position.move_north,
        Direction.East: Position.move_east,
        Direction.South: Position.move_south,
        Direction.West: Position.move_west,
    }

    def move_forward(self, value: int) -> None:
        self._MOVE_FORWARD_DIRECTIONS[self.direction](self, value)


class Waypoint(Position):

    def rotate_right(self, value: int) -> None:
        if self.pos_north == 0 and self.pos_east == 0:
            return None
        deg = value % 360
        while deg > 0:
            pos_north = - self.pos_east
            self.pos_east = self.pos_north
            self.pos_north = pos_north
            deg -= 90

    def rotate_left(self, value: int) -> None:
        self.rotate_right(360 - value % 360)


def solve1() -> int:
    ship = Ship(0, 0, Direction.East)
    instructions = {
        'F': ship.move_forward,
        'N': ship.move_north,
        'E': ship.move_east,
        'S': ship.move_south,
        'W': ship.move_west,
        'R': ship.rotate_right,
        'L': ship.rotate_left,
    }
    for line in get_input():
        action, value = line[0], int(line[1:])
        instructions[action](value)
    return ship.manhattan_distance()


def solve2() -> int:
    ship = Ship(0, 0, Direction.East)
    waypoint = Waypoint(10, 1)

    def forward(factor: int) -> None:
        ship.move_towards(waypoint, factor)

    instructions = {
        'F': forward,
        'N': waypoint.move_north,
        'E': waypoint.move_east,
        'S': waypoint.move_south,
        'W': waypoint.move_west,
        'R': waypoint.rotate_right,
        'L': waypoint.rotate_left,
    }
    for line in get_input():
        action, value = line[0], int(line[1:])
        instructions[action](value)
    return ship.manhattan_distance()


if __name__ == '__main__':
    solution_part1 = solve1()
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve2()
    print(f'solution part 2: {solution_part2}')
