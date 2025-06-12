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
    'PRINTL':   '00111000',
    'PRINTR':   '00111001',

    # Control de usuario
    'LOGOUT':   '00111010',
    'LOGIN':    '00111011',
    'CLEAR':    '00111100',

    # Seguridad
    'AUTHCMP':  '00111101',
    'STRPASS':  '00111110',
    'STRK':     '00111111',
}


# Función para codificar un registro Rn o wn
def encode_register(regname):
    reg_type = '1' if regname.startswith('R') else '0'
    number = int(regname[1:])
    return reg_type + format(number, '05b')  # 6 bits total
