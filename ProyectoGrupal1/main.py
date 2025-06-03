import time
from ExtraPrograms.table_control import TableControl


def mostrar_menu():
    """Muestra el menú de opciones"""
    print("\n" + "="*60)
    print("📋 MENÚ DE CONTROL")
    print("="*60)
    print("1 - Ejecutar TODAS las acciones pendientes")
    print("2 - Ejecutar SOLO las acciones de LECTURA")
    print("3 - Ejecutar SOLO las acciones de ESCRITURA")
    print("4 - Reordenar cola (Lecturas primero, Escrituras después)")
    print("5 - Ver cantidad de acciones en cola")
    print("6 - Limpiar cola")
    print("7 - Salir")
    print("-"*60)


def agregar_bloque_1(tc):
    """Agrega el primer bloque de acciones"""
    print("\n🔵 BLOQUE 1: Tipos de datos básicos (mezclados)")
    print("-"*40)
    
    # Mezclar escrituras y lecturas
    tc.write(2, 1, "'Hola Mundo'")
    tc.write(3, 1, '"Este es un string con comillas dobles"')
    tc.read(2, 1, lambda s, v: print(f"    📖 Callback: {v}") if s else None)
    
    tc.write(2, 2, "0d42")
    tc.write(3, 2, "0d1234567890")
    tc.read(3, 1, lambda s, v: print(f"    📖 Callback: {v}") if s else None)
    
    tc.write(2, 3, "0b1010")
    tc.read(2, 2, lambda s, v: print(f"    📖 Callback: {v}") if s else None)
    tc.write(3, 3, "0b11111111")
    
    tc.write(2, 4, "0xCAFE")
    tc.write(3, 4, "0xDEADBEEF")
    tc.read(2, 3, lambda s, v: print(f"    📖 Callback: {v}") if s else None)
    
    print(f"\n✓ {tc.get_queue_size()} acciones agregadas (lecturas y escrituras mezcladas)")


def agregar_bloque_2(tc):
    """Agrega el segundo bloque de acciones con números grandes"""
    print("\n🔶 BLOQUE 2: Números grandes (128 bits) y más lecturas")
    print("-"*40)
    
    # Primero algunas lecturas de lo anterior
    tc.read(3, 2, lambda s, v: print(f"    📖 Valor decimal: {v}") if s else None)
    tc.read(3, 4, lambda s, v: print(f"    📖 Valor hex: {v}") if s else None)
    
    # Número binario de 128 bits
    binary_128 = "0b" + "1" * 128
    tc.write(6, 1, f"'Binario 128 bits'")
    tc.write(6, 3, binary_128)
    
    # Más lecturas intercaladas
    tc.read(6, 1, lambda s, v: print(f"    📖 Descripción: {v}") if s else None)
    
    # Número hexadecimal de 128 bits (32 caracteres hex)
    hex_128 = "0x" + "F" * 32
    tc.write(7, 1, "'Hexadecimal 128 bits'")
    tc.write(7, 4, hex_128)
    
    # Otra lectura
    tc.read(6, 3, lambda s, v: print(f"    📖 Binario grande: {v[:50]}...") if s else None)
    
    # Número decimal muy grande
    tc.write(8, 1, "'Decimal grande'")
    tc.write(8, 2, "0d340282366920938463463374607431768211455")  # 2^128 - 1
    
    print(f"\n✓ {tc.get_queue_size()} acciones agregadas (mezcladas)")


def agregar_bloque_3(tc):
    """Agrega el tercer bloque con patrones específicos"""
    print("\n🔷 BLOQUE 3: Patrón escritura-lectura-escritura")
    print("-"*40)
    
    # Patrón: escribir, leer lo escrito, escribir más
    for i in range(3):
        row = 11 + i
        tc.write(row, 1, f"'Iteración {i+1}'")
        tc.write(row, 2, f"0d{1000 + i}")
        tc.read(row, 1, lambda s, v, r=row: print(f"    📖 Fila {r}: {v}") if s else None)
        tc.write(row, 3, f"0b{'1' * (8 + i*4)}")
        tc.read(row, 2, lambda s, v, r=row: print(f"    📖 Fila {r}: {v}") if s else None)
        tc.write(row, 4, f"0x{format(255 + i*100, 'X')}")
    
    print(f"\n✓ {tc.get_queue_size()} acciones agregadas (patrón específico)")


def probar_funcionalidades(tc):
    """Prueba las diferentes funcionalidades de ejecución"""
    print("\n🧪 DEMOSTRACIÓN DE FUNCIONALIDADES")
    print("="*60)
    
    # Agregar acciones de prueba
    print("\n1️⃣ Agregando acciones de prueba...")
    tc.write(20, 1, "'Test escritura 1'")
    tc.read(2, 1, lambda s, v: print(f"    📖 Test lectura 1: {v}") if s else None)
    tc.write(20, 2, "'Test escritura 2'")
    tc.read(3, 1, lambda s, v: print(f"    📖 Test lectura 2: {v}") if s else None)
    tc.write(20, 3, "'Test escritura 3'")
    tc.read(2, 2, lambda s, v: print(f"    📖 Test lectura 3: {v}") if s else None)
    
    print(f"   Total en cola: {tc.get_queue_size()} (3 escrituras, 3 lecturas)")
    
    input("\n   Presiona ENTER para ejecutar SOLO las lecturas...")
    tc.execute_reads_only()
    
    input("\n   Presiona ENTER para ejecutar SOLO las escrituras...")
    tc.execute_writes_only()
    
    print("\n2️⃣ Probando reordenamiento...")
    tc.write(21, 1, "'Nueva escritura 1'")
    tc.read(20, 1, lambda s, v: print(f"    📖 Nueva lectura 1: {v}") if s else None)
    tc.write(21, 2, "'Nueva escritura 2'")
    tc.read(20, 2, lambda s, v: print(f"    📖 Nueva lectura 2: {v}") if s else None)
    
    print(f"   Acciones agregadas (mezcladas): {tc.get_queue_size()}")
    
    input("\n   Presiona ENTER para reordenar (lecturas primero)...")
    tc.reorder_reads_first()
    
    input("\n   Presiona ENTER para ejecutar todo en el nuevo orden...")
    tc.execute_all()


def main():
    """Función principal con control manual de ejecución"""
    print("=" * 80)
    print("🚀 SISTEMA DE CONTROL DE TABLA - MODO MANUAL")
    print("=" * 80)
    
    # Crear instancia (siempre en modo manual ahora)
    tc = TableControl()
    print(f"✓ Archivo: {tc.filename}")
    
    # Variables de control
    bloque_actual = 1
    bloques_ejecutados = set()
    
    # Primero mostrar demostración de funcionalidades
    demo = input("\n¿Deseas ver una demostración de las funcionalidades? (s/n): ").lower()
    if demo == 's':
        probar_funcionalidades(tc)
        input("\n✅ Demostración completada. Presiona ENTER para continuar con el programa principal...")
        tc.clear_queue()  # Limpiar cola después de la demo
    
    while True:
        # Agregar bloques según corresponda
        if bloque_actual == 1 and 1 not in bloques_ejecutados:
            agregar_bloque_1(tc)
            bloques_ejecutados.add(1)
        elif bloque_actual == 2 and 2 not in bloques_ejecutados:
            agregar_bloque_2(tc)
            bloques_ejecutados.add(2)
        elif bloque_actual == 3 and 3 not in bloques_ejecutados:
            agregar_bloque_3(tc)
            bloques_ejecutados.add(3)
        
        mostrar_menu()
        
        try:
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                acciones_pendientes = tc.get_queue_size()
                if acciones_pendientes > 0:
                    print(f"\n⏳ Ejecutando TODAS las {acciones_pendientes} acciones...")
                    start_time = time.time()
                    
                    ejecutadas = tc.execute_all()
                    
                    elapsed_time = time.time() - start_time
                    print(f"\n✅ Completado en {elapsed_time:.2f} segundos")
                    
                    # Avanzar al siguiente bloque si hay
                    if bloque_actual < 3:
                        bloque_actual += 1
                        print(f"\n🎯 Preparado para cargar BLOQUE {bloque_actual}")
                    else:
                        print("\n🏁 Todos los bloques han sido procesados")
                else:
                    print("\n⚠️ No hay acciones pendientes en la cola")
                    
            elif opcion == "2":
                tc.execute_reads_only()
                
            elif opcion == "3":
                tc.execute_writes_only()
                
            elif opcion == "4":
                tc.reorder_reads_first()
                
            elif opcion == "5":
                total = tc.get_queue_size()
                print(f"\n📊 Acciones en cola: {total}")
                if total > 0:
                    print("   (Usa opción 4 para ver el orden actual)")
                
            elif opcion == "6":
                if tc.get_queue_size() > 0:
                    confirmacion = input("¿Estás seguro de limpiar la cola? (s/n): ").lower()
                    if confirmacion == 's':
                        tc.clear_queue()
                else:
                    print("\n⚠️ La cola ya está vacía")
                
            elif opcion == "7":
                if tc.get_queue_size() > 0:
                    print(f"\n⚠️ Hay {tc.get_queue_size()} acciones pendientes")
                    confirmacion = input("¿Salir sin ejecutarlas? (s/n): ").lower()
                    if confirmacion != 's':
                        continue
                print("\n👋 Saliendo del programa...")
                break
                
            else:
                print("\n❌ Opción inválida. Por favor seleccione 1-7")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Programa interrumpido por el usuario")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print("\n" + "="*80)
    print("✅ PROGRAMA FINALIZADO")
    print("="*80)
    
    # Estadísticas finales
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   - Bloques procesados: {len(bloques_ejecutados)}/3")
    print(f"   - Acciones pendientes: {tc.get_queue_size()}")
    print(f"   - Archivo generado: {tc.filename}")
    print("\n💡 Abre el archivo Excel para ver todos los cambios!")
    
    # Esperar un momento antes de cerrar
    time.sleep(2)


if __name__ == "__main__":
    main()