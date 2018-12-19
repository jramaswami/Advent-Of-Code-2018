"""
Advent of Code 2018
Day 19: Go With The Flow
"""
from collections import namedtuple, defaultdict


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


Instruction = namedtuple('Instruction', ['abbr', 'fun', 'a', 'b', 'c'])


def parse_instruction(instruction):
    "Parse instruction"
    tokens = instruction.split()
    abbr = tokens[0]
    fun = OPERATIONS[abbr]
    a, b, c = (int(i) for i in tokens[1:])
    return Instruction(abbr, fun, a, b, c)


def execute(instructions, instruction_ptr, instruction_reg, registers):
    "Execute the given instruction."
    if instruction_ptr >= len(instructions):
        # print("ip={} {} HALT".format(instruction_ptr, registers))
        return -1

    registers[instruction_reg] = instruction_ptr
    instruction = instructions[instruction_ptr]
    # output = "ip={} {} {} {} {} {}".format(instruction_ptr, registers, instruction.abbr,
    #                                       instruction.a, instruction.b, instruction.c)
    instruction.fun(instruction.a, instruction.b, instruction.c, registers)
    # print("{} {}".format(output, registers))

    instruction_ptr = registers[instruction_reg]
    instruction_ptr += 1
    return instruction_ptr


def run_program(instructions, instruction_reg, registers):
    "Run the program"
    instruction_ptr = 0
    while instruction_ptr >= 0:
        instruction_ptr = execute(instructions, instruction_ptr, instruction_reg, registers)


def generate_dot(instructions, instruction_reg, registers):
    """
    Generates instructions for dot file for
    graphviz to generate call graph.
    """
    instruction_ptr = 0
    adj = defaultdict(set)
    while instruction_ptr >= 0:
        instruction_ptr0 = execute(instructions, instruction_ptr, instruction_reg, registers)
        adj[instruction_ptr].add(instruction_ptr0)
        instruction_ptr = instruction_ptr0

    print('digraph {')
    for u, children in adj.items():
        for v in children:
            print('\t', u, '->', v)
    print('}')


def solve_a(instructions, instruction_reg):
    "Solve first part of puzzle:  Actually executes assembly code."
    registers = [0, 0, 0, 0, 0, 0]
    run_program(instructions, instruction_reg, registers)
    return registers[0]


def solve_b(reg1):
    """"
    Solve second part of puzzle: Assembly program is summing the
    divisors of the initial number in register 1.
    """
    soln = 0
    for n in range(1, reg1 + 1):
        if reg1 % n == 0:
            soln += n
    return(soln)


def main():
    "Main program"
    import sys
    instruction_reg = int(sys.stdin.readline().strip()[4:])
    instructions = [parse_instruction(ln.strip()) for ln in sys.stdin]
    # generate_dot(instructions, instruction_reg, [0, 0, 0, 0, 0, 0])
    print(solve_a(instructions, instruction_reg))
    # register1 = 867 # a
    register1 = 10551267 #b
    print(solve_b(register1))


if __name__ == '__main__':
    main()
