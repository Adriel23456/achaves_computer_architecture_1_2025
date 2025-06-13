OPCODES = {
    # Aritméticas
    'ADD':      '00000000',
    'ADDS':     '00000001',
    'SUB':      '00000010',
    'ADC':      '00000011',
    'SBC':      '00000100',
    'MUL':      '00000101',
    'DIV':      '00000110',
    'AND':      '00000111',
    'ORR':      '00001000',
    'EOR':      '00001001',
    'BIC':      '00001010',
    'LSL':      '00001011',
    'LSR':      '00001100',
    'ASR':      '00001101',
    'ROR':      '00001110',

    # Inmediatos
    'ADDI':     '00001111',
    'SUBI':     '00010000',
    'ADCI':     '00010001',
    'SBCI':     '00010010',
    'MULI':     '00010011',
    'DIVI':     '00010100',
    'ANDI':     '00010101',
    'ORRI':     '00010110',
    'EORI':     '00010111',
    'BICI':     '00011000',
    'LSLI':     '00011001',
    'LSRI':     '00011010',
    'ASRI':     '00011011',
    'RORI':     '00011100',

    # Movimiento
    'MOV':      '00011101',
    'MVN':      '00011110',
    'MOVI':     '00011111',
    'MVNI':     '00100000',

    # Comparación
    'CMP':      '00100001',
    'CMPS':     '00100010',
    'CMN':      '00100011',
    'TST':      '00100100',
    'TEQ':      '00100101',
    'CMPI':     '00100110',
    'CMNI':     '00100111',
    'TSTI':     '00101000',
    'TEQI':     '00101001',

    # Saltos
    'B':        '00101010',
    'BEQ':      '00101011',
    'BNE':      '00101100',
    'BLT':      '00101101',
    'BGT':      '00101110',

    # Especiales
    'SWI':      '00101111',
    'NOP':      '00110000',

    # Memoria
    'LDR':      '00110001',
    'STR':      '00110010',
    'LDRB':     '00110011',
    'STRB':     '00110100',

    # I/O
    'PRINTI':   '00110101',
    'PRINTS':   '00110110',
    'PRINTB':   '00110111',

    # Control de usuario
    'LOGOUT':   '00111000',


    # Seguridad
    'STRK':     '00111001',
    'STRPASS':  '00111010',
    
}

# Función para codificar un registro Rn o wn

def encode_register(regname):
    """Codifica un registro según la especificación ISA"""
    regname = regname.lower()  # Estandariza todo a minúsculas

    if regname.startswith('r'):
        number = int(regname[1:])
        return format(number, '04b')
    elif regname.startswith('w'):
        number = int(regname[1:])
        return format(number, '04b')
    elif regname.startswith('p'):
        number = int(regname[1:])
        return format(number, '04b')
    elif regname.startswith('d'):
        number = int(regname[1:])
        return format(number + 9, '04b')  # ajusta según codificación real
    elif regname.startswith('k'):
        # Maneja claves del tipo k0.0, k1.3, etc.
        clave, word = map(int, regname[1:].split('.'))
        return format(clave, '02b') + format(word, '02b')
    else:
        raise ValueError(f"Registro desconocido: {regname}")


def encode_special_field(tokens, op):
    """Determina el campo Special basado en los operandos"""
    if op == 'ADDS':
        return '0000'

    if op in ['ADD', 'SUB', 'ADC', 'SBC', 'MUL', 'DIV', 'AND', 'ORR', 'EOR', 'BIC', 'LSL', 'LSR', 'ASR', 'ROR']:
        return '0100'

    if op in ['ADDI', 'SUBI', 'ADCI', 'SBCI', 'MULI', 'DIVI', 'ANDI', 'ORRI', 'EORI', 'BICI', 'LSLI', 'LSRI', 'ASRI', 'RORI']:
        return '0100'

    if op in ['MOV', 'MVN', 'MOVI', 'MVNI', 'CMPS', 'B', 'BEQ', 'BNE', 'BLT', 'BGT', 'SWI', 'NOP', 'LOGOUT', 'STRPASS', 'STRK']:
        return '0000'

    if op in ['CMP', 'CMN', 'TST', 'TEQ', 'CMPI', 'CMNI', 'TSTI', 'TEQI']:
        return '0100'

    if op in ['LDR', 'STR', 'LDRB', 'STRB']:
        # Ejemplo de operando mem:  D[R8,#5]  ó  G[R2]
        mem = tokens[3][1] if len(tokens) > 3 else 'G[0]'
        mem_type = mem[0]                 # 'G', 'D', 'V', 'P'
        x_bit = '1' if mem_type in ['D', 'P'] else '0'  # 1 = Dinamic/Password
        return '01' + x_bit + '0'

    if op in ['PRINTI', 'PRINTS', 'PRINTB']:
        mem = tokens[1][1]
        mem_type = mem[0]

        # Mapeo a los 2 bits (bit54‑bit53)
        mem_map = {
            'G': '00',   # General
            'V': '01',   # Vault
            'D': '10',   # Dynamic
            'P': '11'    # Password
        }
        sel = mem_map.get(mem_type, '00')
        return '0' + sel + '0'  # bit55=0, bit52=0


    # Fallback genérico basado en análisis de operandos
    special_bits = ['0', '0', '0', '0']

    if len(tokens) >= 2:
        operand = tokens[1][1]
        if operand.startswith(('P', 'w', 'k')):
            special_bits[1] = '1'

    if len(tokens) >= 4:
        operand = tokens[3][1]
        if operand.startswith(('P', 'w')) or operand.startswith(('D[', 'G[', 'V[', 'P[')):
            special_bits[2] = '1'

    for i in range(1, len(tokens)):
        if len(tokens[i]) > 1:
            operand = tokens[i][1]
            if operand.startswith(('D[', 'P[')):
                special_bits[3] = '1'
                break
            elif operand.startswith(('G[', 'V[')):
                special_bits[3] = '0'
                break

    return ''.join(special_bits)

