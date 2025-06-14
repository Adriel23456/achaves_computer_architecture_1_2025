# encoder.py
from ExtraPrograms.ISA.isa import OPCODES, encode_register, encode_special_field

def encode_instruction(tokens, label_table=None, current_index= None):
    op = tokens[0][1]

    # =========================================
    # Aritméticas: tipo REG, REG, REG
    if op in ['ADD', 'ADDS', 'SUB', 'ADC', 'SBC', 'MUL', 'DIV', 'AND', 'ORR', 'EOR', 'BIC', 'LSL', 'LSR', 'ASR', 'ROR']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        Rm = encode_register(tokens[5][1])
        rest = '0' * (64 - 8 - 4 - 4 - 4 - 4)
        return opcode + special + Rd + Rn + Rm + rest

    # =========================================
    # Inmediatos: tipo REG, REG, IMM (con Rm=0000)
    elif op in ['ADDI', 'SUBI', 'ADCI', 'SBCI', 'MULI', 'DIVI', 'ANDI', 'ORRI', 'EORI', 'BICI', 'LSLI', 'LSRI', 'ASRI', 'RORI']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        Rd = encode_register(tokens[1][1])
        Rn = encode_register(tokens[3][1])
        Rm = '0000'  # Rm nulo
        imm = int(tokens[5][1].replace('#', ''), 0)
        bin_imm = format(imm & 0xFFFFFFFF, '032b')
        rest = '0' * 8
        return opcode + special + Rd + Rn + Rm + bin_imm + rest

    # =========================================
    # MOV / MVN
    elif op in ['MOV', 'MVN']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        Rd = encode_register(tokens[1][1])
        Rn = '0000'  # Rn nulo
        Rm = encode_register(tokens[3][1])
        rest = '0' * (64 - 8 - 4 - 4 - 4 - 4)
        return opcode + special + Rd + Rn + Rm + rest

    elif op in ['MOVI', 'MVNI']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        Rd = encode_register(tokens[1][1])
        Rn = '0000'  # Rn nulo
        Rm = '0000'
        imm = int(tokens[3][1].replace('#', ''), 0)
        bin_imm = format(imm & 0xFFFFFFFF, '032b')
        rest = '0' * 8
        return opcode + special + Rd + Rn + Rm + bin_imm + rest

    # =========================================
    # Comparaciones
    elif op in ['CMP', 'CMN', 'TST', 'TEQ']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        Rd = '0000'  # Rd nulo
        Rn = encode_register(tokens[1][1])
        Rm = encode_register(tokens[3][1])
        rest = '0' * (64 - 8 - 4 - 4 - 4 - 4)
        return opcode + special + Rd + Rn + Rm + rest

    elif op in ['CMPI', 'CMNI', 'TSTI', 'TEQI']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        Rd = '0000'  # Rd nulo
        Rn = encode_register(tokens[1][1])
        Rm = '0000'
        imm = int(tokens[3][1].replace('#', ''), 0)
        bin_imm = format(imm & 0xFFFFFFFF, '032b')
        rest = '0' * 8
        return opcode + special + Rd +Rn + Rm + bin_imm + rest

    # =========================================
    # Comparación con contraseña (CMPS)
    elif op == 'CMPS':
        opcode = OPCODES[op]
        special = '0000'
        rd = '0000'
        rn = encode_register(tokens[1][1])
        pass_reg = encode_register(tokens[3][1])
        imm = '0' * 32
        extra = '0' * 8
        return opcode + special + rd + rn + pass_reg + imm + extra

    # =========================================
    # Bifurcaciones
    elif op in ['B', 'BEQ', 'BNE', 'BLT', 'BGT']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        # Calcular offset en instrucciones y multiplicar por 8 (bytes por instrucción)
        offset_instructions = label_table.get(tokens[1][1], 0) - current_index
        offset_bytes = offset_instructions * 8  # Cada instrucción es de 8 bytes
        # Manejar valores con signo de 32 bits
        if offset_bytes < 0:
            offset_bytes = (1 << 32) + offset_bytes  # Complemento a 2 para negativos
        imm = format(offset_bytes & 0xFFFFFFFF, '032b')  # Offset en bytes (32 bits)
        extra = '0' * 8  # Extra no relevante
        rd = rn = rm = '0000'
        return opcode + special + rd + rn + rm + imm + extra

    # =========================================
    # Especiales
    elif op in ['SWI', 'NOP', 'LOGOUT', 'CLEAR']:
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)
        rest = '0' * (64 - 8 - 4)
        return opcode + special + rest

    # =========================================
    # Memoria
    elif op in ['LDR', 'STR', 'LDRB', 'STRB']:
        opcode  = OPCODES[op]

        # --- analizar operando de memoria ---
        mem_token   = tokens[3][1]                 # G[R1,#50] …
        mem_type    = mem_token[0]                 # 'G' / 'D' / 'V' / 'P'
        inside      = mem_token[mem_token.find('[')+1 : mem_token.find(']')]
        parts       = [p.strip() for p in inside.split(',')]

        Ra_bin      = encode_register(parts[0])    # registro dentro de [ ]
        offset      = int(parts[1].lstrip('#'), 0) if len(parts) > 1 else 0
        imm32       = format(offset & 0xFFFFFFFF, '032b')
        extra       = '00000000'

        # --- decidir Rd / Rm según instrucción ---
        if op in ['LDR', 'LDRB']:
            Rd_bin  = encode_register(tokens[1][1])      # destino
            Rm_bin  = '0000'                             # no se usa
        else:  # STR / STRB
            Rd_bin  = '0000'                             # no hay Rd
            Rm_bin  = encode_register(tokens[1][1])      # fuente (Rb)

        # --- SPECIAL ---
        special = encode_special_field(tokens, op,
                                   mem_type=mem_type,
                                   Ra=parts[0],
                                   Rb=tokens[1][1])

        # ensamblar
        return opcode + special + Rd_bin + Ra_bin + Rm_bin + imm32 + extra

    # =========================================
    # PRINT
    elif op in ['PRINTI', 'PRINTS', 'PRINTB']:
        opcode  = OPCODES[op]                      # 8 bits
        special = encode_special_field(tokens, op) # 4 bits (X1X0)

        # Operando de memoria «G[R6,#1]» …
        mem      = tokens[1][1]
        mem_type = mem[0]                          # G/D/V/P
        inside   = mem[mem.find('[')+1 : mem.find(']')]
        parts    = [p.strip() for p in inside.split(',')]

        Rn       = encode_register(parts[0])       # 4 bits
        offset   = int(parts[1].lstrip('#'), 0)
        imm32    = format(offset & 0xFFFFFFFF, '032b')

        # Campos que no se usan:
        Rd = '0000'
        Rm = '0000'
        extra = '00000000'

        # 8+4+4+4+4+32+8 = 64 bits
        return opcode + special + Rd + Rn + Rm + imm32 + extra


    # =========================================
    # Seguridad / cifrado
    elif op == 'STRK':
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)

        rd = '0000'  # No importa
        rn = '0000'  # No importa

        kword = tokens[1][1]  # Ej: 'k1.0'
        clave, word = map(int, kword[1:].split('.'))
        bin_clave = format(clave, '02b')  # 2 bits
        bin_word = format(word, '02b')    # 2 bits

        imm = int(tokens[2][1].replace('#', ''), 0)  # Inmediato
        bin_imm = format(imm & 0xFFFFFFFF, '032b')
        extra = '0' * 8

        return opcode + special + rd + rn + bin_clave + bin_word + bin_imm + extra

    elif op == 'STRPASS':
        opcode = OPCODES[op]
        special = encode_special_field(tokens, op)

        rd = '0000'  # No importa
        rn = '0000'  # No importa

        pass_token = tokens[1][1]  # Ej: 'P1'
        # CORRECCIÓN: Usar encode_register para mantener consistencia
        bin_pass = encode_register(pass_token)  # P1→0000, P2→0001, etc.

        imm = int(tokens[2][1].replace('#', ''), 0)  # Inmediato
        bin_imm = format(imm & 0xFFFFFFFF, '032b')
        extra = '0' * 8

        return opcode + special + rd + rn + bin_pass + bin_imm + extra
    
    # =========================================
    # Pseudoinstrucción AUTHCMP (expande a 8 CMPS)
    elif op == 'AUTHCMP':
        binaries = []
        for i in range(1, 9):
            Ri = f'R{i}'
            Pi = f'P{i}'
            tokens_cmps = [('OPCODE', 'CMPS'), ('REG', Ri), ('COMMA', ','), ('PASS', Pi)]
            bin_cmps = encode_instruction(tokens_cmps)
            binaries.append(bin_cmps)
        return binaries
    
    # =========================================
    # Pseudoinstrucción TEA #0, #val
    if op == 'TEA':
        binaries = []
        val = int(tokens[3][1].replace('#', ''), 0)
        tokens1 = [('OPCODE', 'MOVI'), ('REG', 'W6'), ('COMMA', ','), ('IMM', f'#{hex(val)}')]
        tokens2 = [('OPCODE', 'MOVI'), ('REG', 'W7'), ('COMMA', ','), ('IMM', '#32')]
        binaries.append(encode_instruction(tokens1))
        binaries.append(encode_instruction(tokens2))
        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAENC #1, kx
    if op == 'TEAENC' and tokens[1][1] == '#1':
        binaries = []
        clave_token = tokens[3][1]  # 'k1', etc.
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([('OPCODE', 'ADD'), ('REG', 'W6'), ('COMMA', ','), ('REG', 'W6'), ('COMMA', ','), ('REG', 'd0')]))
        binaries.append(encode_instruction([('OPCODE', 'LSLI'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W5'), ('COMMA', ','), ('IMM', '#4')]))
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        kword = f'{clave_token}.0'
        binaries.append(encode_instruction([('OPCODE', 'ADDS'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W8'), ('COMMA', ','), ('KWORD', kword)]))
        return binaries

    # =========================================
    # Pseudoinstrucción TEAENC #2
    if op == 'TEAENC' and tokens[1][1] == '#2':
        binaries = []
        binaries.append(encode_instruction([('OPCODE', 'ADD'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W5'), ('COMMA', ','), ('REG', 'W6')]))
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([('OPCODE', 'EOR'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W9')]))
        return binaries
    
    # Pseudoinstrucción TEAENC #3
    elif op == 'TEAENC' and tokens[1][1] == '#3':
        binaries = []
        kword = tokens[3][1] if len(tokens) > 3 else 'k0'  # Por defecto k0
        binaries.append(encode_instruction([('OPCODE', 'LSRI'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W5'), ('COMMA', ','), ('IMM', '#5')]))
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([('OPCODE', 'ADDS'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W9'), ('COMMA', ','), ('KWORD', f'{kword}.1')]))
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([('OPCODE', 'EOR'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W9')]))
        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAENC #4
    elif op == 'TEAENC' and tokens[1][1] == '#4':
        binaries = []
        kword = tokens[3][1] if len(tokens) > 3 else 'k0'
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([('OPCODE', 'ADD'), ('REG', 'W4'), ('COMMA', ','), ('REG', 'W4'), ('COMMA', ','), ('REG', 'W8')]))
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([('OPCODE', 'LSLI'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W4'), ('COMMA', ','), ('IMM', '#4')]))
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([('OPCODE', 'ADDS'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W8'), ('COMMA', ','), ('KWORD', f'{kword}.2')]))
        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAENC #5
    elif op == 'TEAENC' and tokens[1][1] == '#5':
        binaries = []
        binaries.append(encode_instruction([
            ('OPCODE', 'ADD'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W4'), ('COMMA', ','), ('REG', 'W6')
        ]))
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))
        binaries.append(encode_instruction([
            ('OPCODE', 'EOR'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W9')
        ]))
        return binaries

    # =========================================
    # Pseudoinstrucción TEAENC #6
    elif op == 'TEAENC' and tokens[1][1] == '#6':
        binaries = []
        kword = tokens[3][1] if len(tokens) > 3 else 'k0'  # Valor por defecto

        binaries.append(encode_instruction([
            ('OPCODE', 'LSRI'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W4'), ('COMMA', ','), ('IMM', '#5')
        ]))

        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        binaries.append(encode_instruction([
            ('OPCODE', 'ADDS'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W9'), ('COMMA', ','), ('KWORD', f'{kword}.3')
        ]))

        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        binaries.append(encode_instruction([
            ('OPCODE', 'EOR'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W9')
        ]))

        return binaries
    
    elif op == 'TEAENC' and tokens[1][1] == '#7':
        binaries = []

        # 4 NOPs
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # ADD W5, W5, W8
        binaries.append(encode_instruction([
            ('OPCODE', 'ADD'), ('REG', 'W5'), ('COMMA', ','), ('REG', 'W5'), ('COMMA', ','), ('REG', 'W8')
        ]))

        # SUBI W7, W7, #1
        binaries.append(encode_instruction([
            ('OPCODE', 'SUBI'), ('REG', 'W7'), ('COMMA', ','), ('REG', 'W7'), ('COMMA', ','), ('IMM', '#1')
        ]))

        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAD #1
    elif op == 'TEAD' and tokens[1][1] == '#1':
        binaries = []
        kword = tokens[3][1] if len(tokens) > 3 else 'k0'  # Por defecto k0

        # NOP x4
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # LSLI W8, W4, #4
        binaries.append(encode_instruction([('OPCODE', 'LSLI'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W4'), ('COMMA', ','), ('IMM', '#4')]))

        # NOP x4
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # ADDS W8, W8, k?.2
        binaries.append(encode_instruction([('OPCODE', 'ADDS'), ('REG', 'W8'), ('COMMA', ','), ('REG', 'W8'), ('COMMA', ','), ('KWORD', f'{kword}.2')]))

        # ADD W9, W4, W6
        binaries.append(encode_instruction([('OPCODE', 'ADD'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W4'), ('COMMA', ','), ('REG', 'W6')]))

        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAD #2
    elif op == 'TEAD' and tokens[1][1] == '#2':
        binaries = []
        kword = tokens[3][1] if len(tokens) > 3 else 'k0'  # Por defecto k0

        # NOP x4
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # EOR W8, W8, W9
        binaries.append(encode_instruction([
            ('OPCODE', 'EOR'),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W9')
        ]))

        # LSRI W9, W4, #5
        binaries.append(encode_instruction([
            ('OPCODE', 'LSRI'),
            ('REG', 'W9'), ('COMMA', ','),
            ('REG', 'W4'), ('COMMA', ','),
            ('IMM', '#5')
        ]))

        # NOP x4
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # ADDS W9, W9, k?.3
        binaries.append(encode_instruction([
            ('OPCODE', 'ADDS'),
            ('REG', 'W9'), ('COMMA', ','),
            ('REG', 'W9'), ('COMMA', ','),
            ('KWORD', f'{kword}.3')
        ]))

        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAD #3
    elif op == 'TEAD' and tokens[1][1] == '#3':
        binaries = []
        # 4 NOPs
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # EOR W8, W8, W9
        binaries.append(encode_instruction([
            ('OPCODE', 'EOR'),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W9')
        ]))

        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # SUB W3, W3, W8
        binaries.append(encode_instruction([
            ('OPCODE', 'SUB'),
            ('REG', 'W3'), ('COMMA', ','),
            ('REG', 'W3'), ('COMMA', ','),
            ('REG', 'W8')
        ]))
        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAD #4
    elif op == 'TEAD' and tokens[1][1] == '#4':
        binaries = []
        kword = tokens[3][1] if len(tokens) > 3 else 'k0'  # Por defecto k0

        # LSLI W8, W5, #4
        binaries.append(encode_instruction([
            ('OPCODE', 'LSLI'),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W5'), ('COMMA', ','),
            ('IMM', '#4')
        ]))

        # NOP x4
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # ADDS W8, W8, k?.0
        binaries.append(encode_instruction([
            ('OPCODE', 'ADDS'),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W8'), ('COMMA', ','),
            ('KWORD', f'{kword}.0')
        ]))

        # ADD W9, W3, W6
        binaries.append(encode_instruction([('OPCODE', 'ADD'), ('REG', 'W9'), ('COMMA', ','), ('REG', 'W3'), ('COMMA', ','), ('REG', 'W6')]))
        

        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAD #5
    elif op == 'TEAD' and tokens[1][1] == '#5':
        binaries = []
        kword = tokens[3][1] if len(tokens) > 3 else 'k0'  # Por defecto k0

        # NOP x4
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # EOR W8, W8, W9
        binaries.append(encode_instruction([
            ('OPCODE', 'EOR'),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W9')
        ]))

        # LSRI W9, W5, #5
        binaries.append(encode_instruction([
            ('OPCODE', 'LSRI'),
            ('REG', 'W9'), ('COMMA', ','),
            ('REG', 'W5'), ('COMMA', ','),
            ('IMM', '#5')
        ]))

         # NOP x4
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # ADDS W9, W9, k?.1
        binaries.append(encode_instruction([
            ('OPCODE', 'ADDS'),
            ('REG', 'W9'), ('COMMA', ','),
            ('REG', 'W9'), ('COMMA', ','),
            ('KWORD', f'{kword}.1')
        ]))
       

        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAD #6
    elif op == 'TEAD' and tokens[1][1] == '#6':
        binaries = []
        # 4 NOPs
        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # EOR W8, W8, W9
        binaries.append(encode_instruction([
            ('OPCODE', 'EOR'),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W8'), ('COMMA', ','),
            ('REG', 'W9')
        ]))

        for _ in range(4):
            binaries.append(encode_instruction([('OPCODE', 'NOP')]))

        # SUB W4, W4, W8
        binaries.append(encode_instruction([
            ('OPCODE', 'SUB'),
            ('REG', 'W4'), ('COMMA', ','),
            ('REG', 'W4'), ('COMMA', ','),
            ('REG', 'W8')
        ]))
        
        return binaries
    
    # =========================================
    # Pseudoinstrucción TEAD #7
    elif op == 'TEAD' and tokens[1][1] == '#7':
        binaries = []

        # SUB W6, W6, D0
        binaries.append(encode_instruction([
            ('OPCODE', 'SUB'),
            ('REG', 'W6'), ('COMMA', ','),
            ('REG', 'W6'), ('COMMA', ','),
            ('REG', 'D0')
        ]))

        # SUBI W7, W7, #1
        binaries.append(encode_instruction([
            ('OPCODE', 'SUBI'), ('REG', 'W7'), ('COMMA', ','), ('REG', 'W7'), ('COMMA', ','), ('IMM', '#1')
        ]))
        
        return binaries
    else:
        raise ValueError(f"No se puede codificar instrucción: {op}")