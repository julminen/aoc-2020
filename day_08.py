#!/usr/bin/python3

class VMachine:
    def __init__(self, program: list):
        self.acc: int = 0
        self.ip: int = 0
        self.program = program
        self.status = 1
        self.step_counter = 0
    
    def step(self):
        self.program[self.ip].execute(self)
    
    def run_until_end(self):
        self.acc = 0
        self.ip = 0
        self.status = 1
        self.step_counter = 0
        states = set()
        while self.ip not in states:
            if self.ip >= len(self.program):
                if self.ip == len(self.program):
                    self.status = 0
                else:
                    self.status = 2
                break
            states.add(self.ip)
            self.program[self.ip].execute(self)
            self.step_counter += 1

class Instruction:
    def __init__(self, cmd: str, parameter: int):
        self.parameter = int(parameter)
        self.cmd = cmd
        if cmd == 'acc':
            self.execute = self.add_op
        elif cmd == 'jmp':
            self.execute = self.jmp_op
        elif cmd == 'nop':
            self.execute = self.nop_op

    def add_op(self, machine: VMachine):
        machine.acc += self.parameter
        machine.ip += 1
    
    def jmp_op(self, machine: VMachine):
        machine.ip += self.parameter
    
    def nop_op(self, machine: VMachine):
        machine.ip += 1


def read_file():
    with open(f'input/day_08.txt') as file:
        instructions = list()
        for line in list(map(str.strip, file.readlines())):
            op, param = line.split()
            instructions.append(Instruction(op, int(param)))
    return VMachine(instructions)


def phase_1(vm: VMachine):
    vm.run_until_end()
    print(f'Phase 1: acc at stop: {vm.acc} state {vm.status}, executed {vm.step_counter} steps')


def phase_2(vm: VMachine):
    prog = vm.program
    jmps = 0
    nops = 0
    for p in range(len(prog)):
        op = prog[p].execute
        if prog[p].cmd == 'jmp':
            jmps += 1
            prog[p].execute = prog[p].nop_op
        elif prog[p].cmd == 'nop':
            nops += 1
            prog[p].execute = prog[p].jmp_op
        else:
            continue
        vm.run_until_end()
        prog[p].execute = op
        if vm.status == 0:
            print(f'Phase 2: instruction {p} changed: acc at stop: {vm.acc} state {vm.status}, executed {vm.step_counter} steps')
            break
    print(f'Tested jmps: {jmps}, nops: {nops}')


if __name__ == "__main__":
    vm = read_file()
    phase_1(vm)
    phase_2(vm)
