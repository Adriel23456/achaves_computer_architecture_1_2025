# isa.py

OPCODES = {

    # Operaciones aritméticas y lógicas
    'ADD':      '00000000',
    'ADDS':     '00000001', #Por implementar
    'SUB':      '00000010', #Por implementar
    'ADC':      '00000011', #Por implementar
    'SBC':      '00000011', #Por implementar
    'MUL':      '00000101', #Por implementar
    'DIV':      '00000101', #Por implementar
    'AND':      '00000111', #Por implementar
    'ORR':      '00000111', #Por implementar
    'EOR':      '00000111', #Por implementar
    'BIC':      '00000111', #Por implementar
    'LSL':      '00001011', #Por implementar
    'LSR':      '00001100', #Por implementar
    'ASR':      '00001101', #Por implementar
    'ROR':      '00001110', #Por implementar

    # Inmediatos
    'ADDI':     '00001111',
    'SUBI':     '00010000', #Por implementar
    'ADCI':     '00010001', #Por implementar
    'SBCI':     '00010010', #Por implementar
    'MULI':     '00010011', #Por implementar
    'DIVI':     '00010100', #Por implementar
    'ANDI':     '00010101', #Por implementar
    'ORRI':     '00010110', #Por implementar
    'EORI':     '00010111', #Por implementar
    'BICI':     '00011000', #Por implementar
    'LSLI':     '00011001', #Por implementar
    'LSRI':     '00011010', #Por implementar
    'ASRI':     '00011011', #Por implementar
    'RORI':     '00011100', #Por implementar


    # Movimiento de datos 
    'MOV':      '00011101', #Por implementar
    'MVN':      '00011110', #Por implementar

    # Movimiento inmediato (con valor)
    'MOVI':     '00011111',
    'MVNI':     '00100000', #Por implementar


    # Comparaciones
    'CMP':  '00100001',
    'CMPS': '00100010', #Por implementar
    'CMN':  '00100011', #Por implementar
    'TST':  '00100100', #Por implementar
    'TEQ':  '00100101', #Por implementar

    # Comparaciones inmediatas
    'CMPI': '00100110',
    'CMNI': '00100111', #Por implementar
    'TSTI': '00101000', #Por implementar
    'TEQI': '00101001', #Por implementar  

    #Operaciones de bifurcación
    'B':    '00101010',
    'BEQ':  '00101011',  
    'BNE':  '00101100',  
    'BLT':  '00101101',  
    'BGT':  '00101110', 

    #Operaciones especiales
    'SWI':  '00101111', #Por implementar
    'NOP':  '00110000',

    # Memoria
    'LDR':      '00110001', 
    'STR':      '00110010',
    'LDRB':     '00110011', #Por implementar
    'STRB':     '00110100', #Por implementar

    # Prints
    'PRINTI':   '00110101',
    'PRINTS':   '00110110', #Por implementar
    'PRINTB':   '00110111', #Por implementar

    'LOGOUT':   '00111000',

    'STRK':     '00111001', #Revisar (no coincide con idea)
    'STRPASS':  '00111010',

    # Claves criptográficas

    #POR IMPLEMENTAR
    #'AUTHCMP'
    #'TEA'
    #'TEAENC #1' 
    #'TEAENC #2'
    #'TEAENC #3'
    #'TEAENC #4'
    #'TEAENC #5'
    #'TEAENC #6'
    #'TEAENC #7'

    #'TEAD_1'
    #'TEAD_2'
    #'TEAD_3'
    #'TEAD_4'
    #'TEAD_5'
    #'TEAD_6'
    #'TEAD_7'

    

}

# Función para codificar un registro Rn o wn
def encode_register(regname):
    reg_type = '1' if regname.startswith('R') else '0'
    number = int(regname[1:])
    return reg_type + format(number, '05b')  # 6 bits total
