#!/usr/bin/python3

from collections import namedtuple

Instruction = namedtuple("Instruction", ["op", "address", "value"])


class VMachine:
    def __init__(self, version=1):
        self.memory = dict()
        self.mask = "X" * 36
        self.or_mask = int("0" * 36, 2)
        self.and_mask = int("1" * 36, 2)
        self.version = version
        if version == 2:
            self.and_mask = 0

    def execute(self, instruction: Instruction):
        # print(instruction)
        if self.version == 1:
            if instruction.op == "mask":
                self.or_mask = int(instruction.value.replace("X", "0"), 2)
                self.and_mask = int(instruction.value.replace("X", "1"), 2)
            elif instruction.op == "mem":
                self.memory[instruction.address] = (
                    instruction.value & self.and_mask
                ) | self.or_mask
        elif self.version == 2:
            if instruction.op == "mask":
                self.mask = instruction.value
                self.or_mask = int(instruction.value.replace("X", "0"), 2)
            elif instruction.op == "mem":
                addresses = self.get_multiaddresses(instruction.address)
                for a in addresses:
                    self.memory[a] = instruction.value

    def get_multiaddresses(self, address):
        intermediate = list(f'{(address | self.or_mask):036b}')
        for x in [i for i, v in enumerate(self.mask) if v == 'X']:
            intermediate[x] = 'X'

        def replacer(x_list: list):
            ready_list = list()
            not_ready_list = list()
            for s in x_list:
                if 'X' not in s:
                    ready_list.append(s)
                else:
                    not_ready_list.append(s.replace('X', '0', 1))
                    not_ready_list.append(s.replace('X', '1', 1))
            if len(not_ready_list) > 0:
                ready_list.extend(replacer(not_ready_list))
            return ready_list

        l = replacer([''.join(intermediate)])

        return l

    def __repr__(self):
        return f"V{self.version}: and: {self.and_mask:b}, or: {self.or_mask:b}, mem contains {len(self.memory)} values"


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        lines = [line.strip() for line in file]
        program = list()
        for line in lines:
            op, value = line.split(" = ")
            if op == "mask":
                i = Instruction(op, None, value)
            else:
                op, address = op.split("[")
                i = Instruction(op, int(address[:-1]), int(value))
            program.append(i)
        return program


def phase_1(input):
    machine = VMachine()
    for i in input:
        machine.execute(i)
    print(machine)
    return sum(machine.memory.values())


def phase_2(input):
    # 55741467358 is too low
    machine = VMachine(version=2)
    for i in input:
        machine.execute(i)
    print(machine)
    return sum(machine.memory.values())


def execute(input):
    p1 = phase_1(input)
    print(f"Phase 1: {p1}\n")

    p2 = phase_2(input)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    for day_input in ["14"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")
