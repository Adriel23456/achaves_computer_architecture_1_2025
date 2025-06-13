"""
compile_service.py - Servicio de compilación ASM a binario
"""
import re
import os
from pathlib import Path

def compile_text_to_binary(asm_text, print_callback=None, base_dir=None):
    """
    Compila código ASM a binario y lo guarda en Assets/instruction_mem.bin.
    
    Args:
        asm_text: Texto del código ASM
        print_callback: Función para imprimir mensajes (opcional)
        base_dir: Directorio base del proyecto (opcional, se autodetecta si no se proporciona)
        
    Returns:
        bytes: Contenido binario compilado o None si hay errores
    """
    from ExtraPrograms.ISA.lexer import lexer
    from ExtraPrograms.ISA.parser import parse_tokens
    from ExtraPrograms.ISA.encoder import encode_instruction
    
    def log(msg):
        if print_callback:
            print_callback(msg)
    
    # Constantes
    BRANCH_OPS = {'B', 'BEQ', 'BNE', 'BLT', 'BGT'}
    
    def count_real_instructions(tokens):
        """Cuenta cuántas instrucciones reales genera este token-list"""
        try:
            result = encode_instruction(tokens)
            return len(result) if isinstance(result, list) else 1
        except Exception:
            return 1
    
    # PASADA 1: Recolectar etiquetas
    log("[COMPILADOR] Iniciando primera pasada - análisis de etiquetas")
    label_table = {}
    parsed_lines = []
    instr_index = 0
    
    lines = asm_text.strip().split('\n')
    for lineno, raw in enumerate(lines, 1):
        line = raw.split(';')[0].strip()
        if not line:
            continue
        
        # Detectar etiqueta
        if re.match(r'^\.\w+:?$', line):
            label_name = line.rstrip(':')
            label_table[label_name] = instr_index
            log(f"[COMPILADOR] Etiqueta encontrada: {label_name} -> índice {instr_index}")
            continue
        
        try:
            tokens = lexer(line)
            if tokens:
                parsed_lines.append((lineno, line, tokens))
                count = count_real_instructions(tokens)
                instr_index += count
        except Exception as e:
            log(f"[COMPILADOR] Error en línea {lineno}: {str(e)}")
            return
    
    log(f"[COMPILADOR] Primera pasada completa. {len(label_table)} etiquetas encontradas")
    
    # PASADA 2: Generar binarios
    log("[COMPILADOR] Iniciando segunda pasada - generación de código binario")
    binarios = []
    pc = 0
    errors = 0
    
    for lineno, line, tokens in parsed_lines:
        try:
            # Validación sintáctica
            ok, err = parse_tokens(tokens)
            if not ok:
                log(f"[COMPILADOR] Error sintáctico línea {lineno}: {err}")
                errors += 1
                continue
            
            # Compilar instrucción
            if tokens[0][1] in BRANCH_OPS:
                binary = encode_instruction(
                    tokens,
                    label_table=label_table,
                    current_index=pc
                )
                # Log información de branch para depuración
                if tokens[1][1] in label_table:
                    offset_inst = label_table[tokens[1][1]] - pc - 1
                    offset_bytes = offset_inst * 8
                    log(f"[COMPILADOR] Branch {tokens[0][1]} {tokens[1][1]}: "
                        f"desde PC={pc} hacia {label_table[tokens[1][1]]}, "
                        f"offset={offset_inst} instrucciones ({offset_bytes} bytes)")
            else:
                binary = encode_instruction(tokens)
            
            # Registrar salida
            if isinstance(binary, list):
                for i, b in enumerate(binary, 1):
                    log(f"[COMPILADOR] Línea {lineno}.{i}: {tokens[0][1]} -> {b}")
                binarios.extend(binary)
                pc += len(binary)
            else:
                log(f"[COMPILADOR] Línea {lineno}: {tokens[0][1]} -> {binary}")
                binarios.append(binary)
                pc += 1
                
        except Exception as e:
            log(f"[COMPILADOR] Error línea {lineno}: {str(e)}")
            errors += 1
    
    if errors > 0:
        log(f"[COMPILADOR] Compilación con {errors} errores")
        return None
    
    # Convertir a formato binario
    log(f"[COMPILADOR] Compilación exitosa. {len(binarios)} instrucciones generadas")
    
    # Convertir cada string de bits a bytes reales
    binary_data = bytearray()
    
    for i, bin_str in enumerate(binarios):
        # Verificar que la instrucción tenga 64 bits
        if len(bin_str) != 64:
            log(f"[COMPILADOR] Advertencia: Instrucción {i} tiene {len(bin_str)} bits, esperados 64")
            continue
        
        # Convertir string de bits a entero
        value = int(bin_str, 2)
        
        # Convertir a 8 bytes (64 bits) en big-endian
        bytes_data = value.to_bytes(8, byteorder='big')
        binary_data.extend(bytes_data)
    
    # Guardar en Assets/instruction_mem.bin
    if base_dir is None:
        # Auto-detectar el directorio base
        current_file = Path(__file__).resolve()
        # Subir 3 niveles: compile_service.py -> ISA -> ExtraPrograms -> [directorio base]
        base_dir = current_file.parent.parent.parent
    else:
        base_dir = Path(base_dir)
    
    # Crear ruta de destino
    target_path = base_dir / "Assets" / "instruction_mem.bin"
    
    try:
        # Crear directorio Assets si no existe
        target_path.parent.mkdir(exist_ok=True)
        
        # Escribir el archivo binario
        with open(target_path, 'wb') as f:
            f.write(binary_data)
        
        log(f"[COMPILADOR] Binario guardado en: {target_path}")
        log(f"[COMPILADOR] Tamaño del archivo: {len(binary_data)} bytes ({len(binarios)} instrucciones)")
        
    except Exception as e:
        log(f"[COMPILADOR] Error al guardar el archivo binario: {str(e)}")
        return None
    
    return bytes(binary_data)