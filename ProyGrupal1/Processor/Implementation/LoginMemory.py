from __future__ import annotations
from typing import List, Optional
from Flags import Flags

# Parámetros
BLOCK_BITS  = 32
NUM_BLOCKS  = 8
BLOCK_MASK  = (1 << BLOCK_BITS) - 1      # 0xFFFFFFFF

class LoginMemory:
    """
    Login Memory protegida (8 × 32 bits).

    • Lectura  y escritura permitidas si:
        · flags.enabled()      == 1   (S1 == S2 == 1)
          ── o ──
        · flags.login_active() == 1   (L == 1)

    • Interfaz síncrona estilo RegisterFile:
        · read(A)                        → dato combinacional
        · write(A, WD, WE)               → latch
        · tick()                         → commit en flanco
    """

    def __init__(self, flags: Flags):
        self._flags = flags
        self._mem: List[int] = [0] * NUM_BLOCKS

        # búfer escritura pendiente: (idx, data) o None
        self._pending: Optional[tuple[int, int]] = None

    # Lectura combinacional
    def read(self, A: int) -> int:
        if not (self._flags.enabled() == 1 or self._flags.login_active() == 1):
            raise PermissionError("Lectura denegada: requiere L o S1/S2.")
        idx = A & 0x7
        return self._mem[idx]

    # Solicitud de escritura (latched)
    def write(self, A: int, WD: int, WE: int):
        if not WE:
            return
        if not (self._flags.enabled() == 1 or self._flags.login_active() == 1):
            raise PermissionError("Escritura denegada: requiere L o S1/S2.")
        if not (0 <= WD <= BLOCK_MASK):
            raise ValueError(f"Dato excede {BLOCK_BITS} bits.")
        idx = A & 0x7
        self._pending = (idx, WD & BLOCK_MASK)

    # Flanco de reloj (commit)
    def tick(self):
        if self._pending is not None:
            idx, data = self._pending
            self._mem[idx] = data
            self._pending = None

    # Depuración
    def dump(self) -> List[int]:
        return self._mem.copy()
