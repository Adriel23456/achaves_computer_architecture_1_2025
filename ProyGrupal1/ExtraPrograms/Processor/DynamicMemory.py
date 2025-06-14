# ═══════════════════════════════════════════════════════════════════════════
# DynamicMemory.py - VERSIÓN SEGURA Y CORREGIDA
# ═══════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Dict, List
from ExtraPrograms.Processor.Flags import Flags

class DynamicMemory:
    """
    Memoria dinámica protegida con tamaño fijo.
    • Acceso SOLO si flags.enabled() == 1 (S1 == S2 == 1)
    • Si no hay permisos, retorna 0 en lectura y bloquea escritura
    • Tamaño fijo: 64 bloques de 64 bits (512 bytes total)
    • Little-endian para operaciones de 32 bits
    """

    def __init__(self,
                 flags: Flags,
                 memory_size: int = 64,
                 block_bits: int = 64):
        self._flags = flags
        # Tamaño fijo - no se puede cambiar después de la inicialización
        self._mem_size = memory_size
        self._block_bits = block_bits
        self._bytes_per_block = block_bits // 8
        self._total_bytes = self._mem_size * self._bytes_per_block  # 512 bytes
        self._block_mask = (1 << block_bits) - 1
        self._mem: List[int] = [0] * self._mem_size
        self._pending: Dict[int, int] = {}
        self._loaded_blocks = self._mem_size

    def _is_valid_address(self, addr: int) -> bool:
        """Verifica si la dirección está dentro del rango válido."""
        return 0 <= addr < self._total_bytes - 3  # -3 porque leemos/escribimos 4 bytes

    def _split_addr(self, addr: int) -> tuple[int, int]:
        """Divide la dirección en índice de bloque y offset."""
        idx = addr // self._bytes_per_block
        off = addr % self._bytes_per_block
        return idx, off

    def read(self, A_D: int) -> int:
        """Lee 32 bits. Retorna 0 si no hay permisos o dirección inválida."""
        # CRÍTICO: Verificar permisos
        if self._flags.enabled() != 1:
            print(f"[DYNAMIC] Lectura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}")
            return 0
        
        # Verificar si la dirección es válida
        if not self._is_valid_address(A_D):
            print(f"[DYNAMIC] Lectura fuera de rango: {A_D}")
            return 0
        
        # Leer 4 bytes en little-endian
        val = 0
        for i in range(4):  # 4 bytes → 32 bits
            addr_byte = A_D + i
            b_idx, b_off = self._split_addr(addr_byte)
            
            # Verificar que el índice esté en rango
            if b_idx >= self._mem_size:
                return 0
                
            word = self._mem[b_idx]
            # Extraer el byte correcto del bloque de 64 bits
            byte_val = (word >> (8 * b_off)) & 0xFF
            # Construir el valor de 32 bits en little-endian
            val |= byte_val << (8 * i)
            
        return val & 0xFFFFFFFF

    def write(self, A_D: int, WD_D: int, WE_D: int) -> None:
        """Escribe 32 bits. Ignora si no hay permisos o dirección inválida."""
        if not WE_D:
            return
            
        # CRÍTICO: Verificar permisos
        if self._flags.enabled() != 1:
            print(f"[DYNAMIC] Escritura BLOQUEADA: S1={self._flags.S1}, S2={self._flags.S2}")
            return
        
        # Verificar si la dirección es válida
        if not self._is_valid_address(A_D):
            print(f"[DYNAMIC] Escritura fuera de rango: {A_D}")
            return
        
        # Escribir 4 bytes en little-endian
        wd = WD_D & 0xFFFFFFFF
        for i in range(4):
            addr_byte = A_D + i
            b_idx, b_off = self._split_addr(addr_byte)
            
            # Verificar que el índice esté en rango
            if b_idx >= self._mem_size:
                return
                
            # Extraer el byte i del valor de 32 bits (little-endian)
            byte_val = (wd >> (8 * i)) & 0xFF
            
            # Obtener el valor actual del bloque (considerando pendientes)
            cur = self._pending.get(b_idx, self._mem[b_idx])
            
            # Crear máscara para el byte específico dentro del bloque de 64 bits
            shift = b_off * 8
            mask = 0xFF << shift
            
            # Actualizar solo el byte correspondiente
            new_word = (cur & ~mask) | (byte_val << shift)
            self._pending[b_idx] = new_word & self._block_mask

    def tick(self) -> None:
        """Aplica las escrituras pendientes."""
        for idx, val in self._pending.items():
            self._mem[idx] = val
        self._pending.clear()

    # Métodos eliminados para prevenir cambios de tamaño:
    # - set_memory_size() - ELIMINADO
    # - set_block_bits() - ELIMINADO

    def dump(self) -> List[int]:
        """Retorna una copia de la memoria."""
        return self._mem.copy()

    def load(self, values: List[int], base: int = 0) -> None:
        """Carga valores en la memoria."""
        for i, v in enumerate(values):
            if base + i < self._mem_size:
                self._mem[base + i] = v & self._block_mask