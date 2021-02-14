#!/usr/bin/python3

from collections import namedtuple
from functools import reduce
from operator import mul

Location = namedtuple('Location', ['x', 'y'])

def read_input(day):
    with open(f'input/day_{day}.txt') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
    return lines

def make_map(lines):
    map = []
    for l in lines:
        map.append([c == '#' for c in l])
    return map

def is_tree(map, location: Location):
    return 1 if map[location.y][location.x % len(map[location.y])] else 0

def phase_01(map):
    hits = 0
    for row in range(len(map)):
        location = Location(row * 3, row)
        hits += is_tree(map, location)
    return hits

def phase_02(map):
    movements = [
        Location(1, 1),
        Location(3, 1),
        Location(5, 1),
        Location(7, 1),
        Location(1, 2)
    ]
    hit_counter = list()
    for movement in movements:
        location = Location(0, 0)
        hits = 0
        for _ in range(0, len(map) - 1, movement.y):
            location = Location(location.x + movement.x, location.y + movement.y)
            hits += is_tree(map, location)
        hit_counter.append(hits)
    return reduce(mul, hit_counter)


if __name__ == "__main__":
    map = make_map(read_input('03'))
    print(f'Vaihe 1: {phase_01(map)}') # 292
    print(f'Vaihe 2: {phase_02(map)}') # 9354744432
