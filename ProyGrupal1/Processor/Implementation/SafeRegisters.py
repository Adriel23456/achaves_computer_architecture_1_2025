# safe_register_file.py
from __future__ import annotations
from typing import List, Optional
from Flags import Flags

MASK32 = 0xFFFFFFFF

class SafeRegisterFile:
    """
    Banco de registros seguros (10 × 32 bits):
        · w1..w9 → índices 0-8   (R/W)
        · d0     → índice 9      (constante 0x9E3779B9, solo-lectura)

    • Lectura y escritura requieren flags.enabled() == 1 (S1 == S2 == 1)
    • Escrituras se latchean y se aplican en tick() (flanco de reloj)
    """

    NUM_REGS = 10

    def __init__(self, flags: Flags):
        self._flags = flags
        self._regs: List[int] = [0] * self.NUM_REGS
        self._regs[9] = 0x9E3779B9  # d0 (DELTA TEA)

        # búfer de escritura pendiente: (idx, data) o None
        self._pending: Optional[tuple[int, int]] = None

    # Lectura combinacional
    def read(self, ar1: int, ar2: int) -> tuple[int, int]:
        if self._flags.enabled() != 1:
            raise PermissionError("Lectura denegada: S1/S2 inactivos.")
        return (
            self._regs[ar1 & 0xF],
            self._regs[ar2 & 0xF],
        )

    # Solicitud de escritura (latched hasta tick)
    def write(self, ar3: int, wdr3: int, regwrite: int):
        if not regwrite:
            return
        if self._flags.enabled() != 1:
            raise PermissionError("Escritura denegada: S1/S2 inactivos.")

        idx = ar3 & 0xF
        if idx == 9:
            raise PermissionError("Registro d0 es de solo-lectura.")

        self._pending = (idx, wdr3 & MASK32)


    # Flanco de reloj: commit de la escritura
    def tick(self):
        if self._pending is not None:
            idx, data = self._pending
            self._regs[idx] = data
            self._pending = None  # se consume

    # Depuración
    def dump(self) -> List[int]:
        return self._regs.copy()
