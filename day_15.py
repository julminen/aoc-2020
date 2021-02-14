#!/usr/bin/python3

from collections import namedtuple


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        lines = [line.strip() for line in file]
        numbers = [int(n) for n in lines[0].split(",")]
        return numbers


def play(input, until):
    # A bit slow
    print(f"Initial: {input}")
    mem = dict()
    for i, v in enumerate(input[:-1]):
        mem[v] = i + 1
    spoken_num = input[-1]
    for age in range(len(mem) + 1, until):
        previously_spoken = mem.get(spoken_num, age)
        mem[spoken_num] = age
        spoken_num = age - previously_spoken
    print(f'{len(mem)} elements in memory')
    return spoken_num


def phase_1(input):
    return play(input, 2020)


def phase_2(input):
    return play(input, 30_000_000)


def execute(input):
    p1 = phase_1(input)
    print(f"Phase 1: {p1}\n")

    p2 = phase_2(input)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    for day_input in ["15"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")
