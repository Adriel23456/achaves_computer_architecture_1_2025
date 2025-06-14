# ExtraPrograms/Processor/DataMemory.py
from __future__ import annotations
from typing import Dict, List, Optional

BLOCK_BITS  = 32                      # 4 bytes por bloque
NUM_BLOCKS  = 64                      # 256 bytes en total (0-255)
BLOCK_MASK  = (1 << BLOCK_BITS) - 1   # 0xFFFFFFFF


class DataMemory:
    """
    Memoria de datos protegida de 64 × 32 bits.

    – **Direcciones en bytes** (0-255).  
    – Lectura combinacional de 32 bits comenzando en A_G.  
    – Escritura (32 bits) latcheada hasta `tick()`.  
    – Formato little-endian :
         byte 0 = bits 7-0  (dirección más baja)
         byte 3 = bits 31-24
    """

    def __init__(self) -> None:
        self._mem: List[int] = [0] * NUM_BLOCKS          # contenido estable
        self._pending: Dict[int, int] = {}               # idx → nuevo valor

    # ─────────────────────────────── helpers internas ──────────────────────────────
    @staticmethod
    def _split_addr(addr: int) -> tuple[int, int]:
        """Devuelve (idx_de_bloque, offset_byte_dentro_del_bloque)."""
        if not (0 <= addr < NUM_BLOCKS * 4):
            raise ValueError(f"Dirección fuera de rango: {addr}")
        return addr >> 2, addr & 0x3                     # div / mód 4

    def _get_word(self, idx: int) -> int:
        """Lee el valor ya consolidado (ignora _pending)."""
        return self._mem[idx]

    def _stage_write(self, idx: int, new_word: int) -> None:
        """Guarda en el buffer de escritura (sobrescribe si ya había uno)."""
        self._pending[idx] = new_word & BLOCK_MASK

    # ───────────────────────────────── API pública ─────────────────────────────────
    # 1) Lectura combinacional de 32 bits
    def read(self, A_G: int) -> int:
        idx, off = self._split_addr(A_G)
        if off == 0:
            return self._get_word(idx)

        # lectura des-alineada: mezcla 2 bloques
        lo = self._get_word(idx) >> (off * 8)
        hi = self._get_word((idx + 1) % NUM_BLOCKS) << ((4 - off) * 8)
        return (lo | hi) & BLOCK_MASK

    # 2) Escritura latcheada de 32 bits
    def write(self, A_G: int, WD_G: int, WE_G: int) -> None:
        if not WE_G:
            return

        wd = WD_G & BLOCK_MASK
        idx, off = self._split_addr(A_G)

        # extrae cada byte del dato en little-endian y actualiza las palabras
        for i in range(4):
            addr_byte = A_G + i
            b_idx, b_off = self._split_addr(addr_byte)
            byte_val = (wd >> (8 * i)) & 0xFF

            # palabra actual (tener en cuenta si ya hay pendiente)
            cur = self._pending.get(b_idx, self._mem[b_idx])
            shift = b_off * 8
            mask = 0xFF << shift
            new_word = (cur & ~mask) | (byte_val << shift)
            self._stage_write(b_idx, new_word)

    # 3) Flanco de reloj
    def tick(self) -> None:
        for idx, val in self._pending.items():
            self._mem[idx] = val
        self._pending.clear()

    # 4) Utilidades opcionales
    def dump(self) -> List[int]:
        return self._mem.copy()

    def load(self, values: List[int], base: int = 0) -> None:
        for i, v in enumerate(values):
            if base + i < NUM_BLOCKS:
                self._mem[base + i] = v & BLOCK_MASK