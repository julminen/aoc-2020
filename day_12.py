#!/usr/bin/python3

from collections import namedtuple

Instruction = namedtuple("Instruction", ["direction", "amount"])


class Ship:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.heading = "E"

    def move(self, instruction: Instruction):
        if instruction.direction == "N":
            self.y += instruction.amount
        elif instruction.direction == "S":
            self.y -= instruction.amount
        elif instruction.direction == "E":
            self.x += instruction.amount
        elif instruction.direction == "W":
            self.x -= instruction.amount
        elif instruction.direction == "F":
            self.move(Instruction(self.heading, instruction.amount))
        elif instruction.direction == "L":
            self.turn(instruction.amount * -1)
        elif instruction.direction == "R":
            self.turn(instruction.amount)
        else:
            print(f"Bad orders! {instruction}")

    def turn(self, amount: int):
        headings = ["N", "E", "S", "W"]
        turn = int((amount % 360) / 90)
        new_heading = (headings.index(self.heading) + turn) % 4
        self.heading = headings[new_heading]

    def __repr__(self):
        return f"At ({self.x}, {self.y}), heading {self.heading}"


class Cruiser:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.wp_x: int = 10
        self.wp_y: int = 1

    def move(self, instruction: Instruction):
        if instruction.direction == "N":
            self.wp_y += instruction.amount
        elif instruction.direction == "S":
            self.wp_y -= instruction.amount
        elif instruction.direction == "E":
            self.wp_x += instruction.amount
        elif instruction.direction == "W":
            self.wp_x -= instruction.amount
        elif instruction.direction == "F":
            self.x = self.x + instruction.amount * self.wp_x
            self.y = self.y + instruction.amount * self.wp_y
        elif instruction.direction == "L":
            self.rotate_wp(instruction.amount * -1)
        elif instruction.direction == "R":
            self.rotate_wp(instruction.amount)
        else:
            print(f"Bad orders! {instruction}")

    def rotate_wp(self, amount: int):
        rotate = int((amount % 360) / 90) % 4
        if rotate == 1:
            new_y = self.wp_x * -1
            new_x = self.wp_y
        elif rotate == 2:
            new_x = self.wp_x * -1
            new_y = self.wp_y * -1
        elif rotate == 3:
            new_y = self.wp_x
            new_x = self.wp_y * -1
        self.wp_x = new_x
        self.wp_y = new_y

    def __repr__(self):
        return f"At ({self.x}, {self.y}), wp: ({self.wp_x}, {self.wp_y})"


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        instructions = list()
        for line in file:
            instructions.append(Instruction(line[0], int(line[1:])))
        return instructions


def phase_1(instructions: list):
    s = Ship()
    for i in instructions:
        s.move(i)
    distance = abs(s.x) + abs(s.y)
    return distance


def phase_2(instructions: list):
    cruiser = Cruiser()
    for i in instructions:
        cruiser.move(i)
    distance = abs(cruiser.x) + abs(cruiser.y)
    return distance


def execute(instructions: list):
    p1 = phase_1(instructions)
    print(f"Phase 1: {p1}\n")

    p2 = phase_2(instructions)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    sample_1 = read_file("12_s")
    print("Example 1")
    execute(sample_1)
    print("..............")

    real = read_file("12")
    print("Real")
    execute(real)
