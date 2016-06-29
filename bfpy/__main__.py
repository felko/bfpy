#!/usr/bin/env python3.4
# coding: utf-8

from bfpy.instruction import Instruction
from bfpy.bytecode import Bytecode
from bfpy.machine import Machine


def main():
    foo = lambda x, y, z: x * 6 + y - z
    bc = Bytecode.from_function(foo, x=8, y=4, z=5)   #47
    print(bc)
    vm = Machine(bc)
    vm.run()
    print(vm.current)


if __name__ == '__main__':
    main()
