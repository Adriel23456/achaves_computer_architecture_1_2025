# instruction_memory.py
from __future__ import annotations
from typing import List

class InstructionMemory:
    """
    Instruction Memory (ROM) de 64-bits:
        • Cada instrucción ocupa 8 bytes (64 bits).
        • La lectura es puramente combinacional: dado un address A,
          se entrega inmediatamente la palabra de 64 bits que
          comienza en la dirección A alineada a 8.

    Interfaz (igual al diagrama):
        Entradas
            A   : dirección de 32 bits (generalmente PCF)
        Salidas
            RD  : InstrF – palabra de 64 bits leída
    """

    def __init__(self, words64: List[int] | None = None):
        """
        Crea una ROM con la lista de palabras de 64 bits indicada.
        Cada elemento de `words64` → una instrucción.
        Si None, se crea vacía (todo 0’s).
        """
        self._mem: List[int] = words64[:] if words64 else []

    # ─────────────────────────────────────────────
    # Lectura combinacional
    # ─────────────────────────────────────────────
    def read(self, addr: int) -> int:
        """
        Devuelve la instrucción de 64 bits almacenada en `addr`.
        `addr` debe estar alineada a 8 bytes.

        Ejemplo hardware:
            InstrF = imem.read(PCF)
        """
        if addr & 0x7:
            raise ValueError("Instruction address debe estar alineada a 8 bytes.")
        index = addr >> 3  # divide entre 8
        if index >= len(self._mem):
            return 0  # fetch fuera de rango → 0 (NOP)
        return self._mem[index] & 0xFFFFFFFFFFFFFFFF

    # ─────────────────────────────────────────────
    # Métodos utilitarios para carga/debug
    # ─────────────────────────────────────────────
    def load(self, words64: List[int], start_addr: int = 0):
        """
        Carga / sobre-escribe instrucciones a partir de `start_addr`
        (en bytes, alineado a 8).
        """
        if start_addr & 0x7:
            raise ValueError("start_addr debe estar alineado a 8.")
        base = start_addr >> 3
        end  = base + len(words64)
        if end > len(self._mem):
            self._mem.extend([0]*(end - len(self._mem)))
        self._mem[base:end] = [w & 0xFFFFFFFFFFFFFFFF for w in words64]

    def size(self) -> int:
        """Devuelve el tamaño actual en instrucciones de 64 bits."""
        return len(self._mem)

    def dump(self) -> List[int]:
        """Devuelve una copia de toda la ROM (lista de ints de 64 bits)."""
        return self._mem.copy()
