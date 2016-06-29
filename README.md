![](http://puu.sh/pKqB0/1a702f3100.png)


bfpy
====


Python to Brainfuck transpiler

## What is BFPY

BFPY is an alternative Python runtime that uses Brainfuck as a bytecode.

## How does BFPY works ?

BFPY uses the standard `dis` module to disassemble a given Python function, and
translates one by one each bytecode instruction. It uses the Brainfuck memory as
a stack like a virtual machine would.

## Why BFPY ?

Boredom.

## What is currently implemented ?

For instance, BFPY can only translate arithmetic operations (addition,
subtraction, multiplication, floor division and power). There is still a lot
of features to implement for it to be a proper Python runtime alternative

## What remains to be implemented ?

I still have to translate more bytecode instruction to Brainfuck, but most can't
be translated as long as I don't allow Brainfuck to deal with more types (not
just bytes, but also characters, integers, lists, and maybe dictionaries).

I plan on implementing those types by loading the memory with a bytearray given
by a serialization of the said object, using `marshal`, but I don't know yet how
to expand a single stack element size to support multiple bytes.
