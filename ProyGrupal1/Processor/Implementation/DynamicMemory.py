# data_memory.py
from __future__ import annotations
from typing import List, Optional
from Flags import Flags


def load_Memory_Size():
    return 64
#TODO >>> no entiendo bien como estamos cargando cosas del excel aun, para cuando este hacerlo aqui y que asigne el valor a los parametro que esta cosa ocupa


# ─── Parámetros ───────────────────────────────────────────
BLOCK_BITS  = 64
NUM_BLOCKS  = load_Memory_Size()
BLOCK_MASK  = (1 << BLOCK_BITS) - 1  # 0xFFFFFFFF

class DataMemory:


#señales para luego no confundirme
# - A_D   : dirección de acceso (5 bits)
# - WD_G  : dato a escribir (32 bits)
# - WE_G  : write enable (1 bit)
# - RD_G  : salida combinacional (32 bits)


    def __init__(self, flags: Flags):
        self._flags = flags
        self._mem: List[int] = [0] * NUM_BLOCKS
        self._pending: Optional[tuple[int, int]] = None  # (idx, value)

    # Lectura combinacional
    def read(self, A_D: int) -> int:
        if self._flags.enabled() != 1:
            raise PermissionError("Lectura denegada: S1/S2 inactivos.")
        idx = A_D & 0x3F  # 6 bits para rango 0–63
        return self._mem[idx]

    # Escritura latcheada (espera flanco) y tambien espera la activacion de flags
    def write(self, A_D: int, WD_D: int, WE_D: int):
        if not WE_D:
            return
        if self._flags.enabled() != 1:
            raise PermissionError("Escritura denegada: S1/S2 inactivos.")
        idx = A_D & 0x3F
        data = WD_D & BLOCK_MASK
        self._pending = (idx, data)

    # Flanco de reloj: aplica escritura
    def tick(self):
        if self._pending is not None:
            idx, data = self._pending
            self._mem[idx] = data
            self._pending = None

    # Utilidades opcionales
    def dump(self) -> List[int]:
        return self._mem.copy()

    def load(self, values: List[int], base: int = 0):
        for i, val in enumerate(values):
            if base + i < NUM_BLOCKS:
                self._mem[base + i] = val & BLOCK_MASK
