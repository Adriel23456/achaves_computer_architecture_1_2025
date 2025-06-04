from isa import OPCODES, encode_register

def encode_instruction(tokens):
    op = tokens[0][1]

    if op == 'ADD':
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        Rm = encode_register(tokens[5][1])
        rest = '0' * (64 - 9 - 6 - 6 - 6)
        return opcode + Rd + Rn + Rm + rest

    elif op == 'MOVI':
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        imm = int(tokens[3][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 9 - 6 - 32)
        return opcode + Rd + bin_imm + rest

    elif op == 'ADDI':
        opcode = OPCODES[op]
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        imm = int(tokens[5][1].replace('#', ''), 0)
        bin_imm = format(imm, '032b')
        rest = '0' * (64 - 9 - 6 - 6 - 32)
        return opcode + Rd + Rn + bin_imm + rest

    elif op == 'TEA':
        opcode = OPCODES[op]
        val1 = int(tokens[1][1].replace('#', ''), 0)
        val2 = int(tokens[3][1].replace('#', ''), 0)
        bin_val1 = format(val1, '031b')  # 31 bits
        bin_val2 = format(val2, '032b')  # 32 bits
        padding = '0' * (64 - 9 - 31 - 32)
        return opcode + bin_val1 + bin_val2 + padding

    elif op == 'STRK':
        opcode = OPCODES[op]
        kword = tokens[1][1]  # ejemplo: k2.1
        clave, word = map(int, kword[1:].split('.'))
        val = int(tokens[2][1].replace('#', ''), 0)
        bin_clave = format(clave, '02b')
        bin_word = format(word, '02b')
        bin_val = format(val, '032b')
        rest = '0' * (64 - 9 - 2 - 2 - 32)
        return opcode + bin_clave + bin_word + bin_val + rest

    elif op == 'STRPASS':
        opcode = OPCODES[op]
        index = int(tokens[1][1])
        val = int(tokens[2][1].replace('#', ''), 0)
        bin_index = format(index, '03b')
        bin_val = format(val, '032b')
        rest = '0' * (64 - 9 - 3 - 32)
        return opcode + bin_index + bin_val + rest

    elif op == 'PRINTL':
        opcode = OPCODES[op]
        val = int(tokens[1][1].replace('#', ''), 0)
        bin_val = format(val, '055b')
        return opcode + bin_val

    elif op == 'NOP' or op == 'LOGOUT':
        opcode = OPCODES[op]
        padding = '0' * (64 - 9)
        return opcode + padding

    elif op == 'B':
        opcode = OPCODES[op]
        # Por ahora, no implementamos salto real, lo representamos como PC+0
        bin_dir = format(0, '055b')  # 64 - 9
        return opcode + bin_dir

    else:
        raise ValueError(f"No se puede codificar instrucción: {op}")
