from Processor import Procesador
from struct import unpack
from pathlib import Path
import sys
# Instancia CPU
cpu = Procesador()

def bin_to_prog_list(bin_path: str):
    data = Path(bin_path).read_bytes()
    if len(data) % 8:
        raise ValueError("El archivo no tiene múltiplos de 8 bytes.")

    words = []
    for i in range(0, len(data), 8):
        word = unpack(">Q", data[i:i+8])[0]     # 64-bit little-endian
        words.append(word)                      # ← entero, no string
    return words

output = bin_to_prog_list(sys.argv[1])
print("Contenido de la instrucción binaria (prog):")
for idx, instr in enumerate(output):
    print(f"{idx:02d}: 0x{instr:016X}")

# Cargamos la ROM a partir de la dirección 0
cpu.instruction_memory.load(output, start_addr=0)

# Ejecutamos –-máx. 20 ciclos para este ejemplo
cpu.run_all(max_cycles=385)
print("Final state of RegisterFile:", cpu.register_file.debug())