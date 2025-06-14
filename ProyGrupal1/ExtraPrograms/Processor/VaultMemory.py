# ═══════════════════════════════════════════════════════════════════════════
# VaultMemory.py - VERSIÓN SEGURA
# ═══════════════════════════════════════════════════════════════════════════
from typing import List, Optional
from ExtraPrograms.Processor.Flags import Flags

BLOCK_BITS  = 32
NUM_BLOCKS  = 16
BLOCK_MASK  = (1 << BLOCK_BITS) - 1

class VaultMemory:
    """
    Vault Memory protegida (16 × 32 bits).
    • Acceso SOLO si flags.enabled() == 1 (S1 == S2 == 1)
    • Si no hay permisos, retorna 0 en lectura y bloquea escritura
    """

    def __init__(self, flags: Flags):
        self._flags = flags
        self._mem: List[int] = [0] * NUM_BLOCKS
        self._pending: Optional[tuple[int, int]] = None

    def read(self, k: int) -> int:
        """Lee bloque k. Retorna 0 si no hay permisos."""
        # CRÍTICO: Verificar permisos
        if self._flags.enabled() != 1:
            print(f"[VAULT] Lectura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}")
            return 0  # Retornar 0 en lugar de lanzar excepción
        
        idx = k & 0xF
        if idx >= NUM_BLOCKS:
            print(f"[VAULT] Dirección fuera de rango: {idx}")
            return 0
            
        return self._mem[idx]

    def write(self, k: int, data: int, we: int):
        """Escribe en bloque k. Se bloquea si no hay permisos."""
        if not we:
            return
            
        # CRÍTICO: Verificar permisos
        if self._flags.enabled() != 1:
            print(f"[VAULT] Escritura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}")
            return  # No hacer nada
        
        idx = k & 0xF
        if idx >= NUM_BLOCKS:
            print(f"[VAULT] Dirección fuera de rango: {idx}")
            return
            
        self._pending = (idx, data & BLOCK_MASK)

    def tick(self):
        if self._pending is not None:
            idx, data = self._pending
            self._mem[idx] = data
            self._pending = None

    def dump(self) -> List[int]:
        return self._mem.copy()
    