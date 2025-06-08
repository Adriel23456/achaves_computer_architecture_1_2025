# data_memory.py
from __future__ import annotations
from typing import List, Optional

# ─── Parámetros ───────────────────────────────────────────
BLOCK_BITS  = 32
NUM_BLOCKS  = 64
BLOCK_MASK  = (1 << BLOCK_BITS) - 1  # 0xFFFFFFFF

class DataMemory:
    """
    Data Memory: 64 bloques de 32 bits (total: 256 bytes).

    • Lectura combinacional: RD_G ← memoria[A_G]
    • Escritura sincrónica: ocurre al tick si WE_G = 1

    Señales externas (según diagrama):
        - A_G   : dirección de acceso (5 bits)
        - WD_G  : dato a escribir (32 bits)
        - WE_G  : write enable (1 bit)
        - RD_G  : salida combinacional (32 bits)
    """

    def __init__(self):
        self._mem: List[int] = [0] * NUM_BLOCKS
        self._pending: Optional[tuple[int, int]] = None  # (idx, value)

    # Lectura combinacional
    def read(self, A_G: int) -> int:
        idx = A_G & 0x3F  # 6 bits para rango 0–63
        return self._mem[idx]

    # Escritura latcheada (espera flanco)
    def write(self, A_G: int, WD_G: int, WE_G: int):
        if not WE_G:
            return
        idx = A_G & 0x3F
        data = WD_G & BLOCK_MASK
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
