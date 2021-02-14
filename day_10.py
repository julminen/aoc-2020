#!/usr/bin/python3


def read_file(day: str):
    with open(f'input/day_{day}.txt') as file:
        return [int(x) for x in map(str.strip, file.readlines())]



def phase_1(nums: list):
    voltages = list([0])
    voltages.extend(sorted(nums))  # copy
    voltages.append(voltages[-1]+3)
    # print(voltages)
    j_1 = 0
    j_3 = 0
    for i in range(1, len(voltages)):
        if voltages[i] - voltages[i-1] == 1:
            j_1 += 1
        elif voltages[i] - voltages[i-1] == 3:
            j_3 += 1
        else:
            print(f'Bad jump from {voltages[i-1]} to {voltages[i]}')
    return j_1, j_3


def count_paths(node_list: list):
    paths = 0
    path_counts = dict()
    node_list.reverse()
    # print(node_list)
    path_counts[node_list[0]] = 1
    prev_node = node_list[0]
    for i in range(1, len(node_list)):
        node = node_list[i]
        if prev_node - node == 3:
            path_counts[node] = 1 + path_counts[prev_node] - 1
        if prev_node - node == 1:
            count = 1
            if i - 2 >= 0 and node_list[i-2] - node == 2:
                count += 1 + path_counts[node_list[i-2]] - 1
            if i - 3 >= 0 and node_list[i-3] - node == 3:
                count += 1 + path_counts[node_list[i-3]] - 1
            path_counts[node] = count + path_counts[prev_node] - 1
        prev_node = node
    # print(path_counts)
    return path_counts[0]


def phase_2(nums: list):
    voltages = list([0])
    voltages.extend(sorted(nums))  # copy
    voltages.append(voltages[-1]+3)
    return count_paths(voltages)

def execute(nums: list):
    p1 = phase_1(nums)
    p2 = phase_2(nums)
    print(f'Phase 1: 1 and 3 jumps: {p1} -> {p1[0] * p1[1]}')
    print(f'Phase 2: possible configurations: {p2}')


if __name__ == "__main__":
    sample_nums = read_file('10_s1')
    print('Example 1')
    execute(sample_nums)
    print('..............')

    sample_nums = read_file('10_s2')
    print('Example 2')
    execute(sample_nums)
    print('..............')

    real_nums = read_file('10')
    print('Real')
    execute(real_nums)
