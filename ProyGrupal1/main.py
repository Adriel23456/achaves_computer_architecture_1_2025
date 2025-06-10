#!/usr/bin/env python3
"""
main.py - Punto de entrada principal de la aplicación
"""
import os
import sys
import json
from pathlib import Path

# Configurar el directorio base de la aplicación
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(BASE_DIR))

# Importar después de configurar el path
from GUI.view_base import Application
from ExtraPrograms.cpu_info_excel import CPUInfoExcel

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
    # Inicializar la clase de información de CPU
    cpu_excel = CPUInfoExcel()
    #cpu_excel.reset(False) #Resetea la información de CPU al inicio
    
    #cpu_excel.write_k0_0("0xDEADBEEA")
    #cpu_excel.write_k0_1("0xDEADBEEB")
    #cpu_excel.write_k0_2("0xDEADBEEC")
    #cpu_excel.write_k0_3("0xDEADBEED")
    #cpu_excel.table.execute_all()
    #val1 = cpu_excel.read_k0_0()
    #val2 = cpu_excel.read_k0_1()
    #val3 = cpu_excel.read_k0_2()
    #val4 = cpu_excel.read_k0_3()
    #print(f"k0[{1}] = {val1}")
    #print(f"k0[{2}] = {val2}")
    #print(f"k0[{3}] = {val3}")
    #print(f"k0[{4}] = {val4}")
    
    #Ejemplos de lectura y escritura:
    #value = cpu_excel.write_memory_at_address("0x0", "0xDEADBEEF")
    #value = cpu_excel.read_memory_at_address("0x0")
    #print("Valor es:")
    #print(value)
    
    #cpu_excel.write_dynamic_memory("0x0", "0xDEADBEEF")
    #value = cpu_excel.read_dynamic_memory("0x0")
    #print("Valor es:")
    #print(value)
    
    """Función principal de la aplicación"""
    # Asegurar que la configuración existe
    config_path = ensure_config_exists()
    
    # Crear y ejecutar la aplicación
    app = Application(BASE_DIR, config_path, cpu_excel)
    app.run()
    
if __name__ == "__main__":
    main()