#!/usr/bin/python3


def read_input():
    groups = list()
    with open(f'input/day_06.txt') as f:
        group = list()
        for line in f:
            line = line.strip()
            if len(line) == 0:
                groups.append(group)
                group = list()
            else:
                group.append(list(line))
        if len(group) > 0:
            groups.append(group)
    return groups

def phase_1(groups):
    x = 0
    for group in groups:
        yes = set()
        for answer in group:
            yes.update(answer)
        x += len(yes)
    return x

def phase_2(groups):
    x = 0
    for group in groups:
        yes = set(group[0])
        for answer in group:
            yes.intersection_update(answer)
        x += len(yes)
    return x
    

if __name__ == "__main__":
    data = read_input()
    print(f'Yksi: {phase_1(data)}')
    print(f'Kaksi: {phase_2(data)}')
