#!/bin/bash

# Default paths
INPUT_FILE="input.img"
OUTPUT_FILE="output.img"

# Check if inputs are provided
if [ $# -eq 2 ]; then
    INPUT_FILE="$1"
    OUTPUT_FILE="$2"
fi

# Create a copy of the assembly code file
cp output_gen.asm output_gen_mod.asm

# Update the paths in the copy
sed -i "s|input_file_path: db \"input.img\", 0|input_file_path: db \"$INPUT_FILE\", 0|" output_gen_mod.asm
sed -i "s|output_file_path: db \"output.img\", 0|output_file_path: db \"$OUTPUT_FILE\", 0|" output_gen_mod.asm

# Compile the modified assembly code
nasm -f elf64 -o output_gen.o output_gen_mod.asm

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Error: No se pudo compilar el código ensamblador."
    exit 1
fi

# Link the object file
ld -o output_gen output_gen.o

# Check if linking was successful
if [ $? -ne 0 ]; then
    echo "Error: No se pudo enlazar el código objeto."
    exit 1
fi

# Run the program
./output_gen

# Check if the program ran successfully
if [ $? -ne 0 ]; then
    echo "Error: No se pudo ejecutar el programa."
    exit 1
fi

# Clean up
rm -f output_gen.o output_gen output_gen_mod.asm

echo "Proceso completado. Se ha generado el archivo $OUTPUT_FILE."
exit 0