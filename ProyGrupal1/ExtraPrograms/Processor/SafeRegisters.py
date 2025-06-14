# ═══════════════════════════════════════════════════════════════════════════
# SafeRegisterFile.py - VERSIÓN SEGURA
# ═══════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import List, Optional
from ExtraPrograms.Processor.Flags import Flags

MASK32 = 0xFFFFFFFF

class SafeRegisterFile:
    """
    Banco de registros seguros (10 × 32 bits):
        · w1..w9 → índices 0-8   (R/W)
        · d0     → índice 9      (constante 0x9E3779B9, solo-lectura)

    • Lectura y escritura requieren flags.enabled() == 1 (S1 == S2 == 1)
    • Si no hay permisos, retorna 0 en lectura y bloquea escritura
    """

    NUM_REGS = 10

    def __init__(self, flags: Flags):
        self._flags = flags
        self._regs: List[int] = [0] * self.NUM_REGS
        self._regs[9] = 0x9E3779B9  # d0 (DELTA TEA)
        self._pending: Optional[tuple[int, int]] = None

    def read(self, ar1: int, ar2: int) -> tuple[int, int]:
        """Lee dos registros. Retorna (0, 0) si no hay permisos de seguridad."""
        # CRÍTICO: Verificar permisos ANTES de cualquier acceso
        if self._flags.enabled() != 1:
            print(f"[SAFE_REG] Lectura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}")
            return 0, 0  # Retornar ceros en lugar de valores reales
        
        # Validar índices
        if ar1 >= self.NUM_REGS or ar2 >= self.NUM_REGS:
            print(f"[SAFE_REG] Índice fuera de rango: {ar1} o {ar2}")
            return 0, 0
        
        # Solo si hay permisos, retornar valores reales
        return self._regs[ar1], self._regs[ar2]

    def write(self, ar3: int, wdr3: int, regwrite: int):
        """Solicita escritura. Se bloquea completamente si no hay permisos."""
        if not regwrite:
            return
            
        # CRÍTICO: Verificar permisos
        if self._flags.enabled() != 1:
            print(f"[SAFE_REG] Escritura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}")
            return  # No hacer nada, no latchear
        
        if ar3 >= self.NUM_REGS:
            print(f"[SAFE_REG] Índice fuera de rango: {ar3}")
            return
            
        if ar3 == 9:
            print("[SAFE_REG] Registro d0 es de solo-lectura")
            return
        
        # Solo si hay permisos, latchear la escritura
        self._pending = (ar3, wdr3 & MASK32)

    def tick(self):
        """Aplica escrituras pendientes."""
        if self._pending is not None:
            idx, data = self._pending
            self._regs[idx] = data
            self._pending = None

    def dump(self) -> List[int]:
        return self._regs.copy()
    