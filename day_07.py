#!/usr/bin/python3

from typing import Set, Optional, Dict

from collections import namedtuple

BagPointer = namedtuple('BagPointer', ['shade', 'color', 'count'])

class Bag:
    def __init__(self, shade: str, color: str):
        self.shade: str = shade
        self.color: str = color
        self.contains: Set[BagPointer] = set()
        self.contained_in: Set[BagPointer] = set()
        self.contained_bag_count: Optional[int] = None

    @staticmethod
    def from_pointer(pointer: BagPointer):
        return Bag(pointer.shade, pointer.color)

    def __repr__(self):
        return f'{self.shade} {self.color}:\n\tcontains: {self.contains}\n\tcontained in: {self.contained_in}'
    
    def __hash__(self):
        return hash(self.shade + ' ' + self.color)
    
    def __eq__(self, other):
        return self.shade == other.shade and self.color == other.color

    def add_contains(self, pointer: BagPointer):
        self.contains.add(pointer)
    
    def add_to_container(self, bag):
        self.contained_in.add(BagPointer(bag.shade, bag.color, 1))
    
    def get_contained_bag_count(self, bag_map):
        if self.contained_bag_count is None:
            self.contained_bag_count = 0
            for pointer in self.contains:
                other = bag_map[Bag.from_pointer(pointer)]
                self.contained_bag_count += pointer.count * (1 + other.get_contained_bag_count(bag_map))
        return self.contained_bag_count



def create_bag_pointers(bag_definitions: list):
    defs = list()
    if len(bag_definitions) > 0 and bag_definitions[0] != 'no':
        for i in range(0, len(bag_definitions), 4):
            count, shade, color, _ = bag_definitions[i: i+4]
            defs.append(BagPointer(shade, color, int(count)))
    return defs


def add_bag_with_children(bag: Bag, contains: list, bag_map: Dict[Bag, Bag]):
    if not bag in bag_map:
        bag_map[bag] = bag
    contained_bags = create_bag_pointers(contains)
    for sub in contained_bags:
        sub_bag = Bag.from_pointer(sub)
        if not sub_bag in bag_map:
            bag_map[sub_bag] = sub_bag
        bag_map[bag].add_contains(sub)
        bag_map[sub_bag].add_to_container(bag)

def bag_wrappers(bag: Bag, bag_map: dict):
    wrappers = set()
    unhandled_pointers = set(bag_map[bag].contained_in)
    while len(unhandled_pointers) > 0:
        p = unhandled_pointers.pop()
        if p not in wrappers:
            unhandled_pointers.update(bag_map[Bag.from_pointer(p)].contained_in)
            wrappers.add(p)
    return wrappers

def read_file():
    with open(f'input/day_07.txt') as file:
        lines = list(map(str.strip, file.readlines()))
        bags: Dict[Bag, Bag] = dict()
        for line in lines:
            parent, contains = line.split(' bags contain ')
            shade, color = parent.split()
            bag = Bag(shade, color)
            add_bag_with_children(bag, contains.split(), bags)
    return bags

def phase_1(bags: dict):
    wrappers = bag_wrappers(Bag('shiny', 'gold'), bags)
    print(f'Shiny Golden bag can be stored in {len(wrappers)} different bags')

def phase_2(bags: dict):
    sg = bags[Bag('shiny', 'gold')]
    print(f'Shiny Golden bag must include {sg.get_contained_bag_count(bags)} bags')

if __name__ == "__main__":
    bags = read_file()
    phase_1(bags)
    phase_2(bags)