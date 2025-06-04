import re

# Reglas de tokens, ordenadas correctamente (REG antes de OPCODE, etc.)
token_specification = [
    ('LABEL',   r'\.\w+'),  # Etiquetas como .Linicio
    ('REG',     r'[Rw]\d+'),  # Registros: R0-R15, w1-w9
    ('MEM',     r'[GDVP]\[[Rw]\d+(?:,\s*#?-?\d+)?\]'),  # G[R1], D[w3, #4], etc.
    ('KWORD',   r'k\d\.\d'),  # Claves criptográficas como k0.0
    ('OPCODE',  r'[A-Z]+'),  # Nombres de instrucciones
    ('IMM',     r'#0x[0-9A-Fa-f]+|#-?\d+'),  # Inmediatos hex o decimales
    ('PASS',    r'\d'),  # Para STRPASS y CMPS
    ('COMMA',   r','),  # Coma
    ('SKIP',    r'[ \t]+'),  # Espacios y tabs
    ('NEWLINE', r'\n'),  # Saltos de línea
    ('MISMATCH',r'.'),  # Cualquier otro carácter inesperado
]

# Compilación del patrón principal
token_re = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)

def lexer(line):
    # Eliminar comentarios al estilo ensamblador (; ...)
    line = line.split(';')[0].strip()

    tokens = []
    for mo in re.finditer(token_re, line):
        kind = mo.lastgroup
        value = mo.group()
        if kind in ('SKIP', 'NEWLINE') or not value:
            continue
        if kind == 'MISMATCH':
            raise SyntaxError(f'Caracter inesperado: {value}')
        tokens.append((kind, value))
    return tokens
