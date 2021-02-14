#!/usr/bin/python3

def read_file(day):
    with open(f'input/day_{day}.txt') as file:
        lines = file.readlines()
    return [int(line.strip()) for line in lines]


def solve_phase_1(number_list):
    for a in range(len(numbers) - 1):
        eka = numbers[a]
        for n in range(a+1, len(numbers)):
            toka = numbers[n]
            if eka + toka == 2020:
                # print(f'1: {eka} + {toka} = 2020\n   {eka} * {toka} = {eka * toka}')
                return eka * toka


def solve_phase_2(number_list):
    for a in range(len(numbers) - 2):
        yy = numbers[a]
        for b in range(a+1, len(numbers)-1):
            kaa = numbers[b]
            if yy + kaa >= 2020:
                continue
            for c in range(b+1, len(numbers)):
                koo = numbers[c]
                if yy + kaa + koo == 2020:
                    # print(f'2: {yy} + {kaa} + {koo} = 2020\n   {yy} * {kaa} * {koo} = {yy * kaa * koo}')
                    return yy * kaa * koo



if __name__ == "__main__":
    numbers = read_file('01')
    print(f'Vaihe 1: {solve_phase_1(numbers)}')
    print(f'Vaihe 2: {solve_phase_2(numbers)}')
