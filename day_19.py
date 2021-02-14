#!/usr/bin/python3

# TODO: tidy up the code

from typing import List, Tuple, Dict, Set, Union, Iterable
from re import split
from operator import mul, add

class Matcher:
    def __init__(self, definition: str):
        my_id, rules = definition.split(':')
        self.id = int(my_id)
        str_match = rules.strip().split('"')
        self.rule_set: List[List[int]] = list()
        self.is_recursive = False
        if len(str_match) == 3:
            self.char_match = str_match[1]
            self.min_rule_length = 1
        else:
            self.char_match = ''
            for or_rule in rules.split('|'):
                and_rules = list(map(int, or_rule.split()))
                if self.id in and_rules:
                    self.is_recursive = True
                self.rule_set.append(and_rules)
            self.min_rule_length = None

    def min_length(self, rules):
        if self.min_rule_length is not None:
            return self.min_rule_length
        rl = 0
        for or_rule in self.rule_set:
            tl = 0
            for and_rule in or_rule:
                if and_rule != self.id:
                    tl += rules[and_rule].min_length(rules)
            if tl > rl:
                rl = tl
        self.min_rule_length = rl
        return rl

    def get_version(self, version: int):
        if not self.is_recursive:
            return self.rule_set
        if version == 0:
            return self.rule_set[0]
        rec_rule = self.rule_set[1]
        idx = rec_rule.index(self.id)
        l = rec_rule[:idx] + self.get_version(version - 1) + rec_rule[idx+1:]
        return l

    def match(self, message: str, index: int, rules, indent=0) -> Tuple[bool, int]:
        n = list(message)
        n.insert(index, '-')
        #print(f'{" "*indent}Matching rule {self.id}: @[{index}] {str(self)} : {"".join(n)}')
        if index >= len(message):
            print('Bad index')
            return False, 0
        if self.char_match != '':
            ok = message[index] == self.char_match
            advance = 1
        else:
            for or_rule in self.rule_set:
                ok = True
                advance = 0
                for and_rule in or_rule:
                    #print(f'{" "*indent}[{and_rule}] in {self.rule_set}')
                    next_rule = rules[and_rule]
                    #print(f'Next: {next_rule} for {message}[{index+advance}]')
                    ok, a = next_rule.match(message, index + advance, rules, indent+2)
                    advance += a
                    if not ok:
                        break
                if ok:
                    break
        n = list(message)
        n.insert(index+advance, '-')
        #print(f'{" "*indent}{self.id} --> {ok, advance} : {"".join(n)}')
        return ok, advance

    def __repr__(self) -> str:
        if self.char_match != '':
            s = f'"{self.char_match}"'
        else:
            s = ' | '.join([' '.join(map(str, x)) for x in self.rule_set])
        if self.is_recursive:
            rec = ' (recursive)'
        else:
            rec = ''
        return f'{self.id}: {s}{rec}'


def read_file(day: str) -> List[str]:
    with open(f"input/day_{day}.txt") as file:
        lines = [line.strip() for line in file]
        rules = dict()
        messages = list()
        line_it = iter(lines)
        for l in line_it:
            if len(l) == 0:
                break
            m = Matcher(l)
            rules[m.id] = m
        for l in line_it:
            messages.append(l)
        return rules, messages


def phase_1(input):
    rules: Dict[int, Matcher] = input[0]
    messages: List[str] = input[1]
    counter = 0
    for msg in messages:
        ok, upto = rules[0].match(msg, 0, rules)
        #print(f'{msg}: {ok, upto} -> {ok and upto == len(msg)}')
        if ok and upto == len(msg):
            counter += 1
            # print(f'MATCH: {msg}')
    return counter


def phase_2(input):
    rules: Dict[int, Matcher] = input[0]
    # Fixed rules
    rules[8] = Matcher('8: 42 | 42 8')
    rules[11] = Matcher('11: 42 31 | 42 11 31')
    #for k in sorted(rules.keys()):
    #    print(f'{rules[k]} - {rules[k].min_length(rules)}')

    messages: List[str] = input[1]
    counter = 0
    for msg in messages:
        # print(f'\nMessage: {msg} ({len(msg)})')
        root_rule = rules[0]
        # Rule 0 contains two rules, both recursive
        rule_a, rule_b = map(rules.get, root_rule.rule_set[0])
        #print(f'{rule_a}\n{rule_b}')
        #print(f'{" ".join(map(str, rule_a.get_version(0)))}')

        max_length = len(msg)
        loop_a = 0
        loop_b = 0
        new_rule_a = Matcher(f'{rule_a.id}: {" ".join(map(str, rule_a.get_version(loop_a)))}')
        new_rule_b = Matcher(f'{rule_b.id}: {" ".join(map(str, rule_b.get_version(loop_b)))}')
        rules[rule_a.id] = new_rule_a
        rules[rule_b.id] = new_rule_b

        test_messages = True
        rule_min_length = rules[rule_a.id].min_length(rules) + rules[rule_b.id].min_length(rules)
        while test_messages and rule_min_length <= len(msg):
            while test_messages and rule_min_length <= len(msg):
                # print(f'testing with {loop_a} / {loop_b}, len = {rules[rule_a.id].min_length(rules)} + {rules[rule_b.id].min_length(rules)}')
                ok, upto = rules[0].match(msg, 0, rules)
                if ok and upto == len(msg):
                    counter += 1
                    # print(f'MATCH: {msg}')
                    test_messages = False
                loop_a += 1
                rules[rule_a.id] = Matcher(f'{rule_a.id}: {" ".join(map(str, rule_a.get_version(loop_a)))}')
                rule_min_length = rules[rule_a.id].min_length(rules) + rules[rule_b.id].min_length(rules)
            loop_b += 1
            rules[rule_b.id] = Matcher(f'{rule_b.id}: {" ".join(map(str, rule_b.get_version(loop_b)))}')
            loop_a = 0
            rules[rule_a.id] = Matcher(f'{rule_a.id}: {" ".join(map(str, rule_a.get_version(loop_a)))}')
            rule_min_length = rules[rule_a.id].min_length(rules) + rules[rule_b.id].min_length(rules)
        rules[rule_a.id] = rule_a
        rules[rule_b.id] = rule_b
        # ok, upto = rules[0].match(msg, 0, rules)
        # print(f'{msg}: {ok, upto} -> {ok and upto == len(msg)}')
        # if ok and upto == len(msg):
        #     counter += 1
    return counter


def execute(input: List[str], do_phase_2=False):
    p1 = phase_1(input)
    print(f"Phase 1 matches: {p1}")

    if (do_phase_2):
        p2 = phase_2(input)
        print(f"Phase 2 matches: {p2}")


if __name__ == "__main__":
    for day_input in ["19"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input, day_input in ("19"))
        print("..............")


# Answers
# 1: 120
# 2: 350