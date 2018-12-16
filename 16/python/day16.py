"""
Advent of Code 2018
Day 16: Chronal Classification
"""
from collections import namedtuple

Sample = namedtuple('Sample', ['before', 'instruction', 'after'])
Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])


def parse_input_file(input_lines):
    "Parse the input file."
    samples = []
    index = 0
    while index < len(input_lines):
        if input_lines[index].strip() == '':
            break
        samples.append(parse_sample(input_lines[index:index+3]))
        index += 4
    program = []
    while index < len(input_lines):
        line = input_lines[index].strip()
        if line:
            program.append(line)
        index += 1
    return samples, program





def parse_sample(input_lines):
    "Parse three input lines into a Sample."
    assert len(input_lines) == 3
    before = tuple([int(i) for i in input_lines[0].strip()[9:-1].split(', ')])
    instruction = Instruction(*(int (i) for i in input_lines[1].strip().split()))
    after = tuple([int(i) for i in input_lines[2].strip()[9:-1].split(', ')])
    return Sample(before, instruction, after)


# Addition:
def addr(a, b, c, registers):
    """
    addr (add register) stores into register C the result of
    adding register A and register B.
    """
    registers[c] = registers[a] + registers[b]


def addi(a, b, c, registers):
    """
    addi (add immediate) stores into register C the result of
    adding register A and value B.
    """
    registers[c] = registers[a] + b

# Multiplication:

def mulr(a, b, c, registers):
    """
    mulr (multiply register) stores into register C the result of
    multiplying register A and register B.
    """
    registers[c] = registers[a] * registers[b]


def muli(a, b, c, registers):
    """
    muli (multiply immediate) stores into register C the result of
    multiplying register A and value B.
    """
    registers[c] = registers[a] * b

# Bitwise AND:

def banr(a, b, c, registers):
    """
    banr (bitwise AND register) stores into register C the result of
    the bitwise AND of register A and register B.
    """
    registers[c] = registers[a] & registers[b]


def bani(a, b, c, registers):
    """
    bani (bitwise AND immediate) stores into register C the result of
    the bitwise AND of register A and value B.
    """
    registers[c] = registers[a] & b

# Bitwise OR:

def borr(a, b, c, registers):
    """
    borr (bitwise OR register) stores into register C the result of
    the bitwise OR of register A and register B.
    """
    registers[c] = registers[a] | registers[b]

def bori(a, b, c, registers):
    """
    bori (bitwise OR immediate) stores into register C the result of
    the bitwise OR of register A and value B.
    """
    registers[c] = registers[a] | b

# Assignment:

def setr(a, b, c, registers):
    """
    setr (set register) copies the contents of register A
    into register C. (Input B is ignored.)
    """
    registers[c] = registers[a]

def seti(a, b, c, registers):
    """
    seti (set immediate) stores value A into register C.
    (Input B is ignored.)
    """
    registers[c] = a

# Greater-than testing:

def gtir(a, b, c, registers):
    """
    gtir (greater-than immediate/register) sets register C to 1
    if value A is greater than register B. Otherwise, register C is set to 0.
    """
    if a > registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0

def gtri(a, b, c, registers):
    """
    gtri (greater-than register/immediate) sets register C to 1
    if register A is greater than value B. Otherwise, register C is set to 0.
    """
    if registers[a] > b:
        registers[c] = 1
    else:
        registers[c] = 0

def gtrr(a, b, c, registers):
    """
    gtrr (greater-than register/register) sets register C to 1
    if register A is greater than register B. Otherwise, register C is set to 0.
    """
    if registers[a] > registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0

# Equality testing:

def eqir(a, b, c, registers):
    """
    eqir (equal immediate/register) sets register C to 1
    if value A is equal to register B. Otherwise, register C is set to 0.
    """
    if a == registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0

def eqri(a, b, c, registers):
    """
    eqri (equal register/immediate) sets register C to 1
    if register A is equal to value B. Otherwise, register C is set to 0.
    """
    if registers[a] == b:
        registers[c] = 1
    else:
        registers[c] = 0

def eqrr(a, b, c, registers):
    """
    eqrr (equal register/register) sets register C to 1
    if register A is equal to register B. Otherwise, register C is set to 0.
    """
    if registers[a] == registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0

OPERATIONS = dict([('addr', addr), ('addi', addi),
                   ('mulr', mulr), ('muli', muli),
                   ('banr', banr), ('bani', bani),
                   ('borr', borr), ('bori', bori),
                   ('setr', setr), ('seti', seti),
                   ('gtir', gtir), ('gtri', gtri), ('gtrr', gtrr),
                   ('eqir', eqir), ('eqri', eqri), ('eqrr', eqrr)])

def find_valid_ops(sample):
    "Find the valid operations for given sample."
    possible_ops = []
    expected = list(sample.after)
    for name, fun in OPERATIONS.items():
        a, b, c = sample.instruction.a, sample.instruction.b, sample.instruction.c
        registers = list(sample.before)
        fun(a, b, c, registers)
        if registers == expected:
            possible_ops.append(name)
    return possible_ops


def solve_a(samples):
    "Solve first part of puzzle."
    soln = 0
    for sample in samples:
        valid_ops = find_valid_ops(sample)
        if len(valid_ops) >= 3:
            soln += 1
    return soln


def solve_b(samples, program):
    "Solve second part of puzzle."
    opcodes = set()
    opcode_abbr = [set(OPERATIONS.keys()) for _ in range(16)]
    for sample in samples:
        opcodes.add(sample.instruction.opcode)
        valid_ops = set(find_valid_ops(sample))
        opcode_abbr[sample.instruction.opcode] &= valid_ops

    while max(len(abbr) for abbr in opcode_abbr) > 1:
        for opcode, abbr in enumerate(opcode_abbr):
            if len(abbr) == 1:
                for opcode0, abbr0 in enumerate(opcode_abbr):
                    if opcode != opcode0:
                        abbr0.difference_update(abbr)

    opcode_abbr = [a.pop() for a in opcode_abbr]
    assert sorted(opcode_abbr) == sorted(OPERATIONS.keys())
    registers = [0, 0, 0, 0]
    for line in program:
        opcode, a, b, c = (int(i) for i in line.split())
        opabbr = opcode_abbr[opcode]
        fun = OPERATIONS[opabbr]
        fun(a, b, c, registers)
    return(registers[0])



def main():
    "Main program."
    import sys
    input_lines = sys.stdin.readlines()
    samples, program = parse_input_file(input_lines)
    print(solve_a(samples))
    print(solve_b(samples, program))


if __name__ == '__main__':
    main()
