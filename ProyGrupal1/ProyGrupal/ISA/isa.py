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
        return format(number, '04b')
    elif regname.startswith('k'):
        # Maneja claves del tipo k0.0, k1.3, etc.
        clave, word = map(int, regname[1:].split('.'))
        return format(clave, '02b') + format(word, '02b')
    else:
        raise ValueError(f"Registro desconocido: {regname}")


def encode_special_field(tokens, op):
    """Determina el campo Special basado en los operandos"""
    special_bits = ['0', '0', '0', '0']  # [bit55, bit54, bit53, bit52]
    
    # Bit 54: Tipo de registro destino (Rd)
    if len(tokens) >= 2:  # Hay operando destino
        operand = tokens[1][1]
        if operand.startswith('P'):  # Registro de contraseña
            special_bits[1] = '1'
        elif operand.startswith('w'):  # Registro w
            special_bits[1] = '1'
        elif operand.startswith('k'):  # Palabra clave
            special_bits[1] = '1'
    
    # Bit 53: Tipo de registro operando A (Rn)
    if len(tokens) >= 4:  # Hay segundo operando
        operand = tokens[3][1]
        if operand.startswith('P'):  # Registro de contraseña
            special_bits[2] = '1'
        elif operand.startswith('w'):  # Registro w
            special_bits[2] = '1'
        elif operand.startswith('D['):  # Memoria D
            special_bits[2] = '1'
        elif operand.startswith('G['):  # Memoria G
            special_bits[2] = '1'
        elif operand.startswith('V['):  # Memoria V
            special_bits[2] = '1'
        elif operand.startswith('P['):  # Memoria P
            special_bits[2] = '1'
    
    # Bit 52: Tipo de memoria (0=G/V, 1=D/P)
    for i in range(1, len(tokens)):
        if len(tokens[i]) > 1:
            operand = tokens[i][1]
            if operand.startswith('D[') or operand.startswith('P['):
                special_bits[3] = '1'
                break
            elif operand.startswith('G[') or operand.startswith('V['):
                special_bits[3] = '0'
                break
    
    return ''.join(special_bits)