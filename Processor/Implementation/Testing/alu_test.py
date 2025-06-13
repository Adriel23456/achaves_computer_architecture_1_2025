# alu_test.py

from Processor.Implementation.ALU import ALU, Flags, MASK32          # ← adapta el import a tu ruta

alu = ALU()

def test_add_wraparound():
    # 0xFFFFFFFF + 1 = 0x00000000 (carry)
    res, flags = alu.execute(0b000000, 0xFFFFFFFF, 1)
    assert res == 0x00000000
    assert flags.Z == 1 and flags.C == 1

def test_sub_negative_result():
    # 1 - 2 = 0xFFFFFFFF (−1 en complemento a 2)
    res, flags = alu.execute(0b000001, 1, 2)
    assert res == 0xFFFFFFFF
    assert flags.N == 1 and flags.Z == 0

def test_adc_with_carry():
    # (0xFFFFFFFE + 1) + carry_in=1 → 0x00000000 with carry
    res, flags = alu.execute(0b000010, 0xFFFFFFFE, 1, carry_in=1)
    assert res == 0x00000000
    assert flags.Z == 1 and flags.C == 1

def test_sbc_underflow():
    # 0 - 1 - ¬1 = 0 - 1 - 0 = 0xFFFFFFFF
    res, flags = alu.execute(0b000011, 0, 1, carry_in=1)
    assert res == 0xFFFFFFFF
    assert flags.N == 1 and flags.C == 0

def test_mul_large_numbers():
    res, flags = alu.execute(0b000100, 0x00010000, 0x00010000)
    assert res == 0x00000000  # low 32 bits of 2^32
    assert flags.Z == 1

def test_divide_by_zero():
    res, flags = alu.execute(0b000101, 123456, 0)
    assert res == 0  # must avoid crash
    assert flags.Z == 1

def test_lsl_overflow():
    res, flags = alu.execute(0b001010, 0x00000001, 32)
    assert res == 0
    assert flags.Z == 1

def test_asr_signed():
    # 0xFFFFFFF0 >> 4 → debe ser 0xFFFFFFFF (preservando el signo)
    res, flags = alu.execute(0b001100, 0xFFFFFFF0, 4)
    assert res == 0xFFFFFFFF
    assert flags.N == 1

def test_ror_edge():
    # rotar 0x80000001 1 bit → 0xC0000000
    res, flags = alu.execute(0b001101, 0x80000001, 1)
    assert res == 0xC0000000

def test_mvn_all_ones():
    res, flags = alu.execute(0b001111, 0, 0x00000000)
    assert res == 0xFFFFFFFF

def test_teq_flags():
    res, flags = alu.execute(0b010011, 0b1010, 0b1010)
    assert flags.Z == 1  # A ^ B = 0

def test_cmp_borrow():
    # 2 − 3 = -1 → carry = 0 (borrow)
    res, flags = alu.execute(0b010000, 2, 3)
    assert flags.C == 0 and flags.N == 1
#-------------------------------------------------------------------------------------------------
def test_div_signed_behavior():
    assert alu.execute(0b000101, -10 & MASK32, 2)[0] == (-5 & MASK32)
    assert alu.execute(0b000101, 10, (-2 & MASK32))[0] == (-5 & MASK32)
    assert alu.execute(0b000101, 0, 123)[0] == 0
    assert alu.execute(0b000101, (-2**31) & MASK32, (-1) & MASK32)[0] == (2**31) & MASK32  # wraparound
def test_ror_full_cycle():
    res, _ = alu.execute(0b001101, 0x80000001, 32)
    assert res == 0x80000001  # ROR 32 debe dejar igual
def test_mov_mvn_extremos():
    assert alu.execute(0b001110, 0, 0xFFFFFFFF)[0] == 0xFFFFFFFF
    assert alu.execute(0b001111, 0, 0x00000000)[0] == 0xFFFFFFFF
def test_logic_flags_consistency():
    _, fl = alu.execute(0b000110, 0xFFFFFFFF, 0x00000000)  # AND
    assert fl.C == 0 and fl.V == 0
def extra_f():
    assert alu.execute(0b001101, 0x12345678, 64)[0] == 0x12345678
def extra_second():
    res, fl = alu.execute(0b000001, 0x00000000, 0x00000001)
    assert res == 0xFFFFFFFF and fl.C == 0 and fl.N == 1

def run_all_advanced():
    test_add_wraparound()
    test_sub_negative_result()
    test_adc_with_carry()
    test_sbc_underflow()
    test_mul_large_numbers()
    test_divide_by_zero()
    test_lsl_overflow()
    test_asr_signed()
    test_ror_edge()
    test_mvn_all_ones()
    test_teq_flags()
    test_cmp_borrow()
    test_div_signed_behavior()
    test_ror_full_cycle()
    test_mov_mvn_extremos()
    test_logic_flags_consistency()
    extra_f()
    extra_second()
    print("✅ ALU pasó todos los tests exigentes.")

if __name__ == "__main__":
    run_all_advanced()