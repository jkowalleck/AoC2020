from copy import deepcopy
from enum import Enum, unique
from os import path
from typing import Callable, List, Tuple

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return fh.read().splitlines()


@unique
class SeatState(Enum):
    Floor = '.'
    Empty = 'L'
    Occupied = '#'


SeatNeighbors = Tuple[SeatState, SeatState, SeatState, SeatState, SeatState, SeatState, SeatState, SeatState]

_Row = int
_Col = int

NeighborFunction = Callable[["SeatArea", _Row, _Col, Tuple[_Row, _Col]], SeatState]


class SeatArea(List[List[SeatState]]):

    def count_state(self, value: SeatState) -> int:
        return sum(row.count(value) for row in self)

    def neighbor_adjacent(self, row: _Row, col: _Col, vector: Tuple[_Row, _Col]) -> SeatState:
        neighbor_row = row + vector[0]
        neighbor_col = col + vector[1]
        rows = len(self)
        cols = len(self[0])
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
            return self[neighbor_row][neighbor_col]
        return SeatState.Floor

    def neighbor_sight(self, row: _Row, col: _Col, vector: Tuple[_Row, _Col]) -> SeatState:
        neighbor_row = row + vector[0]
        neighbor_col = col + vector[1]
        rows = len(self)
        cols = len(self[0])
        while 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
            seat = self[neighbor_row][neighbor_col]
            if seat != SeatState.Floor:
                return seat
            neighbor_row += vector[0]
            neighbor_col += vector[1]
        return SeatState.Floor

    def neighbors(self, row: _Row, col: _Col, neighbor: NeighborFunction) -> SeatNeighbors:
        return (
            neighbor(self, row, col, (-1, -1)),
            neighbor(self, row, col, (-1, +0)),
            neighbor(self, row, col, (-1, +1)),
            neighbor(self, row, col, (-0, -1)),
            # neighbor(self, row, col, (+0, +0)), # own seat
            neighbor(self, row, col, (+0, +1)),
            neighbor(self, row, col, (+1, -1)),
            neighbor(self, row, col, (+1, +0)),
            neighbor(self, row, col, (+1, +1)),
        )

    def step(self, neighbor: NeighborFunction, tolerance: int) -> "SeatArea":
        rows = len(self)
        cols = len(self[0])
        new = deepcopy(self)
        for row in range(rows):
            for col in range(cols):
                if self[row][col] == SeatState.Floor:
                    continue
                occupied_count = self.neighbors(row, col, neighbor).count(SeatState.Occupied)
                if self[row][col] == SeatState.Empty:
                    if occupied_count == 0:
                        new[row][col] = SeatState.Occupied
                else:
                    if occupied_count >= tolerance:
                        new[row][col] = SeatState.Empty
        return new


def solve(neighbor: NeighborFunction, tolerance: int) -> int:
    seats = SeatArea([SeatState(char) for char in line] for line in get_input())
    while True:
        seats_next = seats.step(neighbor, tolerance)
        if seats_next == seats:
            break
        seats = seats_next
    return seats.count_state(SeatState.Occupied)


if __name__ == '__main__':
    solution_part1 = solve(SeatArea.neighbor_adjacent, 4)
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve(SeatArea.neighbor_sight, 5)
    print(f'solution part 2: {solution_part2}')
