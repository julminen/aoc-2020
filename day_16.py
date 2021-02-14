#!/usr/bin/python3

from typing import List, Tuple
from collections import namedtuple


class Rule:
    """Validation rule"""

    def __init__(self, definition: str):
        self.name, self.rule = definition.split(": ")
        low, high = self.rule.split(" or ")
        a, b = map(int, low.split("-"))
        c, d = map(int, high.split("-"))
        # Define a function for validating
        self.check = lambda i: a <= i and i <= b or c <= i and i <= d

    def __repr__(self):
        return f"{self.name}: {self.rule}, {self.check}"


class Ticket:
    def __init__(self, definition: str):
        self.values = list(map(int, definition.split(",")))

    def is_valid(self, rules: List[Rule]) -> bool:
        """Check if all ticket values pass some of the given Rules

        Args:
            rules (Rule): List of validation Rules which need to be passed

        Returns:
            bool: True, if all ticket values pass some Rules
        """
        for value in self.values:
            value_is_valid = False
            for rule in rules:
                if rule.check(value):
                    value_is_valid = True
                    break
            if not value_is_valid:
                return False
        return True

    def get_invalid_values(self, rules: List[Rule]) -> List[int]:
        """Return values which do not pass any given Rules

        Args:
            rules (Rule): List of validation Rules to check against

        Returns:
            list: list of values which did not pass any Rules
        """
        invalids = list()
        if not self.is_valid(rules):
            for value in self.values:
                valid = False
                for rule in rules:
                    if rule.check(value):
                        valid = True
                        break
                if not valid:
                    invalids.append(value)
        return invalids

    def field_validity(self, rule: Rule) -> List[bool]:
        """Find which columns pass given rule

        Args:
            rule (Rule): The Rule to check against

        Returns:
            list: List of Boolean values, one for each value and value telling if it passes the Rule or not
        """
        return [rule.check(x) for x in self.values]

    def __repr__(self):
        return f"{self.values}"


def read_file(day: str) -> Tuple[List[Rule], Ticket, List[Ticket]]:
    with open(f"input/day_{day}.txt") as file:
        lines = [line.strip() for line in file]
        blanks = 0
        rules = list()
        other_tikects = list()
        for l in lines:
            if len(l) == 0:
                blanks += 1
                continue
            if blanks == 0:
                rules.append(Rule(l))
            elif blanks == 1:
                if l.startswith("your"):
                    continue
                my_ticket = Ticket(l)
            elif blanks == 2:
                if l.startswith("nearby"):
                    continue
                other_tikects.append(Ticket(l))
        return rules, my_ticket, other_tikects


def phase_1(input: Tuple[List[Rule], Ticket, List[Ticket]]) -> int:
    rules = input[0]
    other_tickets = input[2]
    # completely invalid values
    invalid_values = list()
    for ticket in other_tickets:
        invalids = ticket.get_invalid_values(rules)
        # print(f'Invalid in {ticket}: {invalids}')
        invalid_values.extend(invalids)
    return sum(invalid_values)


def solve_rule_validity(matrix: List[bool], rows: int, columns: int):
    """Solve the rule validity. Given matrix should contain one row per each rule
     and each column for each ticket value. Matrix tells whether the rule is valid
     for that ticket value or not.

    Args:
        matrix (List[bool]): One-dimensional array of boolean values. Modified in place
        rows (int): Number of rows in matrix
        columns (int): Number of columns in matrix
    """
    # Assuming only possible true values in matrix
    # Iterate over rows until each row has only one True value
    # For each column, if column contains only one True value, on that row set other to False
    # If there are multiple correct combinations this algorithm probably won't end
    print(f"{rows} x {columns}")
    modifications = True
    while modifications:
        modifications = False
        for r in range(rows):
            row_start = r * columns
            row_end = r * columns + columns
            row = matrix[row_start:row_end]
            # If number of possible trues per rule is more than one, process row
            if row.count(True) > 1:
                # Check each column for just one True
                for c in range(columns):
                    column = matrix[c::rows]
                    # Only one ticket field can be True for one Rule
                    # Indexes to rows which are true
                    fix_rows = [i for i, v in enumerate(column) if v]
                    # If there is only one, the rule must be valid for only that field
                    if len(fix_rows) == 1:
                        # Create and set the row to contain only one True
                        fix_row_start = fix_rows[0] * columns
                        fix_row_end = fix_row_start + columns
                        new_row = [False] * columns
                        new_row[c] = True
                        matrix[fix_row_start:fix_row_end] = new_row
                        # Modifications made, need to check the matrix again
                        modifications = True


def phase_2(input: Tuple[List[Rule], Ticket, List[Ticket]]) -> int:
    rules = input[0]
    my_ticket: Ticket = input[1]
    valid_tickets: List[Ticket] = [
        ticket for ticket in input[2] if ticket.is_valid(rules)
    ]
    valid_tickets.append(my_ticket)
    print(f"Valid tickets: {len(valid_tickets)}")

    rule_validity = list()
    # Phase 1: check which are valid columns for rules
    # This results in 2D matrix of rules x ticket fields so 20x20 but stored as continuous
    # array for easier manipulation
    rows = len(rules)
    columns = len(valid_tickets[0].values)
    for rule in rules:
        validity = [True] * len(valid_tickets[0].values)
        for ticket in valid_tickets:
            ticket_field_validity = ticket.field_validity(rule)
            validity = [c[0] and c[1] for c in zip(ticket_field_validity, validity)]
        rule_validity.extend(validity)

    # Phase 2:
    solve_rule_validity(rule_validity, rows, columns)

    # We have the data. Now go through the "departure" rules and find the values for end result
    return_value = 1
    for i, rule in enumerate(rules):
        if rule.name.startswith("departure"):
            # Calculate the correct location in "matrix"
            start = i * columns
            end = i * columns + columns
            rule_index = rule_validity[start:end].index(True)
            ticket_value = my_ticket.values[rule_index]
            # print(f"{rule.name}: field {rule_index} -> value {ticket_value}")
            return_value = return_value * ticket_value
    return return_value


def execute(input):
    p1 = phase_1(input)
    print(f"Phase 1: {p1}\n")

    p2 = phase_2(input)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    for day_input in ["16_s", "16_s2", "16"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")
