#!/usr/bin/python3

def read_file(day: str):
    with open(f'input/day_{day}.txt') as file:
        return [int(x) for x in map(str.strip, file.readlines())]


def has_valid_sum(numbers: list, target: int):
    # print(f'search for {target} in {numbers}')
    for a in range(len(numbers)-1):
        for b in range(a+1, len(numbers)):
            # print(f'{a}.{b}: {numbers[a]} + {numbers[b]}')
            if numbers[a] + numbers[b] == target:
                return True
    return False


def phase_1(nums: list, prem: int):
    for a in range(len(nums) - prem - 1):
        if not has_valid_sum(nums[a:a+prem], nums[a+prem]):
            print( f'1 -> at {a+prem} value {nums[a+prem]} is invalid')
            return nums[a+prem]


def phase_2(nums: list, target: int):
    a = 0
    b = 1
    s = sum(nums[a:b])
    while s != target:
        if s < target:
            b += 1
        elif s > target:
            a += 1
        if a >= b or a >= len(nums) or b >= len(nums):
            print(f'Bad state a: {a}, b: {b}, nums: {len(nums)}')
            break
        s = sum(nums[a:b])
    smallest = min(nums[a:b])
    largest = max(nums[a:b])
    print(f'Sum from {a} to {b-1} produces {s} and min/max are {smallest}/{largest}')
    return smallest + largest


def execute(nums: list, premeable: int):
    bad_num = phase_1(nums, premeable)
    print(f'Phase 1: value {bad_num} is invalid')
    print(f'Phase 2: min + max is {phase_2(nums, bad_num)}')


if __name__ == "__main__":
    sample_nums = read_file('09_sample')
    print('Example numbers:')
    execute(sample_nums, 5)

    print('\nReal list')
    nums = read_file('09')
    execute(nums, 25)
