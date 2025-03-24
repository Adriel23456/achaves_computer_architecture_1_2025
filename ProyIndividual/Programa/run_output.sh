#!/bin/bash

# Compile
nasm -f elf64 -o lfsr.o lfsr.asm
ld -o lfsr lfsr.o

# Run program and capture output
./lfsr > raw_output.txt

echo "Process completed. Values written to raw_output.txt"