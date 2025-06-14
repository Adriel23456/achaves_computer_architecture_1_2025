# ExtraPrograms/Processor/DynamicMemory.py
from __future__ import annotations
from typing import Dict, List
from ExtraPrograms.Processor.Flags import Flags


class DynamicMemory:
    """
    Memoria dinámica protegida.

    ▸ Direcciones externas en **bytes**.  
    ▸ Operaciones de palabras de 32 bits (little-endian).  
    ▸ Accesos permitidos sólo si flags.enabled() == 1.
    """

    def __init__(self,
                 flags: Flags,
                 memory_size: int = 64,      # nº de bloques
                 block_bits: int = 64):      # bits por bloque (8 bytes)
        self._flags = flags
        self._mem_size = memory_size
        self._block_bits = block_bits
        self._bytes_per_block = block_bits // 8
        self._block_mask = (1 << block_bits) - 1

        self._mem: List[int] = [0] * self._mem_size          # contenido estable
        self._pending: Dict[int, int] = {}                   # idx → nuevo valor

    # ───────────────────────── helpers internas ──────────────────────────
    def _split_addr(self, addr: int) -> tuple[int, int]:
        if not (0 <= addr < self._mem_size * self._bytes_per_block):
            raise ValueError(f"Dirección fuera de rango: {addr}")
        idx = addr // self._bytes_per_block
        off = addr %  self._bytes_per_block
        return idx, off

    def _require_auth(self) -> None:
        if self._flags.enabled() != 1:
            raise PermissionError("Lectura/Escritura denegada: S1/S2 inactivos.")

    # ───────────────────────────── API pública ───────────────────────────
    def read(self, A_D: int) -> int:
        self._require_auth()

        idx, off = self._split_addr(A_D)
        val = 0
        for i in range(4):                              # 4 bytes → 32 bits
            a = A_D + i
            b_idx, b_off = self._split_addr(a)
            word = self._mem[b_idx]
            byte = (word >> (8 * b_off)) & 0xFF
            val |= byte << (8 * i)
        return val & 0xFFFFFFFF

    def write(self, A_D: int, WD_D: int, WE_D: int) -> None:
        if not WE_D:                                    # ⬅️  **cambio clave**
            return
        self._require_auth()

        wd = WD_D & 0xFFFFFFFF
        for i in range(4):
            addr_byte = A_D + i
            b_idx, b_off = self._split_addr(addr_byte)
            byte_val = (wd >> (8 * i)) & 0xFF

            cur = self._pending.get(b_idx, self._mem[b_idx])
            shift = b_off * 8
            mask  = 0xFF << shift
            new_word = (cur & ~mask) | (byte_val << shift)
            self._pending[b_idx] = new_word & self._block_mask

    def tick(self) -> None:
        for idx, val in self._pending.items():
            self._mem[idx] = val
        self._pending.clear()

    # ───────────────────── Gestión dinámica (opc) ───────────────────────
    def set_memory_size(self, new_size: int) -> None:
        if new_size < self._mem_size:
            raise ValueError("No se puede reducir el tamaño existente.")
        self._mem.extend([0] * (new_size - self._mem_size))
        self._mem_size = new_size

    def set_block_bits(self, bits: int) -> None:
        if bits % 8 != 0:
            raise ValueError("block_bits debe ser múltiplo de 8.")
        self._block_bits = bits
        self._bytes_per_block = bits // 8
        self._block_mask = (1 << bits) - 1

    # ───────────────────────── utilidades ────────────────────────────────
    def dump(self) -> List[int]:
        return self._mem.copy()

    def load(self, values: List[int], base: int = 0) -> None:
        for i, v in enumerate(values):
            if base + i < self._mem_size:
                self._mem[base + i] = v & self._block_mask
