# ═══════════════════════════════════════════════════════════════════════════
# LoginMemory.py - VERSIÓN SEGURA
# ═══════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import List, Optional
from ExtraPrograms.Processor.Flags import Flags

BLOCK_BITS  = 32
NUM_BLOCKS  = 8
BLOCK_MASK  = (1 << BLOCK_BITS) - 1

class LoginMemory:
    """
    Login Memory protegida (8 × 32 bits).
    • Lectura permitida si: flags.enabled() == 1 O L == 1
    • Escritura permitida si: flags.enabled() == 1
    • Si no hay permisos, retorna 0 en lectura y bloquea escritura
    """

    def __init__(self, flags: Flags):
        self._flags = flags
        self._mem: List[int] = [0] * NUM_BLOCKS
        self._pending: Optional[tuple[int, int]] = None

    def read(self, A: int, L: int = 0) -> int:
        """Lee bloque A. Retorna 0 si no hay permisos."""
        # Verificar permisos: necesita S1/S2 O flag L
        if not (self._flags.enabled() == 1 or L == 1):
            print(f"[LOGIN] Lectura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}, L={L}")
            return 0  # Retornar 0 en lugar de lanzar excepción
        
        idx = A & 0x7
        return self._mem[idx]

    def write(self, A: int, WD: int, WE: int, L: int = 0):
        """Escribe en bloque A. Solo con SafeFlags activos."""
        if not WE:
            return
        if self._flags.enabled() != 1:
            print(f"[LOGIN] Escritura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}")
            return
        idx = A & 0x7
        self._pending = (idx, WD & BLOCK_MASK)
        # ─── NUEVO LOG ────────────────────────────────────────────
        print(f"[LOGIN] ★ escritura latcheada P{idx+1} <- 0x{WD & BLOCK_MASK:08X}")

    def tick(self):
        if self._pending is not None:
            idx, data = self._pending
            self._mem[idx] = data
            # ─── CONFIRMACIÓN ─────────────────────────────────────
            print(f"[LOGIN] ✔ P{idx+1} <= 0x{data:08X} (commit)")
            self._pending = None

    def dump(self) -> List[int]:
        return self._mem.copy()
    