#!/usr/bin/python3

class Key():
    def __init__(self, public_key: int):
        self.public_key = public_key
        self.loop_size = self.resolve_loop_size()

    def resolve_loop_size(self) -> int:
        loop_size = 0
        value = 1
        while value != self.public_key:
            value = value * 7
            value = value % 20201227
            loop_size += 1
        return loop_size
    
    def transform(self, subject_number: int):
        value = 1
        for _ in range(self.loop_size):
            value = value * subject_number
            value = value % 20201227
        return value

    def __repr__(self):
        return f'Public key: {self.public_key}, loop size: {self.loop_size}'


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        lines = file.readlines()
    return int(lines[0]), int(lines[1])


def phase_1(card_public_key, door_public_key):
    card = Key(card_public_key)
    # door = Key(door_pub_key)
    # print(card.transform(door.public_key))
    # print(door.transform(card.public_key))
    return card.transform(door_public_key)

def phase_2():
    return '*'

def execute(keys):
    p1 = phase_1(keys[0], keys[1])
    print(f"Phase 1: {p1}")

    p2 = phase_2()
    print(f"Phase 2: {p2} ")


if __name__ == "__main__":
    for day_input in ["25_s", "25"]:
        print(f"For {day_input}:")
        data = read_file(day_input)
        execute(data)
        print("..............")


# Answers
# 1: 10187657
# 2: *
