#!/usr/bin/python3

from typing import List, Tuple, Dict, Set, Union, Iterable, Optional
from enum import Enum
from functools import reduce

class Color(Enum):
    BLACK = 'black',
    WHITE = 'white'


class HexVec:
    # x + y + z = 0
    def __init__(self, x, y, z):
        if x + y + z != 0:
            raise ValueError
        self.x = x  # SW -> NE
        self.y = y  # SE -> NW
        self.z = z  # N  -> S
    
    def __repr__(self):
        return f'({self.x}:{self.y}:{self.z})'
    
    def __add__(self, other):
        return HexVec(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def neighbors(self):
        return [
            self + HexVec(1, -1,  0),
            self + HexVec(1,  0, -1),
            self + HexVec(0,  1, -1),
            self + HexVec(-1, 1,  0),
            self + HexVec(0, -1,  1),
            self + HexVec(-1, 0,  1)
        ]


class Tile:
    def __init__(self, location: HexVec, color: Color = Color.WHITE):
        self.color = color
        self.location = location
    
    def flip(self):
        if self.color == Color.BLACK:
            self.color = Color.WHITE
        elif self.color == Color.WHITE:
            self.color = Color.BLACK
    
    def __repr__(self):
        return f'Tile at {self.location} is {self.color}'


def read_file(day: str) -> List[List[HexVec]]:
    with open(f"input/day_{day}.txt") as file:
        steps = list()
        for line in [line.strip() for line in file]:
            path: List[HexVec] = list()
            sl = list(line)
            i = 0
            while i < len(sl):
                if sl[i] == 'e':
                    path.append(HexVec(1, -1, 0))
                elif sl[i] == 'w':
                    path.append(HexVec(-1, 1, 0))
                elif sl[i] == 's' and sl[i+1] == 'e':
                    path.append(HexVec(0, -1, 1))
                    i += 1
                elif sl[i] == 's' and sl[i+1] == 'w':
                    path.append(HexVec(-1, 0, 1))
                    i += 1
                elif sl[i] == 'n' and sl[i+1] == 'e':
                    path.append(HexVec(1, 0, -1))
                    i += 1
                elif sl[i] == 'n' and sl[i+1] == 'w':
                    path.append(HexVec(0, 1, -1))
                    i += 1
                else:
                    print(f'WARNING: unknown direction {sl[i]}')
                i += 1
            steps.append(path)
    return steps


def phase_1(steps: List[List[HexVec]]):
    tiles = dict()
    for s in steps:
        location = reduce(lambda a, b: a + b, [HexVec(0, 0, 0)] + s)
        if location not in tiles:
            tiles[location] = Tile(location)
        tiles[location].flip()
    return len([x for x in tiles.values() if x.color == Color.BLACK])


def phase_2(steps: List[List[HexVec]]):
    # Initial state
    tiles = dict()
    for s in steps:
        location = reduce(lambda a, b: a + b, [HexVec(0, 0, 0)] + s)
        if location not in tiles.keys():
            tiles[location] = Tile(location)
        tiles[location].flip()
    # 100 days
    for day in range(100):
        # print(f'Day {day}: {len([x for x in tiles.values() if x.color == Color.BLACK])}, tiles: {len(tiles)}')
        # only black tiles and black tile neighbors can change
        checked_locations = set()
        new_tiles = dict()
        for n in [[tile.location] + tile.location.neighbors() for tile in tiles.values() if tile.color == Color.BLACK]:
            checked_locations.update(n)
        for location in checked_locations:
            if location not in tiles:
                tiles[location] = Tile(location)
            current_tile = tiles[location]
            neighbor_tiles = [tiles.get(l, Tile(l)) for l in current_tile.location.neighbors()]
            black_count = len([t for t in neighbor_tiles if t.color == Color.BLACK])
            # white_count = len([t for t in neighbor_tiles if t.color == Color.WHITE])
            if current_tile.color == Color.BLACK:
                if black_count == 1 or black_count == 2:
                    new_tiles[current_tile.location] = Tile(location, Color.BLACK)
            else:
                if black_count == 2:
                    new_tiles[current_tile.location] = Tile(location, Color.BLACK)
        tiles = new_tiles

    return len([x for x in tiles.values() if x.color == Color.BLACK])


def execute(steps: List[List[HexVec]]):
    p1 = phase_1(steps)
    print(f"Phase 1: {p1}")

    p2 = phase_2(steps)
    print(f"Phase 2: {p2} ")


if __name__ == "__main__":
    for day_input in ["24_s", "24"]:
        print(f"For {day_input}:")
        steps = read_file(day_input)
        execute(steps)
        print("..............")


# Answers
# 1: 269
# 2: 3667
