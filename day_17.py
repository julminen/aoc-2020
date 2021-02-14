#!/usr/bin/python3

from typing import List, Tuple, Dict, Set
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y", "z", "w"], defaults=[0])
Box = namedtuple("Box", ["x_range", "y_range", "z_range", "w_range"])


class Space:
    state: Set[Coordinate]

    def __init__(self, initial_state: List[str], dimensions: int = 3):
        if dimensions not in (3, 4):
            print(f'Weird dimensionality: {dimensions}')
        self.state = set()
        self.dimensions = dimensions
        z = 0
        w = 0
        for y, row in enumerate(initial_state):
            for x, cell in enumerate(list(row)):
                if cell == "#":
                    self.state.add(Coordinate(x, y, z))

    def size(self) -> Box:
        x = (
            min(self.state, key=lambda c: c.x).x,
            max(self.state, key=lambda c: c.x).x,
        )
        y = (
            min(self.state, key=lambda c: c.y).y,
            max(self.state, key=lambda c: c.y).y,
        )
        z = (
            min(self.state, key=lambda c: c.z).z,
            max(self.state, key=lambda c: c.z).z,
        )
        w = (
            min(self.state, key=lambda c: c.w).w,
            max(self.state, key=lambda c: c.w).w,
        )
        return Box((x[0], x[1]), (y[0], y[1]), (z[0], z[1]), (w[0], w[1]))

    @staticmethod
    def neighbors(origin: Coordinate, dimensions: int) -> List[Coordinate]:
        neighbors = list()
        if dimensions == 4:
            wr = range(origin.w - 1, origin.w + 2)
        else:
            wr = range(1)
        for w in wr:
            for z in range(origin.z - 1, origin.z + 2):
                for y in range(origin.y - 1, origin.y + 2):
                    for x in range(origin.x - 1, origin.x + 2):
                        neighbors.append(Coordinate(x, y, z, w))
        return neighbors

    def count_active_neighbors(self, origin: Coordinate) -> int:
        neighbors = Space.neighbors(origin, self.dimensions)
        neighbors.remove(origin)
        counter = 0
        for n in neighbors:
            if n in self.state:
                counter += 1
        return counter

    def step(self):
        new_state: Set[Coordinate] = set()
        # Get all possible new pockets
        search_space: Set[Coordinate] = set()
        for c in self.state:
            box = Space.neighbors(c, self.dimensions)
            search_space.update(box)
        for c in search_space:
            nc = self.count_active_neighbors(c)
            active = c in self.state
            if active and nc in (2, 3):
                new_state.add(c)
            elif not active and nc == 3:
                new_state.add(c)
        self.state = new_state

    def __repr__(self) -> str:
        """String representation (2D-slices) of space. Only works in 3D spaces

        Returns:
            str: 2D slices of space
        """
        size = self.size()
        my_repr: str = (
            f"Space, "
            + f"w = {size.w_range[0]}..{size.w_range[1]}, "
            + f"z = {size.z_range[0]}..{size.z_range[1]}, "
            + f"x = {size.x_range[0]}..{size.x_range[1]}, "
            + f"y = {size.y_range[0]}..{size.y_range[1]}:\n"
            + f"{len(self.state)} active pockets\n"
        )
        for z in range(size.z_range[0], size.z_range[1] + 1):
            my_repr += f"z={z}, w=0\n"
            for y in range(size.y_range[0], size.y_range[1] + 1):
                row = ["."] * (size.y_range[1] + 1 - size.y_range[0])
                for x in range(size.x_range[0], size.x_range[1] + 1):
                    if Coordinate(x, y, z, 0) in self.state:
                        row[x] = "#"
                    else:
                        row[x] = "."
                my_repr += "".join(row) + "\n"
        return my_repr


def read_file(day: str) -> List[str]:
    with open(f"input/day_{day}.txt") as file:
        lines = [line.strip() for line in file]
        return lines


def phase_1(input: List[str]):
    space = Space(input)
    print(space)
    for i in range(6):
        space.step()
    return len(space.state)


def phase_2(input: List[str]):
    space = Space(input, dimensions=4)
    for i in range(6):
        space.step()
    return len(space.state)


def execute(input: List[str]):
    p1 = phase_1(input)
    print(f"Phase 1: {p1}\n")

    p2 = phase_2(input)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    for day_input in ["17_s", "17"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")
