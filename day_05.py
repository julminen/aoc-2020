#!/usr/bin/python3


class BoardingPass:
    def __init__(self, code: str):
        str_row, str_column = code[:7], code[7:]
        self.row = int(str_row.replace('F', '0').replace('B', '1'), 2)
        self.column = int(str_column.replace('L', '0').replace('R', '1'), 2)
        self.seat_id = self.row * 8 + self.column

    def __repr__(self) -> str:
        return f'Row {self.row}, seat {self.column}, ID: {self.seat_id}'
    
    def get_id(self) -> int:
        return self.seat_id
    
    def get_row(self) -> int:
        return self.row
    
    def get_column(self) -> int:
        return self.column


def read_input():
    with open(f'input/day_05.txt') as f:
        passes = [BoardingPass(l) for l in f]
    return passes

def phase_1(boarding_passes):
    return max(boarding_passes, key=BoardingPass.get_id)

def phase_2(boarding_passes):
    ids = sorted([bp.get_id() for bp in boarding_passes])
    print(ids)
    min_id = ids[0]
    max_id = ids[-1]
    for i in range(min_id+1, max_id):
        if i not in ids:
            print(f'puuttuu: {i}')
    

if __name__ == "__main__":
    passes = read_input()
    print(f'Phase 1 - max seat ID: {phase_1(passes)}')
    phase_2(passes)