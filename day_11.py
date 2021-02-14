#!/usr/bin/python3

from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])


class SeatMap:
    def __init__(self):
        self.seats = [[], []]
        self.rows: int = 0
        self.columns: int = 0
        self.front = 0
        self.back = 1

    def reset(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if self.read(x, y) != ".":
                    self.seats[self.front][y][x] = "L"
                    self.seats[self.back][y][x] = "L"
        self.front = 0
        self.back = 1

    def flip(self):
        tmp = self.front
        self.front = self.back
        self.back = tmp

    def add_row(self, row: str):
        self.seats[self.front].append(list(row))
        self.seats[self.back].append(list("".join(row)))
        self.rows += 1
        if len(row) > self.columns:
            self.columns = len(row)

    def is_occupied(self, x: int, y: int) -> bool:
        if x >= self.columns or y >= self.rows:
            return False
        return self.read(x, y) == "#"

    def occupied_neighbors(self, x: int, y: int) -> int:
        count = 0
        for ix in range(max(0, x - 1), min(x + 2, self.columns)):
            for iy in range(max(0, y - 1), min(y + 2, self.rows)):
                if (x != ix or y != iy) and self.is_occupied(ix, iy):
                    count += 1
        return count

    def read(self, x: int, y: int):
        return self.seats[self.front][y][x]

    def write(self, x: int, y: int, c: chr):
        self.seats[self.back][y][x] = c

    def look_at(self, origin: Coordinate, delta: Coordinate) -> chr:
        x: int = origin.x + delta.x
        y: int = origin.y + delta.y
        while x >= 0 and x < self.columns and y >= 0 and y < self.rows:
            tile = self.read(x, y)
            if tile != ".":
                return tile
            x += delta.x
            y += delta.y
        return "."

    def visible_occupied_count(self, origin: Coordinate):
        count = 0
        directions = [
            Coordinate(-1, -1),
            Coordinate(-1, 0),
            Coordinate(-1, 1),
            Coordinate(0, 1),
            Coordinate(1, 1),
            Coordinate(1, 0),
            Coordinate(1, -1),
            Coordinate(0, -1),
        ]
        for d in directions:
            if self.look_at(origin, d) == "#":
                count += 1
        return count

    def step_1(self):
        changes = 0
        for y in range(self.rows):
            for x in range(self.columns):
                state = self.read(x, y)
                if state == "L" and self.occupied_neighbors(x, y) == 0:
                    self.write(x, y, "#")
                    changes += 1
                elif state == "#" and self.occupied_neighbors(x, y) >= 4:
                    self.write(x, y, "L")
                    changes += 1
                else:
                    self.write(x, y, state)
        self.flip()
        return changes

    def step_2(self):
        changes = 0
        for y in range(self.rows):
            for x in range(self.columns):
                state = self.read(x, y)
                c: Coordinate = Coordinate(x, y)
                if state == "L" and self.visible_occupied_count(c) == 0:
                    self.write(x, y, "#")
                    changes += 1
                elif state == "#" and self.visible_occupied_count(c) >= 5:
                    self.write(x, y, "L")
                    changes += 1
                else:
                    self.write(x, y, state)
        self.flip()
        return changes

    def occupied_count(self):
        return sum(
            [len(list(filter(lambda c: c == "#", r))) for r in self.seats[self.front]]
        )

    def __repr__(self) -> str:
        output = list()
        for y in range(self.rows):
            output.append("".join(self.seats[self.front][y]))
        output.append(f"Occupied: {self.occupied_count()}")
        return "\n".join(output)


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        seat_map = SeatMap()
        for line in file:
            seat_map.add_row(line.strip())
        return seat_map


def phase_1(seats: SeatMap):
    n = 1
    while seats.step_1() > 0:
        n += 1
    # print('Final state:')
    # print(seats)
    return n, seats.occupied_count()


def phase_2(seats: SeatMap):
    n = 1
    while seats.step_2() > 0:
        n += 1
        if n % 10 == 0:
            print(f"...{n}...")
    # print('Final state:')
    # print(seats)
    # print()
    return n, seats.occupied_count()


def execute(seats: SeatMap):
    p1 = phase_1(seats)
    print(f"Phase 1: {p1}\n")
    seats.reset()

    p2 = phase_2(seats)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    sample_1 = read_file("11_s")
    print("Example 1")
    execute(sample_1)
    print("..............")

    real = read_file("11")
    print("Real")
    execute(real)
