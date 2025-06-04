instruction_patterns = {
    'ADD':     ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'SUB':     ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'REG'],
    'ADDI':    ['OPCODE', 'REG', 'COMMA', 'REG', 'COMMA', 'IMM'],
    'MOVI':    ['OPCODE', 'REG', 'COMMA', 'IMM'],
    'STR':     ['OPCODE', 'REG', 'COMMA', 'MEM'],
    'TEA':     ['OPCODE', 'IMM', 'COMMA', 'IMM'],
    'STRK':    ['OPCODE', 'KWORD', 'IMM'],
    'STRPASS': ['OPCODE', 'PASS', 'IMM'],
    'NOP':     ['OPCODE'],
    'LOGOUT':  ['OPCODE'],
    'B':       ['OPCODE', 'LABEL'],
    'PRINTL':  ['OPCODE', 'IMM'],
    # Puedes agregar más aquí según avances
}

def parse_tokens(tokens):
    if not tokens:
        return False, "Línea vacía o sin tokens"

    op = tokens[0][1]
    expected = instruction_patterns.get(op)

    if expected is None:
        return False, f"Instrucción no reconocida: {op}"

    actual_types = [tok[0] for tok in tokens]
    if actual_types != expected:
        return False, f"Sintaxis inválida para {op}. Esperado: {expected}, obtenido: {actual_types}"

    return True, None
