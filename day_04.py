#!/usr/bin/python3

from typing import Dict
import re

def read_input():
    with open('input/day_04.txt') as f:
        lines = [l.strip().split() for l in f.readlines()]
    data_list = list()
    data: Dict[str, str] = dict()
    for l in lines:
        if len(l) == 0:
            data_list.append(data)
            data = dict()
        else:
            for e in l:
                k, v = e.split(':')
                data[k] = v
    data_list.append(data)

    return data_list


def phase_1(data):
    valid_keys = set([
        'byr', # (Birth Year)
        'iyr', # (Issue Year)
        'eyr', # (Expiration Year)
        'hgt', # (Height)
        'hcl', # (Hair Color)
        'ecl', # (Eye Color)
        'pid', # (Passport ID)
        # 'cid', # (Country ID)
    ])
    counter = 0
    for d in data:
        if valid_keys.issubset(d.keys()):
            counter += 1
    return counter


def validate_passport(passport: dict):
    valid_keys = set([
        'byr', # (Birth Year)
        'iyr', # (Issue Year)
        'eyr', # (Expiration Year)
        'hgt', # (Height)
        'hcl', # (Hair Color)
        'ecl', # (Eye Color)
        'pid', # (Passport ID)
        # 'cid', # (Country ID)
    ])
    if not valid_keys.issubset(passport.keys()):
        # print('<--- Key missing')
        return False
    
    def is_valid_height(x: str):
        if len(x) < 4 or len(x) > 5:
            return False
        value = int(x[:-2])
        unit = x[-2:]
        return (
            unit == 'cm' and value >= 150 and value <= 193
            or unit == 'in' and value >= 59 and value <= 76
        )

    validators = {
        'byr': lambda x: x.isdigit() and int(x) >= 1920 and int(x) <= 2002, # (Birth Year)
        'iyr': lambda x: x.isdigit() and int(x) >= 2010 and int(x) <= 2020, # (Issue Year)
        'eyr': lambda x: x.isdigit() and int(x) >= 2020 and int(x) <= 2030, # (Expiration Year)
        'hgt': lambda x: is_valid_height(x), # (Height)
        'hcl': lambda x: re.fullmatch('#(\d|[a-f]){6}', x) is not None, # (Hair Color)
        'ecl': lambda x: x in set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']), # (Eye Color)
        'pid': lambda x: re.fullmatch('\d{9}', x) is not None, # (Passport ID)
        # 'cid', # (Country ID)
    }
    for k in validators:
        if not validators[k](passport[k]):
            # print(f'<--- Bad {k}: {passport[k]}')
            return False
        # print(f'{k} ({passport[k]}): {validators[k](passport[k])}')
    return True



def phase_2(data):
    counter = 0
    for d in data:
        if validate_passport(d):
            counter += 1
    return counter

if __name__ == "__main__":
    data = read_input()
    print(f'Phase 1: {phase_1(data)}')
    print(f'Phase 2: {phase_2(data)}')
