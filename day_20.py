#!/usr/bin/python3

from typing import List, Tuple, Dict, Set, Union, Iterable, Optional
from re import split
from collections import namedtuple
from functools import reduce
from math import sqrt

Coordinate = namedtuple("Coordinate", ["x", "y"])


class Tile:
    def __init__(self, spec: List[str]):
        _, name = spec[0].split()
        self.name = int(name.strip(':'))
        self.side_len = len(spec[1])
        self.pict_data: List[int] = list()
        for line in spec[1:]:
            self.pict_data.extend(list(map(int, list(line.replace('.', '0').replace('#', '1')))))

        # Bits in clockwise and ccw to account for symmetries
        def bitlist_to_int(bits: List[int]) -> int:
            out: int = 0
            for bit in bits:
                out = (out << 1) | bit
            return out

        self.top        = bitlist_to_int(self.pict_data[0:self.side_len])
        self.ccw_top    = bitlist_to_int(reversed(self.pict_data[0:self.side_len]))
        self.bottom     = bitlist_to_int(reversed(self.pict_data[-self.side_len:]))
        self.ccw_bottom = bitlist_to_int(self.pict_data[-self.side_len:])
        self.left       = bitlist_to_int(reversed(self.pict_data[0:self.side_len*self.side_len:self.side_len]))
        self.ccw_left   = bitlist_to_int(self.pict_data[0:self.side_len*self.side_len:self.side_len])
        self.right      = bitlist_to_int(self.pict_data[self.side_len-1:self.side_len*self.side_len:self.side_len])
        self.ccw_right  = bitlist_to_int(reversed(self.pict_data[self.side_len-1:self.side_len*self.side_len:self.side_len]))
    
    def get_borders(self):
        return [self.top, self.right, self.bottom, self.left]

    def get_ccw_borders(self):
        return [self.ccw_top, self.ccw_right, self.ccw_bottom, self.ccw_left]

    def get_rows(self) -> List[int]:
        sl = self.side_len
        return [self.pict_data[n*sl:n*sl + sl] for n in range(sl)]

    def get_data_rows(self) -> List[int]:
        sl = self.side_len
        return [self.pict_data[n*sl + 1 : n*sl + sl - 1] for n in range(1, sl - 1)]

    def flip(self):
        # flip around y axis
        # print(f'flipped {self.name}')
        self.top, self.ccw_top = self.ccw_top, self.top
        self.left, self.ccw_left, self.right, self.ccw_right = self.ccw_right, self.right, self.ccw_left, self.left
        self.bottom, self.ccw_bottom = self.ccw_bottom, self.bottom
        sl = self.side_len
        for i in range(sl):
            self.pict_data[i*sl:i*sl + sl] = reversed(self.pict_data[i*sl:i*sl+sl])
    
    def rotate(self):
        # print(f'rotated {self.name}')
        self.top, self.right, self.bottom, self.left = self.left, self.top, self.right, self.bottom
        self.ccw_top, self.ccw_right, self.ccw_bottom, self.ccw_left = self.ccw_left, self.ccw_top, self.ccw_right, self.ccw_bottom
        new_data = list()
        for i in range(self.side_len):
            new_data.extend(list(reversed(self.pict_data[i::self.side_len])))
        self.pict_data = new_data
    
    def is_neighbor(self, other, flipped=False) -> Optional[Coordinate]:
        for rotation in range(4):
            if self.top == other.ccw_bottom:
                return Coordinate(0, 1)
            if self.right == other.ccw_left:
                return Coordinate(1, 0)
            if self.bottom == other.ccw_top:
                return Coordinate(0, -1)
            if self.left == other.ccw_right:
                return Coordinate(-1, 0)
            other.rotate()
        if not flipped:
            other.flip()
            return self.is_neighbor(other, True)
        return None

    def count_monsters(self) -> int:
        monster = [
            list(map(int, list("                  # ".replace(' ', '0').replace('#', '1')))),
            list(map(int, list("#    ##    ##    ###".replace(' ', '0').replace('#', '1')))),
            list(map(int, list(" #  #  #  #  #  #   ".replace(' ', '0').replace('#', '1'))))
        ]
        mc = [sum(m) for m in monster]
        m_len = len(monster[0])
        y = 0
        monster_count = 0
        while y < self.side_len - len(monster) - 1:
            row_offset_1 = y * self.side_len
            row_offset_2 = y * self.side_len + self.side_len
            row_offset_3 = y * self.side_len + self.side_len * 2
            for x in range(self.side_len-m_len):
                matches = [
                    sum([a & b for a, b in zip(monster[0], self.pict_data[row_offset_1 + x : row_offset_1 + x * 1 + m_len])]),
                    sum([a & b for a, b in zip(monster[1], self.pict_data[row_offset_2 + x : row_offset_2 + x * 2 + m_len])]),
                    sum([a & b for a, b in zip(monster[2], self.pict_data[row_offset_3 + x : row_offset_3 + x * 3 + m_len])])
                ]
                if matches == mc:
                    # print(f'Found monster at y: {y}, x: {x}')
                    monster_count += 1
            y += 1
        return monster_count, sum(mc) * monster_count

    def __repr__(self):
        x = self.side_len
        y = self.side_len
        tmp: List[str] = list()
        for l in range(y):
            tmp.append(''.join(list(map(str, self.pict_data[l*x:l*x+x]))))
        tile = '\n'.join(tmp)
        return f'Tile {self.name}, {self.side_len} x {self.side_len}: {self.get_borders()} | {self.get_ccw_borders()}'

    def textual(self):
        tmp = list()
        x = self.side_len
        for l in range(x):
            tmp.append(''.join(list(map(str, self.pict_data[l*x:l*x+x]))).replace('0', '.').replace('1', '#'))
        return tmp


def read_file(day: str) -> List[Tile]:
    tiles: List[Tile] = list()
    buffer: List[str] = list()
    with open(f"input/day_{day}.txt") as file:
        for line in [line.strip() for line in file]:
            if line.startswith('Tile'):
                buffer = list()
            if len(line) == 0:
                if len(buffer) > 0:
                    tiles.append(Tile(buffer))
            buffer.append(line)
    return tiles


def phase_1(input: List[Tile]):
    tiles: List[Tile] = input
    # Assume borders are unique, so when combining cw and ccw borders count should not exceeld 2
    border_counts = dict()
    for tile in tiles:
        borders = tile.get_borders() + tile.get_ccw_borders()
        for b in borders:
            border_counts[b] = border_counts.get(b, 0) + 1
    v_counter = dict()
    for k, v in border_counts.items():
        if v > 2:
            print('WARNING')
            print(f'{k}: {v}')
        v_counter[v] = v_counter.get(v, 0) + 1
    
    # Corner tiles have two non-shared borders and two shared borders
    # But borders have ccw and cw variants, so they hit 4 and 4
    singles = set([k for k, v in border_counts.items() if v == 1])
    doubles = set([k for k, v in border_counts.items() if v == 2])

    borders = border_counts.keys()
    corners = list()
    for tile in tiles:
        borders = tile.get_borders() + tile.get_ccw_borders()
        single_hits = len(singles.intersection(borders))
        double_hits = len(doubles.intersection(borders))
        # print(f'Tile {tile.name}: singles: {single_hits}, doubles: {double_hits}')
        if single_hits == double_hits == 4:
            corners.append(tile.name)
    return reduce(lambda x, y: x * y, corners)


def create_big_tile(tiles):
    # print(f'{len(tiles)} tiles')
    full_side_length = int(sqrt(len(tiles)))
    tile_side_len = tiles[0].side_len
    tile_map = dict()
    # Create map
    # Flip and rotate tiles
    unhandled_tiles = [(Coordinate(0, 0), tiles.pop())]
    # print(f'Side len: {full_side_length}, tile side len with borders: {tile_side_len}')
    min_x = 0
    max_y = 0
    while len(unhandled_tiles) > 0:
        coordinate, tile = unhandled_tiles.pop()
        tile_map[coordinate] = tile
        #print(f'Looking at {tile.name} @ {coordinate}, possible neighbors: {len(tiles)}')
        # Find neighbors
        neighbors = []
        for i, t in enumerate(tiles):
            c = tile.is_neighbor(t)
            if c is not None:
                new_coord = Coordinate(coordinate.x + c.x, coordinate.y + c.y)
                #print(f'Neighbor for {tile.name} @ {coordinate}: {t.name} at {c} -> {new_coord}')
                # tile_map[new_coord] = t
                neighbors.append(i)
                unhandled_tiles.append((new_coord, t))
                min_x = min(new_coord.x, min_x)
                max_y = max(new_coord.y, max_y)
        for i in reversed(sorted(neighbors)):
            del tiles[i]
    if len(tiles) > 0:
        print(f'WARN: Tiles left: {len(tiles)}: {tiles}')

    # Drop borders and combine as new tile
    full_map = list()
    i = 0
    for yi, y in enumerate(range(max_y, max_y - full_side_length, -1)):
        for xi, x in enumerate(range(min_x, min_x + full_side_length)):
            c = Coordinate(x, y)
            xt = tile_map.get(c)
            rows = xt.get_data_rows()
            if xi == 0:
                full_map.extend(rows)
            else:
                for sri, sr in enumerate(rows):
                    full_map[yi*len(rows[0]) + sri].extend(sr)

    #for r in full_map:
    #    print(f'{"".join(map(str, r)).replace("1", "#").replace("0", ".")}')

    spec = ['Tile 0:'] + ["".join(map(str, r)).replace("1", "#").replace("0", ".") for r in full_map]
    return Tile(spec)

def phase_2(input):
    tiles: List[Tile] = list(input)
    big_tile = create_big_tile(tiles)
    total_sum = sum(big_tile.pict_data)
    # print(f'total: {total_sum}')
    mc = 0
    for side in range(2):
        for orientation in range(4):
            # print(f'side {side} orientation {orientation}')
            mc, sum_mc = big_tile.count_monsters()
            if mc > 0:
                return mc, total_sum - sum_mc
            big_tile.rotate()
        big_tile.flip()
    return mc, 0


def execute(input):
    p1 = phase_1(input)
    print(f"Phase 1: multiplying corners: {p1}")

    p2 = phase_2(input)
    print(f"Phase 2: with {p2[0]} monsters the sea roughness is {p2[1]} ")


if __name__ == "__main__":
    for day_input in ["20_s", "20"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")


# Answers
# 1: 17148689442341
# 2: 2009
