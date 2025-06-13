# parser.py
instruction_patterns = {
    # Instrucciones de operación
    'ADD': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'ADDS': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'KWORD'],
    'SUB': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'ADC': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'SBC': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'MUL': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'DIV': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'AND': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'ORR': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'EOR': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'BIC': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'LSL': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'LSR': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'ASR': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'ROR': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],

    # Inmediatos
    'ADDI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'SUBI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'ADCI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'SBCI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'MULI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'DIVI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'ANDI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'ORRI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'EORI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'BICI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'LSLI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'LSRI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'ASRI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'RORI': ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],

    # Movimiento de datos
    'MOV': ['OPCODE', 'REG', 'COMMA', 'REG'],
    'MVN': ['OPCODE', 'REG', 'COMMA', 'REG'],

    # Movimiento inmediato (con valor)
    'MOVI': ['OPCODE', 'REG', 'COMMA', 'IMM'],
    'MVNI': ['OPCODE', 'REG', 'COMMA', 'IMM'],

    # Comparaciones
    'CMP':  ['OPCODE', 'REG', 'COMMA', 'REG'],
    'CMPS': ['OPCODE', 'REG', 'COMMA', 'PASS'],
    'CMN':  ['OPCODE', 'REG', 'COMMA', 'REG'],
    'TST':  ['OPCODE', 'REG', 'COMMA', 'REG'],
    'TEQ':  ['OPCODE', 'REG', 'COMMA', 'REG'],

    # Comparaciones inmediatas
    'CMPI': ['OPCODE', 'REG', 'COMMA', 'IMM'],
    'CMNI': ['OPCODE', 'REG', 'COMMA', 'IMM'],
    'TSTI': ['OPCODE', 'REG', 'COMMA', 'IMM'],
    'TEQI': ['OPCODE', 'REG', 'COMMA', 'IMM'],

    # Operaciones de bifurcación
    'B': ['OPCODE', 'LABEL'],
    'BEQ': ['OPCODE', 'LABEL'],
    'BNE': ['OPCODE', 'LABEL'],
    'BLT': ['OPCODE', 'LABEL'],
    'BGT': ['OPCODE', 'LABEL'],

    # Operaciones especiales
    'SWI': ['OPCODE'],
    'NOP': ['OPCODE'],

    # Instrucciones de almacenamiento
    'LDR': ['OPCODE', 'REG', 'COMMA', 'MEM'],
    'STR': ['OPCODE', 'REG', 'COMMA', 'MEM'],
    'LDRB': ['OPCODE', 'REG', 'COMMA', 'MEM'],
    'STRB': ['OPCODE', 'REG', 'COMMA', 'MEM'],

    # Instrucciones de clave
    'PRINTI': ['OPCODE', 'MEM'],
    'PRINTS': ['OPCODE', 'MEM'],
    'PRINTB': ['OPCODE', 'MEM'],
    'LOGOUT': ['OPCODE'],
    'STRK': ['OPCODE', 'KWORD', 'IMM'],
    'STRPASS': ['OPCODE', 'PASS', 'IMM'],

    'AUTHCMP': ['OPCODE'],

    'TEA': ['OPCODE', 'IMM', 'COMMA', 'IMM'],
    
    'TEAENC': [
    ['OPCODE', 'IMM'],                     # TEAENC #2
    ['OPCODE', 'IMM', 'COMMA', 'KWORD']    # TEAENC #1, k1
],
    'TEAD': [['OPCODE', 'IMM'], ['OPCODE', 'IMM', 'COMMA', 'KWORD']],


}

def parse_tokens(tokens):
    if not tokens:
        return False, "Línea vacía o sin tokens"

    op = tokens[0][1]
    expected = instruction_patterns.get(op)

    if expected is None:
        return False, f"Instrucción no reconocida: {op}"

    actual_types = [tok[0] for tok in tokens]

    # Si hay múltiples formas válidas (lista de listas)
    if isinstance(expected[0], list):
        for variant in expected:
            if actual_types == variant:
                return True, None
        return False, f"Sintaxis inválida para {op}. Esperado uno de: {expected}, obtenido: {actual_types}"

    # Forma única esperada
    if actual_types != expected:
        return False, f"Sintaxis inválida para {op}. Esperado: {expected}, obtenido: {actual_types}"

    return True, None
