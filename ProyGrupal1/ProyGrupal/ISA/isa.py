# isa.py

OPCODES = {
    'ADD':     '000000000',
    'SUB':     '000000001',
    'ADDI':    '000000110',
    'MOVI':    '000011110',
    'STR':     '000100001',
    'TEA':     '001000100',
    'STRK':    '001000010',
    'STRPASS': '001000011',
    'NOP':     '000110101',
    'LOGOUT':  '001000001',
    'B':       '000101111',
    'PRINTL':  '000111111'
}

# R o w: 1 para R, 0 para w
def encode_register(regname):
    reg_type = '1' if regname.startswith('R') else '0'
    number = int(regname[1:])
    return reg_type + format(number, '05b')  # total 6 bits
