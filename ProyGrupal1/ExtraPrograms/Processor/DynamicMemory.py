# ExtraPrograms/Processor/DynamicMemory.py
from typing import Dict, List
from ExtraPrograms.Processor.Flags import Flags

class DynamicMemory:
    """
    Memoria dinámica protegida.
    • Tamaño se ajusta en tiempo de carga (dynamic_mem.bin)
    • read / write validan contra self._loaded_blocks (no contra _mem_size fijo)
    """

    BYTES_PER_BLOCK = 8   # 64 bits

    def __init__(self, flags: Flags):
        self._flags = flags
        # arranca con 1 bloque para no quedar vacío
        self._loaded_blocks: int = 1
        self._mem: List[int] = [0]
        self._pending: Dict[int, int] = {}

    # ───────────────────────── helpers ──────────────────────────
    def _max_address(self) -> int:
        """última dirección válida (inclusiva) en bytes."""
        return self._loaded_blocks * self.BYTES_PER_BLOCK - 4  # leemos/escribimos 4 bytes

    def _split_addr(self, addr: int) -> tuple[int, int]:
        idx = addr // self.BYTES_PER_BLOCK
        off = addr %  self.BYTES_PER_BLOCK
        return idx, off

    def _check_access(self, addr: int) -> bool:
        if addr < 0 or addr > self._max_address():
            print(f"[DYNAMIC] Acceso fuera de rango: {addr} / {self._max_address()}")
            return False
        return True

    # ───────────────────────── API pública ──────────────────────
    def set_size(self, blocks: int):
        """Redimensiona la memoria (conservando contenido previo)."""
        if blocks < 1:
            blocks = 1
        if blocks > self._loaded_blocks:
            self._mem.extend([0] * (blocks - self._loaded_blocks))
        elif blocks < self._loaded_blocks:
            self._mem = self._mem[:blocks]
        self._loaded_blocks = blocks

    def read(self, addr: int) -> int:
        if self._flags.enabled() != 1:
            return 0
        if not self._check_access(addr):
            return 0

        val = 0
        for i in range(4):
            b_idx, b_off = self._split_addr(addr + i)
            val |= ((self._mem[b_idx] >> (8 * b_off)) & 0xFF) << (8 * i)
        return val & 0xFFFFFFFF

    def write(self, addr: int, wd: int, we: int):
        if not we or self._flags.enabled() != 1:
            return
        if not self._check_access(addr):
            return

        for i in range(4):
            b_idx, b_off = self._split_addr(addr + i)
            cur  = self._pending.get(b_idx, self._mem[b_idx])
            mask = 0xFF << (8 * b_off)
            byte = ((wd >> (8 * i)) & 0xFF) << (8 * b_off)
            self._pending[b_idx] = (cur & ~mask) | byte

    def tick(self):
        for idx, val in self._pending.items():
            self._mem[idx] = val
        self._pending.clear()

    # Utilidades
    def dump(self) -> List[int]:
        return self._mem.copy()