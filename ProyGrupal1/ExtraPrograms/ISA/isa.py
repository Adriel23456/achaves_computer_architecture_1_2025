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
        if not 1 <= number <= 9:
            raise ValueError("Registro 'w' fuera de rango: válido w1-w9")
        return format(number - 1, '04b')   # w1→0→0000, w9→8→1000
    elif regname.startswith('p'):
        number = int(regname[1:])
        if not 1 <= number <= 8:
            raise ValueError("Registro 'P' fuera de rango: válido P1-P8")
        return format(number - 1, '04b')   # P1→0→0000, P2→1→0001, ..., P8→7→0111
    elif regname.startswith('d'):
        number = int(regname[1:])
        if number != 0:
            raise ValueError("Solo existe el registro d0")
        return '1001'          # d0 ≡ w10 → 9 decimal → 1001
    elif regname.startswith('k'):
        # Maneja claves del tipo k0.0, k1.3, etc.
        clave, word = map(int, regname[1:].split('.'))
        return format(clave, '02b') + format(word, '02b')
    else:
        raise ValueError(f"Registro desconocido: {regname}")


def encode_special_field(tokens, op, **kwargs):
    """
    Devuelve el campo SPECIAL (bits 55-52).

    · bit55 – Rd es w-register
    · bit54 – Rn es w-register
    · bit53 – Rm es w-register
    · bit52 – reservado para otros modos (se deja en 0 en aritméticas)
    """
    def is_w(tok):
        if tok[0] != 'REG':
            return False
        r = tok[1].lower()
        return r.startswith('w') or r == 'd0'   # d0 ≡ w-type
    
    
    # --- casos con valor fijo, NO tocar ---
    if op == 'ADDS':
        return '0000'                    # sigue igual
    if op in ['PRINTI', 'PRINTS', 'PRINTB']:
        mem = tokens[1][1]
        sel = {'G':'00','V':'01','D':'10','P':'11'}[mem[0]]
        return '0' + sel + '0'
    # --- caso especial MOV / MVN ---------------------------------------
    if op in ['MOV', 'MVN']:
        rd_is_w = tokens[1][1].lower().startswith('w')
        rm_is_w = tokens[3][1].lower().startswith('w')
        bit55   = '1' if rd_is_w else '0'
        bit54   = '0'                  # Rn no existe
        bit53   = '1' if rm_is_w else '0'
        bit52   = '0'
        return bit55 + bit54 + bit53 + bit52   # p.e. 0010
    # --- caso especial MOVI / MVNI ---------------------------------------
    if op in ['MOVI', 'MVNI']:
        rd_is_w = tokens[1][1].lower().startswith('w')
        bit55   = '1' if rd_is_w else '0'
        return bit55 + '000'              #  bit54-53-52 = 0
    # ------------- comparaciones sin Rd (CMP/CMN/TST/TEQ) -------------
    if op in ['CMP', 'CMN', 'TST', 'TEQ']:
        rn_w = is_w(tokens[1])                  # Rn  = tokens[1]
        rm_w = is_w(tokens[3])                  # Rm  = tokens[3]
        return '0' + ('1' if rn_w else '0') + ('1' if rm_w else '0') + '0'
    # ------------- comparaciones inmediatas (CMPI/CMNI/TSTI/TEQI) ----
    if op in ['CMPI', 'CMNI', 'TSTI', 'TEQI']:
        rn_w = is_w(tokens[1])                  # Rn  = tokens[1]
        return '0' + ('1' if rn_w else '0') + '00'   # Rm no existe
    # ---------- LDR / LDRB ----------
    if op in ['LDR', 'LDRB']:
        Rd = tokens[1][1]
        Ra = kwargs['Ra']
        mem_type = kwargs['mem_type']

        bit55 = '1' if is_w_or_d(Rd) else '0'   # Rd
        bit54 = '1' if is_w_or_d(Ra) else '0'   # Ra
        bit53 = '0'                              # fijo
        bit52 = '1' if mem_type == 'D' else '0'  # G=0 / D=1
        return bit55 + bit54 + bit53 + bit52

    # ---------- STR / STRB ----------
    if op in ['STR', 'STRB']:
        Ra = kwargs['Ra']
        Rb = kwargs['Rb']
        mem_type = kwargs['mem_type']

        bit55 = '0'                              # siempre 0
        bit54 = '1' if is_w_or_d(Ra) else '0'   # Ra
        bit53 = '1' if is_w_or_d(Rb) else '0'   # Rb
        bit52 = '1' if mem_type == 'D' else '0' # memoria
        return bit55 + bit54 + bit53 + bit52
    
    if op in ['STRK', 'STRPASS']:
        return "0000"

    # --- aritméticas y comparaciones basadas en registros ---
    reg_based = {
        'ADD','SUB','ADC','SBC','MUL','DIV','AND','ORR','EOR','BIC',
        'LSL','LSR','ASR','ROR',
        'ADDI','SUBI','ADCI','SBCI','MULI','DIVI','ANDI','ORRI',
        'EORI','BICI','LSLI','LSRI','ASRI','RORI'
    }
    if op in reg_based:
        def is_w(tok):
            if tok[0] != 'REG':
                return False
            r = tok[1].lower()
            return r.startswith('w') or r == 'd0'   # trata d0 como w-type

        bit55 = '1' if len(tokens) > 1 and is_w(tokens[1]) else '0'   # Rd
        bit54 = '1' if len(tokens) > 3 and is_w(tokens[3]) else '0'   # Rn
        bit53 = '1' if len(tokens) > 5 and is_w(tokens[5]) else '0'   # Rm (si existe)
        bit52 = '0'                                                   # reservado
        return bit55 + bit54 + bit53 + bit52

    # Fallback genérico (etiquetas, k-words, memoria, etc.)
    special_bits = ['0', '0', '0', '0']
    if len(tokens) >= 2 and tokens[1][1].startswith(('P', 'w', 'd', 'k')):
        special_bits[1] = '1'
    if len(tokens) >= 4 and tokens[3][1].startswith(('P', 'w', 'D[', 'G[')):
        special_bits[2] = '1'
    for tok in tokens:
        if tok[1].startswith(('D[', 'P[')):
            special_bits[3] = '1'
            break
    return ''.join(special_bits)

def is_w_or_d(regname: str) -> bool:
    """
    Devuelve True si el registro es un w1-w9 o d0 (alias de w10).
    se usa en SPECIAL para identificar registros tipo 'wide'.
    """
    r = regname.lower()
    return r.startswith('w') or r == 'd0'