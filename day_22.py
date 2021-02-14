#!/usr/bin/python3

from typing import List, Tuple, Dict, Set, Union, Iterable, Optional
from re import split
from collections import namedtuple
from functools import reduce
from math import sqrt
from hashlib import blake2b


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        decks = [list(), list()]
        deck = -1
        for line in [line.strip() for line in file]:
            if line.startswith('Player'):
                deck += 1
                continue
            if line != '':
                decks[deck].append(int(line))
    return decks


def combat(deck_1, deck_2):
    card_1 = deck_1.pop(0)
    card_2 = deck_2.pop(0)
    if card_1 > card_2:
        deck_1.extend([card_1, card_2])
    else:
        deck_2.extend([card_2, card_1])
    return len(deck_1) != 0 and len(deck_2) != 0


def state_id(deck_1, deck_2):
    return blake2b(blake2b(bytes(deck_1)).digest() + b'~' + blake2b(bytes(deck_2)).digest()).digest()

def recursive_combat(deck_1, deck_2, game_states: Set[bytes]):
    winner = 0
    r = 0
    while winner == 0:
        r += 1
        if r % 10000 == 0:
            print(f'Round {r}')
        # Check if state is already played. If so, player 1 wins this (sub)game
        state = state_id(deck_1, deck_2)
        if state in game_states:
            return 1
        game_states.add(state)
        # Draw
        card_1 = deck_1.pop(0)
        card_2 = deck_2.pop(0)
        # Recurse?
        if card_1 <= len(deck_1) and card_2 <= len(deck_2):
            # New subgame
            sub_winner = recursive_combat(list(deck_1[:card_1]), list(deck_2[:card_2]), set())
            if sub_winner == 1:
                deck_1.extend([card_1, card_2])
            elif sub_winner == 2:
                deck_2.extend([card_2, card_1])
            else:
                print(f'WARN: unknow winner {sub_winner}')
        else:
            # Normal game rules
            if card_1 > card_2:
                deck_1.extend([card_1, card_2])
            else:
                deck_2.extend([card_2, card_1])
        if len(deck_1) == 0:
            winner = 2
        elif len(deck_2) == 0:
            winner = 1

    return winner


def count_score(deck):
    return sum(map(lambda x: (x[0]+1)*x[1], enumerate(reversed(deck))))

def phase_1(deck_1, deck_2):
    rounds = 0
    while(combat(deck_1, deck_2)):
        rounds += 1
        if rounds % 1000 == 0:
            print(f'round {rounds}...')
    score = 0
    if len(deck_1) != 0:
        print(f'Player 1 wins: {deck_1}')
        score = count_score(deck_1)
    else:
        print(f'Player 2 wins: {deck_2}')
        score = count_score(deck_2)
    return score


def phase_2(deck_1, deck_2):
    winner = recursive_combat(deck_1, deck_2, set())
    print(f'Winner: {winner}, p1: {count_score(deck_1)}, p2: {count_score(deck_2)}')
    return [count_score(deck_1), count_score(deck_2)][winner-1]


def execute(input, second_only: bool):
    deck_1, deck_2 = input
    if not second_only:
        p1 = phase_1(list(deck_1), list(deck_2))
        print(f"Phase 1: {p1}")

    p2 = phase_2(deck_1, deck_2)
    print(f"Phase 2: {p2} ")


if __name__ == "__main__":
    for day_input in ["22_s", "22_inf", "22"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input, day_input in ["22_inf"])
        print("..............")


# Answers
# 1: 32401
# 2: 
