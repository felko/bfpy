#!/usr/bin/env python3.4
# coding: utf-8

class ParseError(ValueError):
    pass


class Instruction:
    _instr_types = {}

    def __init__(self, char):
        self.char = char

    def __str__(self):
        return self.char

    @classmethod
    def register_simple(cls, char):
        def _instr_wrapper(instr_type):
            instr_type.__str__ = lambda self: char
            instr_type.consume = classmethod(lambda cls, chars: cls() if chars.pop(0) == char else None)
            return cls.register(instr_type)
        return _instr_wrapper

    @classmethod
    def register(cls, instr_type):
        setattr(cls, instr_type.__name__, instr_type)
        cls._instr_types[instr_type.__name__] = instr_type
        return instr_type

    @staticmethod
    def consume(chars):
        for instr_type in Instruction._instr_types.values():
            tmp = chars[:]
            try:
                instr = instr_type.consume(tmp)

                if instr is None:
                    raise ParseError('consume returned None')
            except IndexError:
                raise ParseError('Unexpected EOF')
            except ParseError:
                continue
            else:
                chars[:] = tmp
                return instr

        raise ParseError('Failed to parse instruction')

    @staticmethod
    def read_many(string):
        instrs = []
        chars = list(string)

        while chars:
            instr = Instruction.consume(chars)
            instrs.append(instr)

        return instrs


@Instruction.register_simple('+')
class INCR:
    pass

@Instruction.register_simple('-')
class DECR:
    pass

@Instruction.register_simple('<')
class PREV:
    pass

@Instruction.register_simple('>')
class NEXT:
    pass

@Instruction.register_simple('.')
class PUTC:
    pass

@Instruction.register_simple(',')
class GETC:
    pass

@Instruction.register
class LOOP:
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        return '[{}]'.format(''.join(map(str, self.instructions)))

    @classmethod
    def consume(cls, chars):
        instrs = []

        if chars.pop(0) == '[':
            while chars[0] != ']':
                instr = Instruction.consume(chars)
                instrs.append(instr)
            chars.pop(0)

            return cls(instrs)
