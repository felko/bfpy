#!/usr/bin/env python3.4
# coding: utf-8

import dis
from bfpy.instruction import Instruction


class Bytecode:
    _transpilers = {}

    def __init__(self, instructions=()):
        self.instructions = list(instructions)
        self.symbols = {}

    def __str__(self):
        s = ''

        for instr in self.instructions:
            s += str(instr)

        return s

    @classmethod
    def transpile(cls, py_op):
        def _transpiler_wrapper(fn):
            cls._transpilers[py_op] = fn
            return fn

        return _transpiler_wrapper

    def transpile_instruction(self, py_op):
        transpile = self._transpilers[py_op.opname]
        transpiled = transpile(self, py_op)

        if isinstance(transpiled, str):
            transpiled = Instruction.read_many(transpiled)

        return transpiled

    @classmethod
    def from_function(cls, function, **names):
        bytecode = cls()
        bytecode.symbols = names

        for instr in dis.get_instructions(function):
            transpiled = bytecode.transpile_instruction(instr)
            bytecode.instructions.extend(transpiled)

        return bytecode


@Bytecode.transpile('NOP')
def _(code, nop):
    return ''

@Bytecode.transpile('POP_TOP')
def _(code, pop):
    return '[-]<'

@Bytecode.transpile('ROT_TWO')
def _(code, rot2):
    return '<[->>+<<]>[<+>-]>[<+>-]<'

@Bytecode.transpile('ROT_THREE')
def _(code, rot3):
    return '<<[->>>+<<<]>[->>>+<<<]>[<<+>>-]>[<<+>>-]>[<<+>>-]<<'

@Bytecode.transpile('DUP_TOP')
def _(code, dup):
    return '[->+>+<<]>>[<<+>>-]<'

@Bytecode.transpile('DUP_TOP_TWO')
def _(code, dup2):
    return '<[->>+>>+<<<<]>>>>[<<<<+>>>>-]<<<[->>+>>+<<<<]>>>>[<<<<+>>>>-]<<'

@Bytecode.transpile('BINARY_ADD')
def _(code, add):
    return '[<+>-]<'

@Bytecode.transpile('BINARY_SUBTRACT')
def _(code, sub):
    return '[<->-]<'

@Bytecode.transpile('BINARY_MULTIPLY')
def _(code, mul):
    return '[-<[>>+>+<<<-]>>>[<<<+>>>-]<<]<[-]>>[-<<+>>]<<'

@Bytecode.transpile('BINARY_FLOOR_DIVIDE')
def _(code, div):
    return '[>+<-]<[->+>-[>+>>]>[+[-<+>]>+>>]<<<<<<]>>>>[<<<<+>>>>-]<<<[[-]>]<<<<'

@Bytecode.transpile('BINARY_POWER')
def _(code, pow):
    return '<[>>+>+>+<<<<-]>>>>[<<<<+>>>>-]<<<[>>[-<[>>+>+<<<-]>>>[<<<+>>>-]<<]<[-]>>[-<<+>>]<<<<[->>>+>+<<<<]>>>>[<<<<+>>>>-]<<<-]>>[-]<<<[-]>>[<<+>>-]<<'

@Bytecode.transpile('LOAD_CONST')
def _(code, load):
    return '>' + load.argval * '+'

@Bytecode.transpile('LOAD_FAST')
def _(code, load):
    return '>' + code.symbols[load.argval] * '+'

@Bytecode.transpile('RETURN_VALUE')
def _(code, return_):
    return ''
