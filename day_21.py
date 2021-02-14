#!/usr/bin/python3

from typing import List, Tuple, Dict, Set, Union, Iterable, Optional
from re import split
from collections import namedtuple
from functools import reduce
from math import sqrt


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        output = list()
        for line in [line.strip() for line in file]:
            i, a = line.split('(')
            ingredients = i.strip().split()
            allergens = a[len('contains '):].strip(')').split(', ')
            output.append((ingredients, allergens))
    return output


def phase_1(input):
    ingredient_counter = dict()
    allergen_map = dict()
    for i in input:
        ingredients, allergens = i
        for allergen in allergens:
            allergen_map[allergen] = allergen_map.get(allergen, set(ingredients)) & set(ingredients)
        for ingredient in ingredients:
            ingredient_counter[ingredient] = ingredient_counter.get(ingredient, 0) + 1
    ones = [k for k, v in allergen_map.items() if len(v) == 1]
    unspecified = allergen_map.keys() - ones
    while len(unspecified) > 0:
        for allergen in unspecified:
            for solved in ones:
                allergen_map[allergen] -= allergen_map[solved]
        ones = [k for k, v in allergen_map.items() if len(v) == 1]
        unspecified = allergen_map.keys() - ones
    for bad_ingredient in allergen_map.values():
        del ingredient_counter[list(bad_ingredient)[0]]
    return sum(ingredient_counter.values())


def phase_2(input):
    allergen_map = dict()
    for i in input:
        ingredients, allergens = i
        for allergen in allergens:
            allergen_map[allergen] = allergen_map.get(allergen, set(ingredients)) & set(ingredients)
    ones = [k for k, v in allergen_map.items() if len(v) == 1]
    unspecified = allergen_map.keys() - ones
    while len(unspecified) > 0:
        for allergen in unspecified:
            for solved in ones:
                allergen_map[allergen] -= allergen_map[solved]
        ones = [k for k, v in allergen_map.items() if len(v) == 1]
        unspecified = allergen_map.keys() - ones
    danger = list()
    for k in sorted(allergen_map):
        danger.append(list(allergen_map[k])[0])
    return ','.join(danger)


def execute(input):
    p1 = phase_1(input)
    print(f"Phase 1: {p1}")

    p2 = phase_2(input)
    print(f"Phase 2: {p2} ")


if __name__ == "__main__":
    for day_input in ["21_s", "21"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")


# Answers
# 1: 2170
# 2: nfnfk,nbgklf,clvr,fttbhdr,qjxxpr,hdsm,sjhds,xchzh
