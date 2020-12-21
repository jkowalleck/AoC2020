from copy import deepcopy
from enum import Enum, unique
from os import path
from typing import List, Tuple

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


class SeatArea(List[List[SeatState]]):

    def count_states(self, value: SeatState) -> int:
        return sum(row.count(value) for row in self)

    def get(self, row, col) -> SeatState:
        if 0 <= row < len(self):
            _row = self[row]
            if 0 <= col < len(_row):
                return _row[col]
        return SeatState.Floor

    def neighbors(self, row, col) -> SeatNeighbors:
        return (
            self.get(row - 1, col - 1),
            self.get(row - 1, col),
            self.get(row - 1, col + 1),
            self.get(row, col - 1),
            # self.get(row, col),
            self.get(row, col + 1),
            self.get(row + 1, col - 1),
            self.get(row + 1, col),
            self.get(row + 1, col + 1),
        )

    def step(self) -> "SeatArea":
        rows = len(self)
        cols = len(self[0])
        new = deepcopy(self)
        for row in range(rows):
            for col in range(cols):
                if self[row][col] == SeatState.Floor:
                    continue
                occupied_count = self.neighbors(row, col).count(SeatState.Occupied)
                if self[row][col] == SeatState.Empty:
                    if occupied_count == 0:
                        new[row][col] = SeatState.Occupied
                else:
                    if occupied_count >= 4:
                        new[row][col] = SeatState.Empty
        return new


def get_input_seats() -> SeatArea:
    return SeatArea(
        [SeatState(char) for char in line]
        for line
        in get_input()
    )


def solve() -> int:
    seats = get_input_seats()
    while True:
        seats_next = seats.step()
        if seats_next == seats:
            break
        seats = seats_next
    return seats.count_states(SeatState.Occupied)


if __name__ == '__main__':
    solution_part1 = solve()
    print(f'solution part 1: {solution_part1}')
    # solution_part2 = solve()
    # print(f'solution part 2: {solution_part2}')
