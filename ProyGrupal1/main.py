#!/usr/bin/env python3
"""
main.py – Punto de entrada de la aplicación y compilador de 2 pasadas
"""
import os, sys, json, re
from pathlib import Path

# ────────────────────────────────────────────
#  Rutas y GUI inicial (sin cambios)
# ────────────────────────────────────────────
BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, str(BASE_DIR))

from ProyGrupal.ISA.lexer   import lexer
from ProyGrupal.ISA.parser  import parse_tokens
from ProyGrupal.ISA.encoder import encode_instruction
from GUI.view_base          import Application


# ----------  Configuración GUI (igual que antes)  ----------
def ensure_config_exists():
    cfg = BASE_DIR / "Assets" / "config.json"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    if not cfg.exists():
        json.dump({
            "window": {"width":1200,"height":700,"x":100,"y":100,"fullscreen":False},
            "theme" : {"current":"dark","font_size":12,"font_family":"JetBrainsMono-Regular"},
            "sidebar":{"width":200}
        }, cfg.open("w", encoding="utf-8"), indent=4)
    return cfg


# ----------  utilidades  ----------
BRANCH_OPS = {'B', 'BEQ', 'BNE', 'BLT', 'BGT'}
PSEUDO_OPS = {'TEA', 'TEAENC', 'TEAD', 'AUTHCMP'}

def count_real_instructions(tokens):
    """
    Devuelve cuántas instrucciones REALES genera este token‑list.
    Para pseudoinstrucciones preguntamos al encoder; para el resto 1.
    """
    try:
        result = encode_instruction(tokens)     # sin tabla/índice
        return len(result) if isinstance(result, list) else 1
    except Exception:
        # Branch sin tabla -> 1; cualquier otra excepción pequeña: 1
        return 1


# ────────────────────────────────────────────
#  Compilador de DOS PASADAS
# ────────────────────────────────────────────
def compile_asm(input_file, output_file):
    # ---------- PASADA 1: recolectar etiquetas ----------
    label_table = {}        # {'.Loop': índice_instrucción}
    parsed_lines = []       # [(lineno, raw_line, tokens)]
    instr_index  = 0        # cuenta de instrucciones REALES

    with open(input_file, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.split(';')[0].strip()
            if not line:
                continue

            if re.match(r'^\.\w+:?$', line):            # etiqueta
                label_table[line.rstrip(':')] = instr_index
                continue

            tokens = lexer(line)
            parsed_lines.append((lineno, line, tokens))
            instr_index += count_real_instructions(tokens)

    # ---------- PASADA 2: generar binarios ----------
    binarios = []
    pc = 0                      # índice de instrucción real durante 2ª pasada

    for lineno, line, tokens in parsed_lines:
        try:
            # Validación sintáctica
            ok, err = parse_tokens(tokens)
            if not ok:
                print(f"[Línea {lineno}] ❌ {err}")
                continue

            # Compilar
            if tokens[0][1] in BRANCH_OPS:
                binary = encode_instruction(
                    tokens,
                    label_table=label_table,
                    current_index=pc
                )
            else:
                binary = encode_instruction(tokens)

            # Registrar salida y actualizar pc
            if isinstance(binary, list):
                for i, b in enumerate(binary, 1):
                    print(f"[Línea {lineno}.{i}] 🟢 {b}")
                binarios.extend(binary)
                pc += len(binary)
            else:
                print(f"[Línea {lineno}] 🟢 {binary}")
                binarios.append(binary)
                pc += 1

        except Exception as e:
            print(f"[Línea {lineno}] ⚠️ {e}")

    # Guardar archivo .bin
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write("\n".join(binarios))

    print(f"\n✅ Compilación completada. Binario guardado en: {output_file}")


# ────────────────────────────────────────────
#  main(): lanza GUI y luego compila
# ────────────────────────────────────────────
def main():
    cfg = ensure_config_exists()
    Application(BASE_DIR, cfg).run()          # GUI

    asm_file = BASE_DIR / "ProyGrupal" / "Assembly"  / "programa.asm"
    bin_file = BASE_DIR / "ProyGrupal" / "Simulator" / "programa.bin"
    compile_asm(asm_file, bin_file)


if __name__ == "__main__":
    main()
