#!/usr/bin/python3

from typing import List, Tuple, Dict, Set, Union
from re import split
from operator import mul, add


def compute_equal_precedence(enumerator: enumerate) -> int:
    op = lambda a, b: b
    result = 0
    for i, t in enumerator:
        if t == "*":
            op = mul
        elif t == "+":
            op = add
        elif t == "(":
            result = op(result, compute_equal_precedence(enumerator))
        elif t == ")":
            return result
        else:
            result = op(result, int(t))
    return result


def find_matching_brace(tokens: List[Union[str,int]], idx: int) -> int:
    depth = 0
    for i, t in enumerate(tokens[idx:]):
        if t == '(':
            depth += 1
        elif t == ')':
            depth -= 1
            if depth == 0:
                return i
    return idx


def compute(tokens: List[Union[str,int]]) -> int:
    result = 0
    # print(f'Starting from {tokens}')
    while '(' in tokens:
        a = tokens.index('(')
        b = find_matching_brace(tokens, a) + a
        val = compute(tokens[a+1:b])
        tokens = tokens[:a] + [val] + tokens[b+1:]
    while '+' in tokens:
        m = tokens.index('+')
        v: int = int(tokens[m-1]) + int(tokens[m+1])
        tokens = tokens[:m-1] + [int(v)] + tokens[m+2:]
    while '*' in tokens:
        m = tokens.index('*')
        v = int(tokens[m-1]) * int(tokens[m+1])
        tokens = tokens[:m-1] + [int(v)] + tokens[m+2:]
    return int(tokens[0])


def read_file(day: str) -> List[str]:
    with open(f"input/day_{day}.txt") as file:
        lines = [line.strip() for line in file if line.strip() != ""]
        return lines


def phase_1(input: List[str]):
    xsum: int = 0
    for expression in input:
        # print(expression)
        tokens = [t.strip() for t in split(r"( |\(|\))", expression) if t.strip() != ""]
        res = compute_equal_precedence(enumerate(tokens))
        # print(f' --> {res}')
        xsum += res
    return xsum


def phase_2(input: List[str]):
    xsum: int = 0
    for expression in input:
        # print(expression)
        tokens: List[Union[str, int]] = [t.strip() for t in split(r"( |\(|\))", expression) if t.strip() != ""]
        res = compute(tokens)
        # print(f'  --> {res}')
        xsum += res
    return xsum


def execute(input: List[str]):
    p1 = phase_1(input)
    print(f"Phase 1: {p1}")

    p2 = phase_2(input)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    for day_input in ["18_s", "18"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")


# Answers
# 1: 800602729153
# 2: 92173009047076