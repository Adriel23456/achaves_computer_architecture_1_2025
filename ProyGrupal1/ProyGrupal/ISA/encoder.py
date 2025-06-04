from ProyGrupal.ISA.isa import OPCODES, encode_register

def encode_instruction(tokens):
    op = tokens[0][1]

    if op == 'ADD':
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        Rm = encode_register(tokens[5][1])
        rest = '0' * (64 - 8 - 6 - 6 - 6)
        return opcode + Rd + Rn + Rm + rest

    elif op == 'ADDI':
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        imm = int(tokens[5][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 8 - 6 - 6 - 32)
        return opcode + Rd + Rn + bin_imm + rest

    elif op == 'MOVI':
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        imm = int(tokens[3][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 8 - 6 - 32)
        return opcode + Rd + bin_imm + rest

    elif op in ['LDR', 'STR']:
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        mem = tokens[3][1]  # G[R1, #4]
        mem_type = '0' if mem.startswith('G') else '1'
        inside = mem[mem.find('[')+1:mem.find(']')]
        parts = [p.strip() for p in inside.split(',')]
        Rn = encode_register(parts[0])
        offset = int(parts[1].replace('#', ''), 0) if len(parts) > 1 else 0
        bin_offset = format(offset, '032b')
        rest = '0' * (64 - 8 - 6 - 1 - 6 - 32)
        return opcode + Rd + mem_type + Rn + bin_offset + rest

    elif op == 'PRINTI':
        opcode = OPCODES[op]
        mem = tokens[1][1]  # G[Rn, #offset]
        mem_map = {'G': '00', 'V': '01', 'D': '10', 'P': '11'}
        mem_type = mem_map[mem[0]]
        inside = mem[mem.find('[')+1:mem.find(']')]
        parts = [p.strip() for p in inside.split(',')]
        Rn = encode_register(parts[0])
        offset = int(parts[1].replace('#', ''), 0) if len(parts) > 1 else 0
        bin_offset = format(offset, '032b')
        rest = '0' * (64 - 8 - 2 - 6 - 32)
        return opcode + mem_type + Rn + bin_offset + rest

    elif op == 'PRINTR':
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        rest = '0' * (64 - 8 - 6)
        return opcode + Rd + rest

    elif op == 'TEA':
        opcode = OPCODES[op]
        val1 = int(tokens[1][1].replace('#', ''), 0)
        val2 = int(tokens[3][1].replace('#', ''), 0)
        bin_val1 = format(val1, '031b')
        bin_val2 = format(val2, '032b')
        padding = '0' * (64 - 8 - 31 - 32)
        return opcode + bin_val1 + bin_val2 + padding

    elif op == 'STRK':
        opcode = OPCODES[op]
        kword = tokens[1][1]  # ej: k2.1
        clave, word = map(int, kword[1:].split('.'))
        val = int(tokens[2][1].replace('#', ''), 0)
        bin_clave = format(clave, '02b')
        bin_word = format(word, '02b')
        bin_val = format(val, '032b')
        rest = '0' * (64 - 8 - 2 - 2 - 32)
        return opcode + bin_clave + bin_word + bin_val + rest

    elif op == 'STRPASS':
        opcode = OPCODES[op]
        index = int(tokens[1][1])
        val = int(tokens[2][1].replace('#', ''), 0)
        bin_index = format(index, '03b')
        bin_val = format(val, '032b')
        rest = '0' * (64 - 8 - 3 - 32)
        return opcode + bin_index + bin_val + rest

    elif op == 'PRINTL':
        opcode = OPCODES[op]
        val = int(tokens[1][1].replace('#', ''), 0)
        bin_val = format(val, '055b')
        return opcode + bin_val

    elif op in ['NOP', 'LOGOUT']:
        opcode = OPCODES[op]
        rest = '0' * (64 - 8)
        return opcode + rest

    elif op == 'B':
        opcode = OPCODES[op]
        # Offset aún no calculado: se asume 0 por ahora
        bin_dir = format(0, '055b')
        return opcode + bin_dir
    
    elif op == 'CMP':
        opcode = OPCODES[op]
        Rn = encode_register(tokens[1][1])
        Rm = encode_register(tokens[3][1])
        rest = '0' * (64 - 8 - 6 - 6)
        return opcode + Rn + Rm + rest

    elif op == 'CMPI':
        opcode = OPCODES[op]
        Rn = encode_register(tokens[1][1])
        imm = int(tokens[3][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 8 - 6 - 32)
        return opcode + Rn + bin_imm + rest

    elif op in ['BEQ', 'BNE', 'BGT', 'BLT']:
        opcode = OPCODES[op]
        offset = 0  # 🧠 Placeholder, luego lo resolveremos con etiquetas
        bin_offset = format(offset, '055b')
        return opcode + bin_offset

    else:
        raise ValueError(f"No se puede codificar instrucción: {op}")
