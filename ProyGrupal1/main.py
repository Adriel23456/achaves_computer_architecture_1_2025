#!/usr/bin/env python3
"""
main.py - Punto de entrada principal de la aplicación
"""
import os
import sys
import json
from pathlib import Path
import re


from ProyGrupal.ISA.lexer import lexer
from ProyGrupal.ISA.parser import parse_tokens
from ProyGrupal.ISA.encoder import encode_instruction


# Configurar el directorio base de la aplicación
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(BASE_DIR))

# Importar después de configurar el path
from GUI.view_base import Application

def ensure_config_exists():
    """Asegura que el archivo de configuración exista con valores por defecto"""
    config_path = BASE_DIR / "Assets" / "config.json"
    
    # Crear directorios si no existen
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configuración por defecto
    default_config = {
        "window": {
            "width": 1200,
            "height": 700,
            "x": 100,
            "y": 100,
            "fullscreen": False
        },
        "theme": {
            "current": "dark",
            "font_size": 12,
            "font_family": "JetBrainsMono-Regular"
        },
        "sidebar": {
            "width": 200
        }
    }
    
    # Si no existe el archivo, crearlo con valores por defecto
    if not config_path.exists():
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
    
    return config_path

def main():
    """Función principal de la aplicación"""
    # Asegurar que la configuración existe
    config_path = ensure_config_exists()
    
    # Crear y ejecutar la aplicación
    app = Application(BASE_DIR, config_path)
    app.run()

    input_file = "ProyGrupal/Assembly/programa.asm"
    output_file = "ProyGrupal/Simulator/programa.bin"


    # Compiler
    binarios = []

    with open(input_file) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()

            # Ignorar comentarios completos y líneas vacías
            if not line or line.startswith(';'):
                continue

            # Detectar etiquetas
            if re.match(r'^\.\w+:?$', line):
                print(f"[Línea {lineno}] 🏷️ Etiqueta: {line}")
                continue

            try:
                tokens = lexer(line)
                valid, error = parse_tokens(tokens)

                if not valid:
                    print(f"[Línea {lineno}] ❌ Error de sintaxis: {error}")
                else:
                    print(f"[Línea {lineno}] ✅ Correcto: {tokens}")
                    binary = encode_instruction(tokens)
                    print(f"[Línea {lineno}] 🟢 Binario: {binary}")
                    binarios.append(binary)

            except Exception as e:
                print(f"[Línea {lineno}] ⚠️ Excepción: {e}")

    # Guardar binarios en archivo de salida
    with open(output_file, 'w') as f:
        for b in binarios:
            f.write(b + '\n')

    print(f"\n✅ Compilación completada. Binario guardado en: {output_file}")

if __name__ == "__main__":
    main()