#!/usr/bin/python3

# Tried different variations for phase 2, none which is especially fast

from typing import List
from collections import namedtuple

Cup = namedtuple('Cup', ['value', 'next'])

class ListNode:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.next_node = None
    
    def __repr__(self):
        return f'Node {self.node_id}'


def phase_1(cups: List[int], moves: int):
    # print(f'Initial: {cups}')
    cup_count = len(cups)
    current_cup_index = 0
    max_cup_value = max(cups)
    min_cup_value = min(cups)
    all_indexes = list(range(cup_count))
    for round in range(moves):
        # print(f'Move {round+1}: cci = {current_cup_index} : {cups}')

        pick_up_indexes = [(current_cup_index + x + 1) % cup_count for x in range(3)]
        # print(f'    picking up: {[cups[i] for i in pick_up_indexes]}')

        current_cup_value = cups[current_cup_index]
        new_cups = [cups[i] for i in all_indexes if i not in pick_up_indexes]
        destination_cup_index = -1
        search_cup_value = current_cup_value - 1
        while destination_cup_index == -1:
            if search_cup_value in new_cups:
                destination_cup_index = new_cups.index(search_cup_value)
            else:
                search_cup_value -= 1
                if search_cup_value < min_cup_value:
                    search_cup_value = max_cup_value
        # print(f'    destination: [{destination_cup_index}] = {search_cup_value}')
        cups = new_cups[0:destination_cup_index+1] + [cups[i] for i in pick_up_indexes] + new_cups[destination_cup_index+1:]
        current_cup_index = (cups.index(current_cup_value) + 1) % len(cups)
    # print(f'Final: {cups}')
    bp = cups.index(1)
    return ''.join(map(str, cups[bp+1:] + cups[0:bp]))


def phase_2_faster(cups: List[int], moves: int):
    print(cups)
    # More moves
    moves = 10_000_000
    # More cups
    cups = cups + list(range(max(cups)+1, 1_000_001))
    #
    min_cup_value = min(cups)
    max_cup_value = max(cups)
    start_node = ListNode(cups[0])
    current_node = start_node
    node_map: Dict[int: ListNode] = dict()
    node_map[cups[0]] = start_node
    print(f'Creating node list ({len(cups)})')
    for cup in cups[1:]:
        head_node = ListNode(node_id=cup)
        node_map[cup] = head_node
        current_node.next_node = head_node
        current_node = head_node
    current_node.next_node = start_node
    print(f'Nodes done {current_node} -> {current_node.next_node}')
    current_node = start_node

    x = start_node.next_node
    counter = 1
    while x != start_node:
        #print(x)
        x = x.next_node
        counter += 1
    print(x, counter)
    print(f'node_map len = {len(node_map)}')

    for move in range(moves):
        if move % 250000 == 0:
            print(f'Move {move}')
        # pick up 3 nodes after current_node
        pick_up_node = current_node.next_node
        current_node.next_node = current_node.next_node.next_node.next_node.next_node
        #pick_up_node.next_node.next_node.next_node = None
        pick_up_ids = [pick_up_node.node_id, pick_up_node.next_node.node_id, pick_up_node.next_node.next_node.node_id]
        # Find destination
        destination_cup_value = current_node.node_id - 1
        while destination_cup_value < min_cup_value or destination_cup_value in pick_up_ids:
            if destination_cup_value < min_cup_value:
                destination_cup_value = max_cup_value + 1
            destination_cup_value -= 1
        destination_node = node_map[destination_cup_value]
        # Put picked up cups after destination
        pick_up_node.next_node.next_node.next_node, destination_node.next_node = destination_node.next_node, pick_up_node
        # Set new current_node
        current_node = current_node.next_node
    node_1 = node_map[1]
    print(f'Nodes after {node_1} are {node_1.next_node} and {node_1.next_node.next_node}')

    return node_1.next_node.node_id * node_1.next_node.next_node.node_id


def phase_2_namedtuple(cups: List[int], moves: int):
    print(cups)
    # More moves (10M)
    moves = 10_000_000
    # More cups (1M total)
    cups = cups + list(range(max(cups)+1, 1_000_001))
    #
    min_cup_value = min(cups)
    max_cup_value = max(cups)
    cup_map: Dict[int: Cup] = dict()

    print(f'Creating cup map ({len(cups)})')
    for i, cup in enumerate(cups[:-1]):
        cup_map[cup] = Cup(cup, cups[i+1])
    cup_map[cups[-1]] = Cup(cups[-1], cups[0])

    current_cup: Cup = cup_map[cups[0]]
    print(f'Cups done, first = {current_cup}')

    for move in range(moves):
        if move % 250000 == 0:
            print(f'Move {move}')
        # print(current_cup)
        # pick up 3 nodes after current_node
        pick_up_node = cup_map[current_cup.next]
        new_next_node_value = cup_map[cup_map[cup_map[current_cup.next].next].next].next
        current_cup = Cup(current_cup.value, new_next_node_value)
        # print(f'CC: {current_cup}')
        cup_map[current_cup.value] = current_cup
        pick_up_values = [pick_up_node.value, pick_up_node.next, cup_map[pick_up_node.next].next]

        # Find destination
        destination_cup_value = current_cup.value - 1
        while destination_cup_value < min_cup_value or destination_cup_value in pick_up_values:
            if destination_cup_value < min_cup_value:
                destination_cup_value = max_cup_value + 1
            destination_cup_value -= 1
        destination_cup = cup_map[destination_cup_value]
        # Put picked up cups after destination
        new_dest_cup = Cup(destination_cup.value, pick_up_node.value)
        new_last_picked_up_cup = Cup(pick_up_values[2], destination_cup.next)
        cup_map[destination_cup.value] = new_dest_cup
        cup_map[new_last_picked_up_cup.value] = new_last_picked_up_cup
        # Set new current_node
        current_cup = cup_map[current_cup.next]
    cup_1 = cup_map[1]
    print(f'Nodes after {cup_1} are {cup_1.next} and {cup_map[cup_1.next].next}')

    return cup_1.next * cup_map[cup_1.next].next

def phase_2(cups: List[int], moves: int):
    print(cups)
    # More moves (10M)
    moves = 10_000_000
    # More cups (1M total)
    cups = cups + list(range(max(cups)+1, 1_000_001))
    #
    min_cup_value = min(cups)
    max_cup_value = max(cups)
    cup_map: Dict[int: List[int]] = dict()

    print(f'Creating cup map ({len(cups)})')
    for i, cup in enumerate(cups[:-1]):
        cup_map[cup] = [cup, cups[i+1]]
    cup_map[cups[-1]] = [cups[-1], cups[0]]

    current_cup_value, current_cup_next = cup_map[cups[0]]
    print(f'Cups done, first = {current_cup_value} -> {current_cup_next}')

    for move in range(moves):
        if move % 500000 == 0:
            print(f'Move {move}')
        # pick up 3 nodes after current_node
        pick_up_cup = cup_map[current_cup_next]
        current_cup_next = cup_map[cup_map[pick_up_cup[1]][1]][1]
        cup_map[current_cup_value][1] = current_cup_next
        pick_up_values = [pick_up_cup[0], pick_up_cup[1], cup_map[pick_up_cup[1]][1]]

        # Find destination
        destination_cup_value = current_cup_value - 1
        while destination_cup_value < min_cup_value or destination_cup_value in pick_up_values:
            if destination_cup_value < min_cup_value:
                destination_cup_value = max_cup_value + 1
            destination_cup_value -= 1
        destination_cup = cup_map[destination_cup_value]
        # Put picked up cups after destination
        cup_map[destination_cup[0]][1], cup_map[pick_up_values[2]][1] = pick_up_cup[0], destination_cup[1]
        # Set new current_node
        current_cup_value, current_cup_next = cup_map[current_cup_next]
    cup_1 = cup_map[1]
    print(f'Nodes after {cup_1} are {cup_1[1]} and {cup_map[cup_1[1]][1]}')

    return cup_1[1] * cup_map[cup_1[1]][1]


def execute(input: str, moves: int):
    cups = list(map(int, list(input)))
    p1 = phase_1(cups, moves)
    print(f"Phase 1: {p1}")
    if moves == 100:
        p2 = phase_2_faster(cups, moves)
        print(f"Phase 2: {p2} ")


if __name__ == "__main__":
    for day_input in [
            ("389125467", 10),
            # ("389125467", 100),
            ("942387615", 100)
        ]:
        print(f"For {day_input[0]} with {day_input[1]} moves:")
        execute(day_input[0], day_input[1])
        print("..............")


# Answers
# 1: 36542897
# 2: 562136730660
