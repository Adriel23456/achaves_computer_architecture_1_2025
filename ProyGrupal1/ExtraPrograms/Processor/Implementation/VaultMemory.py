# vault_memory.py
from typing import List, Optional
from ExtraPrograms.Processor.Implementation.Flags import Flags

# ─── Parámetros de la memoria ─────────────────────────────
BLOCK_BITS  = 32
NUM_BLOCKS  = 16
BLOCK_MASK  = (1 << BLOCK_BITS) - 1  # 0xFFFFFFFF

# ─── Índices base de cada clave de 128 bits ───────────────
KEY0, KEY1, KEY2, KEY3 = 0, 4, 8, 12   # 4 bloques por clave (0-3, 4-7, …)

class VaultMemory:
    """
    Vault Memory protegida (16 × 32 bits = 512 bits).

    • Acceso solo si flags.enabled() == 1   (S1 == S2 == 1)
    • Escrituras se latchean en _pending y se comiten en tick()
    • Lectura es combinacional (como en tu RegisterFile.read)
    """

    def __init__(self, flags: Flags):
        self._flags        = flags
        self._mem: List[int] = [0] * NUM_BLOCKS

        # ---------------- Señales de acceso ----------------
        self._pending: Optional[tuple[int, int]] = None  # (idx, data) latched

    # ───────────────────────────────────────────────────────
    # Lectura (combinacional)
    # ───────────────────────────────────────────────────────
    def read(self, k: int) -> int:
        """Devuelve el bloque k si S1/S2 están activos; combinacional."""
        if self._flags.enabled() != 1:
            raise PermissionError("Lectura denegada: S1/S2 inactivos.")
        idx = k & 0xF
        if idx >= NUM_BLOCKS:
            raise IndexError("Dirección fuera de rango (0-15)")
        return self._mem[idx]

    # ───────────────────────────────────────────────────────
    # Escritura (latched)
    # ───────────────────────────────────────────────────────
    def write(self, k: int, data: int, we: int):
        """
        k    : dirección de bloque (0-15)
        data : entero de 32 bits
        we   : 1 = solicitar escritura
        """
        if not we:
            return  # nada que latch-ear
        if self._flags.enabled() != 1:
            raise PermissionError("Escritura denegada: S1/S2 inactivos.")
        if not (0 <= data <= BLOCK_MASK):
            raise ValueError(f"data debe ser un entero de {BLOCK_BITS} bits.")
        idx = k & 0xF
        if idx >= NUM_BLOCKS:
            raise IndexError("Dirección fuera de rango (0-15)")
        self._pending = (idx, data)

    # ───────────────────────────────────────────────────────
    # Flanco de reloj  (commit de la escritura pendiente)
    # ───────────────────────────────────────────────────────
    def tick(self):
        if self._pending is not None:
            idx, data = self._pending
            self._mem[idx] = data
            self._pending = None  # se consume

    # ───────────────────────────────────────────────────────
    # Debug opcional
    # ───────────────────────────────────────────────────────
    def dump(self) -> List[int]:
        return self._mem.copy()
