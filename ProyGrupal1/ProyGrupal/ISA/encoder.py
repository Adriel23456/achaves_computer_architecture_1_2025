# encoder.py
from ProyGrupal.ISA.isa import OPCODES, encode_register

def encode_instruction(tokens):
    op = tokens[0][1]

    # =========================================
    # Aritméticas: tipo REG, REG, REG
    if op in ['ADD', 'ADDS', 'SUB', 'ADC', 'SBC', 'MUL', 'DIV', 'AND', 'ORR', 'EOR', 'BIC', 'LSL', 'LSR', 'ASR', 'ROR']:
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        Rm = encode_register(tokens[5][1])
        rest = '0' * (64 - 8 - 6 - 6 - 6)  # 8b opcode + 3 regs (6b c/u)
        return opcode + Rd + Rn + Rm + rest

    # =========================================
    # Inmediatos: tipo REG, REG, IMM
    elif op in ['ADDI', 'SUBI', 'ADCI', 'SBCI', 'MULI', 'DIVI', 'ANDI', 'ORRI', 'EORI', 'BICI', 'LSLI', 'LSRI', 'ASRI', 'RORI']:
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        imm = int(tokens[5][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 8 - 6 - 6 - 32)
        return opcode + Rd + Rn + bin_imm + rest

    # =========================================
    # MOV / MVN
    elif op in ['MOV', 'MVN']:
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        rest = '0' * (64 - 8 - 6 - 6)
        return opcode + Rd + Rn + rest

    elif op in ['MOVI', 'MVNI']:
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        imm = int(tokens[3][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 8 - 6 - 32)
        return opcode + Rd + bin_imm + rest

    # =========================================
    # Comparaciones
    elif op in ['CMP', 'CMN', 'TST', 'TEQ']:
        opcode = OPCODES[op]
        Rn = encode_register(tokens[1][1])
        Rm = encode_register(tokens[3][1])
        rest = '0' * (64 - 8 - 6 - 6)
        return opcode + Rn + Rm + rest

    elif op in ['CMPI', 'CMNI', 'TSTI', 'TEQI']:
        opcode = OPCODES[op]
        Rn = encode_register(tokens[1][1])
        imm = int(tokens[3][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 8 - 6 - 32)
        return opcode + Rn + bin_imm + rest

    # =========================================
    # Bifurcaciones
    elif op in ['B', 'BEQ', 'BNE', 'BLT', 'BGT']:
        opcode = OPCODES[op]
        offset = 0  # TODO: calcular offset relativo a etiquetas
        bin_offset = format(offset, '056b')
        return opcode + bin_offset

    # =========================================
    # Especiales
    elif op in ['SWI', 'NOP', 'LOGOUT', 'CLEAR']:
        opcode = OPCODES[op]
        rest = '0' * (64 - 8)
        return opcode + rest

    elif op == 'LOGIN':
        opcode = OPCODES[op]
        Rn = encode_register(tokens[1][1])
        Rm = encode_register(tokens[3][1])
        clave = int(tokens[5][1].replace('#', ''), 0)
        bin_clave = format(clave, '032b')
        rest = '0' * (64 - 8 - 6 - 6 - 32)
        return opcode + Rn + Rm + bin_clave + rest

    # =========================================
    # Memoria
    elif op in ['LDR', 'STR', 'LDRB', 'STRB']:
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        mem = tokens[3][1]
        mem_type = mem[0]  # G, D, V, P
        mem_map = {'G': '00', 'D': '01', 'V': '10', 'P': '11'}
        mem_type_bin = mem_map[mem_type]
        inside = mem[mem.find('[')+1:mem.find(']')]
        parts = [p.strip() for p in inside.split(',')]
        Rn = encode_register(parts[0])
        offset = int(parts[1].replace('#', ''), 0) if len(parts) > 1 else 0
        bin_offset = format(offset, '032b')
        rest = '0' * (64 - 8 - 6 - 2 - 6 - 32)
        return opcode + Rd + mem_type_bin + Rn + bin_offset + rest

    # =========================================
    # PRINT
    elif op in ['PRINTI', 'PRINTS', 'PRINTB']:
        opcode = OPCODES[op]
        mem = tokens[1][1]
        mem_type = mem[0]
        mem_map = {'G': '00', 'D': '01', 'V': '10', 'P': '11'}
        mem_type_bin = mem_map[mem_type]
        inside = mem[mem.find('[')+1:mem.find(']')]
        parts = [p.strip() for p in inside.split(',')]
        Rn = encode_register(parts[0])
        offset = int(parts[1].replace('#', ''), 0)
        bin_offset = format(offset, '032b')
        rest = '0' * (64 - 8 - 2 - 6 - 32)
        return opcode + mem_type_bin + Rn + bin_offset + rest

    elif op == 'PRINTL':
        opcode = OPCODES[op]
        val = int(tokens[1][1].replace('#', ''), 0)
        bin_val = format(val, '056b')
        return opcode + bin_val

    elif op == 'PRINTR':
        opcode = OPCODES[op]
        Rn = encode_register(tokens[1][1])
        rest = '0' * (64 - 8 - 6)
        return opcode + Rn + rest

    # =========================================
    # Seguridad / cifrado
    elif op in ['STRK']:
        opcode = OPCODES[op]
        kword = tokens[1][1]  # k0.0
        clave, word = map(int, kword[1:].split('.'))
        bin_clave = format(clave, '02b')
        bin_word = format(word, '02b')
        val = int(tokens[2][1].replace('#', ''), 0)
        bin_val = format(val, '032b')
        rest = '0' * (64 - 8 - 2 - 2 - 32)
        return opcode + bin_clave + bin_word + bin_val + rest

    elif op == 'STRPASS':
        opcode = OPCODES[op]
        index = int(tokens[1][1])
        bin_index = format(index, '03b')
        val = int(tokens[2][1].replace('#', ''), 0)
        bin_val = format(val, '032b')
        rest = '0' * (64 - 8 - 3 - 32)
        return opcode + bin_index + bin_val + rest



    else:
        raise ValueError(f"No se puede codificar instrucción: {op}")
