#!/usr/bin/env python3.4
# coding: utf-8

import dis
from functools import singledispatch

from bfpy.instruction import Instruction


class Machine:
    _executers = {}

    def __init__(self, bytecode, input='', allocate=256):
        self.bytecode = bytecode
        self.memory = bytearray(allocate)
        self.input = bytearray(input, encoding='utf-8')
        self.symbols = []
        self.constants = []
        self.cursor = 0

    @classmethod
    def execute(cls, instr):
        def _execute_wrapper(fn):
            cls._executers[instr] = fn
            return fn

        return _execute_wrapper

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value % len(self.memory)

    @property
    def current(self):
        return self.memory[self.cursor]

    @current.setter
    def current(self, value):
        self.memory[self.cursor] = value

    def execute_instr(self, instr):
        self._executers[type(instr)](self, instr)

    def run(self):
        for instr in self.bytecode.instructions:
            self.execute_instr(instr)


@Machine.execute(Instruction.INCR)
def _(self, incr):
    self.current += 1

@Machine.execute(Instruction.DECR)
def _(self, decr):
    self.current -= 1

@Machine.execute(Instruction.PREV)
def _(self, prev):
    self.cursor -= 1

@Machine.execute(Instruction.NEXT)
def _(self, next):
    self.cursor += 1

@Machine.execute(Instruction.PUTC)
def _(self, putc):
    char = chr(self.current)
    print(char, end='')

@Machine.execute(Instruction.GETC)
def _(self, getc):
    self.current = self.input.pop(0)

@Machine.execute(Instruction.LOOP)
def _(self, loop):
    while self.current:
        for instr in loop.instructions:
            self.execute_instr(instr)
