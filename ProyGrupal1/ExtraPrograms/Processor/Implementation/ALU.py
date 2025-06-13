"""ALU module for the custom RISC-style ISA.

This ALU implements all data-processing and comparison operations
identified by the 6-bit *ALUSrc* field that the **ControlUnit** emits.

The mapping between ALUSrc codes and operations is documented in
`IdeaDeDesarrollo.pdf` (operaciones del procesador básicas / lógicas
/ desplazamientos)fileciteturn0file0turn0file18 and reproduced
below for convenience:

    0b000000  ADD   A + B
    0b000001  SUB   A - B
    0b000010  ADC   A + B + C_in
    0b000011  SBC   A - B - ¬C_in
    0b000100  MUL   A x B (32-bit low result)
    0b000101  DIV   A ÷ B (integer, trunc toward 0)
    0b000110  AND   A & B
    0b000111  ORR   A | B
    0b001000  EOR   A ^ B
    0b001001  BIC   A & ¬B
    0b001010  LSL   A <<  B[4:0]
    0b001011  LSR   A >>  B[4:0] (logical)
    0b001100  ASR   A >>> B[4:0] (arithmetic)
    0b001101  ROR   (A ror B[4:0])
    0b001110  MOV   B
    0b001111  MVN   ¬B
    0b010000  CMP   set flags for A - B        (result ignored)
    0b010001  CMN   set flags for A + B        (result ignored)
    0b010010  TST   set flags for A & B        (result ignored)
    0b010011  TEQ   set flags for A ^ B        (result ignored)

Flags produced (as a namedtuple):
    N  Negative (MSB of result)
    Z  Zero (result == 0)
    C  Carry (out from the ALU or borrow for SUB/SBC)
    V  Overflow (signed 2 - complement overflow)

All data paths are 32 bits; results are masked to 32 bits.
"""
from __future__ import annotations
from collections import namedtuple
from typing import Tuple
import ctypes

Flags = namedtuple("Flags", "N Z C V")

MASK32 = 0xFFFFFFFF
BIT32  = 1 << 32

class ALU:
    """Arithmetic/Logic Unit implementing the ISA's *ALUSrc* operations."""

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _add_with_carry(a: int, b: int, carry: int) -> Tuple[int, int, int]:
        """Return (result32, carry_out, overflow)."""
        unsigned_sum = (a & MASK32) + (b & MASK32) + carry
        result = unsigned_sum & MASK32
        carry_out = 1 if unsigned_sum >> 32 else 0
        # signed overflow: operands with same sign, result different sign
        sa = (a >> 31) & 1
        sb = (b >> 31) & 1
        sr = (result >> 31) & 1
        overflow = 1 if (sa == sb) and (sr != sa) else 0
        return result, carry_out, overflow

    @staticmethod
    def _sub_with_borrow(a: int, b: int, carry: int) -> Tuple[int, int, int]:
        """Implement A - B - ¬carry  (i.e. borrow = ¬carry)."""
        # convert to addition:  A + (~B) + carry
        return ALU._add_with_carry(a, (~b) & MASK32, carry)

    # ------------------------------------------------------------------
    # public entry
    # ------------------------------------------------------------------
    def execute(self, code: int, A: int, B: int, carry_in: int = 0) -> Tuple[int, Flags]:
        """Execute ALU operation *code* on operands A, B.

        *carry_in* is only used by ADC / SBC.  For other ops it is ignored.
        The returned *result* is a 32-bit value (or 0 for pure flag ops).
        """
        op = code & 0b111111
        C_out = V_out = 0

        if   op == 0b000000:  # ADD
            res, C_out, V_out = self._add_with_carry(A, B, 0)
        elif op == 0b000001:  # SUB
            res, C_out, V_out = self._sub_with_borrow(A, B, 1)  # borrow=0
        elif op == 0b000010:  # ADC
            res, C_out, V_out = self._add_with_carry(A, B, carry_in & 1)
        elif op == 0b000011:  # SBC (A − B − ¬C)
            res, C_out, V_out = self._sub_with_borrow(A, B, carry_in & 1)
        elif op == 0b000100:  # MUL (lower 32 bits)
            res = (A * B) & MASK32
        elif op == 0b000101:  # DIV (signed)
            if B == 0:
                res = 0
            else:
                a_signed = ctypes.c_int32(A).value
                b_signed = ctypes.c_int32(B).value
                res = int(a_signed // b_signed) & MASK32
        elif op == 0b000110:  # AND
            res = A & B
        elif op == 0b000111:  # ORR
            res = A | B
        elif op == 0b001000:  # EOR
            res = A ^ B
        elif op == 0b001001:  # BIC
            res = A & (~B & MASK32)
        elif op == 0b001010:  # LSL (Logical Shift Left)
            shift = B & 0x1F            # solo 5 bits significativos
            if shift == 0:
                res = A & MASK32
                # convención: carry no cambia (0)
                C_out = 0
            else:
                res = (A << shift) & MASK32
                C_out = (A >> (32 - shift)) & 1

        elif op == 0b001011:  # LSR (Logical Shift Right)
            shift = B & 0x1F
            if shift == 0:
                # en ARM un shift de 0 significa 32 → resultado 0, carry = bit31
                res = 0
                C_out = (A >> 31) & 1
            else:
                res = (A & MASK32) >> shift
                C_out = (A >> (shift - 1)) & 1

        elif op == 0b001100:  # ASR (signed)
            shift = B
            a_signed = ctypes.c_int32(A).value
            if shift >= 32:
                res = -1 if a_signed < 0 else 0
            else:
                res = a_signed >> shift
            C_out = (A >> (shift - 1)) & 1 if 0 < shift < 32 else 0

        elif op == 0b001101:  # ROR
            rot = B & 0x1F
            rot %= 32
            res = ((A >> rot) | (A << (32 - rot))) & MASK32
            C_out = (res >> 31) & 1
        elif op == 0b001110:  # MOV
            res = B & MASK32
        elif op == 0b001111:  # MVN
            res = (~B) & MASK32
        elif op in (0b010000, 0b010001, 0b010010, 0b010011):
            # Pure flag ops: CMP, CMN, TST, TEQ
            if   op == 0b010000:  # CMP -> A - B
                res, C_out, V_out = self._sub_with_borrow(A, B, 1)
            elif op == 0b010001:  # CMN -> A + B
                res, C_out, V_out = self._add_with_carry(A, B, 0)
            elif op == 0b010010:  # TST -> A & B
                res = A & B
            elif op == 0b010011:  # TEQ -> A ^ B
                res = A ^ B
        else:
            raise ValueError(f"ALU code {op:06b} no implementado")

        # Flags: N (bit31), Z, C, V
        N_out = (res >> 31) & 1
        Z_out = 1 if (res & MASK32) == 0 else 0
        flags = Flags(N_out, Z_out, C_out & 1, V_out & 1)
        return res & MASK32, flags
    


