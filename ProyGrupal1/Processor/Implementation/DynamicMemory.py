from __future__ import annotations
from typing import List, Optional
from Flags import Flags


class DynamicMemory:
    def __init__(self, flags: Flags, memory_size: int = 64, block_bits: int = 64):
        self._flags = flags
        self._memory_size = memory_size          # equivale a NUM_BLOCKS
        self._block_bits = block_bits            # equivale a BLOCK_BITS
        self._block_mask = (1 << block_bits) - 1 # equivale a BLOCK_MASK

        self._mem: List[int] = [0] * self._memory_size
        self._pending: Optional[tuple[int, int]] = None  # (idx, value)

    # ─── Getters y Setters de parámetros internos ───────────────────────

    def set_memory_size(self, new_size: int):
        if new_size < len(self._mem):
            raise ValueError("No se puede reducir el tamaño de memoria existente.")
        self._memory_size = new_size
        self._mem.extend([0] * (new_size - len(self._mem)))

    def get_memory_size(self) -> int:
        return self._memory_size

    def set_block_bits(self, bits: int):
        self._block_bits = bits
        self._block_mask = (1 << bits) - 1

    def get_block_bits(self) -> int:
        return self._block_bits

    def get_block_mask(self) -> int:
        return self._block_mask

    # ─── Señales principales ─────────────────────────────────────────────

    def read(self, A_D: int) -> int:
        if self._flags.enabled() != 1:
            raise PermissionError("Lectura denegada: S1/S2 inactivos.")
        idx = A_D % self._memory_size
        return self._mem[idx]

    def write(self, A_D: int, WD_D: int, WE_D: int):
        if not WE_D:
            return
        if self._flags.enabled() != 1:
            raise PermissionError("Escritura denegada: S1/S2 inactivos.")
        idx = A_D % self._memory_size
        data = WD_D & self._block_mask
        self._pending = (idx, data)

    def tick(self):
        if self._pending is not None:
            idx, data = self._pending
            self._mem[idx] = data
            self._pending = None

    # ─── Utilidades opcionales ──────────────────────────────────────────

    def dump(self) -> List[int]:
        return self._mem.copy()

    def load(self, values: List[int], base: int = 0):
        for i, val in enumerate(values):
            if base + i < self._memory_size:
                self._mem[base + i] = val & self._block_mask
