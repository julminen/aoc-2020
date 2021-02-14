#!/usr/bin/python3

from collections import namedtuple

PasswordEntry = namedtuple('PasswordEntry', ['min', 'max', 'letter', 'password'])

def read_file(day):
    with open(f'input/day_{day}.txt') as file:
        lines = map(str.strip, file.readlines())
    entries = list()
    for l in lines:
        a, b, c = l.split()
        min, max = a.split('-')
        entry = PasswordEntry(int(min), int(max), b[0], c)
        entries.append(entry)
    return entries


def is_valid_entry_range(entry):
    lettercount = entry.password.count(entry.letter)
    return lettercount >= entry.min and lettercount <= entry.max


def is_valid_entry_exact(entry):
    match_one = int(entry.password[entry.min-1] == entry.letter)
    match_two = int(entry.password[entry.max-1] == entry.letter)
    # Max one match
    return match_one + match_two == 1


def solve_phase_01(entries):
    valid = [e for e in entries if is_valid_entry_range(e)]
    return len(valid)


def solve_phase_02(entries):
    valid = [e for e in entries if is_valid_entry_exact(e)]
    return len(valid)


if __name__ == "__main__":
    entries = read_file('02')
    print(f'Eka : {solve_phase_01(entries)}')
    print(f'Toka: {solve_phase_02(entries)}')
