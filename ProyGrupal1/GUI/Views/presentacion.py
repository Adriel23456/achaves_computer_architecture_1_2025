"""
presentacion.py - Vista de presentación de la aplicación
"""
import tkinter as tk
from tkinter import ttk, filedialog
import hashlib
import os
from GUI.Components.styled_console import StyledConsole
from GUI.Components.styled_button import StyledButton

class PresentacionView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        
        # Crear la consola como atributo de instancia para acceso posterior
        self.console = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario de la vista"""
        colors = self.design_manager.get_colors()
        
        # Frame principal con padding
        main_frame = tk.Frame(self.parent, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid con pesos para que la consola se expanda
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para la consola (ocupará la mayor parte del espacio)
        console_frame = tk.Frame(main_frame, bg=colors['bg'])
        console_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 10))
        
        # Crear el componente de consola
        self.console = StyledConsole(console_frame, self.design_manager)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Frame para los botones
        buttons_frame = tk.Frame(main_frame, bg=colors['bg'])
        buttons_frame.grid(row=1, column=0, sticky='ew')
        
        # Centrar los botones
        buttons_container = tk.Frame(buttons_frame, bg=colors['bg'])
        buttons_container.pack(expand=True)
        
        # Botón "Cargar Memoria Dinámica"
        btn_cargar = StyledButton(
            buttons_container,
            text="Cargar Memoria Dinámica",
            command=self._on_cargar_memoria,
            design_manager=self.design_manager
        )
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        # Botón "Obtener MD5"
        btn_md5 = StyledButton(
            buttons_container,
            text="Obtener MD5",
            command=self._on_obtener_md5,
            design_manager=self.design_manager
        )
        btn_md5.pack(side=tk.LEFT, padx=5)
        
        # Botón "Prueba de Encriptación"
        btn_enc_test = StyledButton(
            buttons_container,
            text="Prueba de Encriptación",
            command=self._on_encriptar_tea,     # reutilizamos la misma callback
            design_manager=self.design_manager
        )
        btn_enc_test.pack(side=tk.LEFT, padx=5)
        
        # Agregar texto de bienvenida
        self._add_welcome_message()
    
    def _add_welcome_message(self):
        """Agrega un mensaje de bienvenida a la consola"""
        self.console.printConsoleLn("=== Simulador de CPU - Grupo 5 ===")
        self.console.printConsoleLn("")
    
    #SE TIENE QUE ARREGLAR, LO CORRECTO ES GENERAR UN ARCHIVO "dinamic_mem.bin" en Assets que contenga todo en bits
    def _on_cargar_memoria(self):
        """Maneja el click del botón Cargar Memoria Dinámica"""
        # 1) Diálogo para elegir el archivo
        # Construir la ruta de la carpeta
        out_path = os.path.join(self.base_dir)
        # Obtener la ventana principal para el diálogo
        root = self.parent.winfo_toplevel()
        # Guardar el estado actual de la ventana
        was_grab = root.grab_current()
        # Abrir el diálogo de selección de archivos
        archivo = filedialog.askopenfilename(
            parent=root,
            title="Seleccionar archivo como memoria dinámica",
            initialdir=out_path
        )
        # Restaurar el estado de la ventana
        if was_grab:
            was_grab.grab_set()
            
        # 2) Comprobaciones básicas
        if not archivo:
            self.console.printConsoleLn("[INFO] No se seleccionó ningún archivo")
            return
        if not os.path.isfile(archivo):
            self.console.printConsoleLn(f"[ERROR] '{archivo}' no es un archivo válido")
            return
        
        try:
            # ================================================================
            # PASO 1  ▸ Leer todos los bytes del archivo
            # ================================================================
            with open(archivo, "rb") as f:
                data = f.read()

            byte_len = len(data)
            if byte_len == 0:
                raise ValueError("El archivo está vacío")

            # ================================================================
            # PASO 2  ▸ Alinear a múltiplo de 8 bytes (64 bits)
            # ================================================================
            resto = byte_len % 8
            if resto != 0:
                pad = 8 - resto
                data += b"\x00" * pad
                byte_len += pad

            # ================================================================
            # PASO 3  ▸ Generar la lista de bloques de 32 bits
            #          (2 palabras de 32 bits por cada 64 bits)
            # ================================================================
            bloques_32 = []
            for i in range(0, byte_len, 4):
                word_bytes = data[i : i + 4]           # siempre 4 bytes
                word_int   = int.from_bytes(word_bytes, byteorder="big")
                bloques_32.append(f"0x{word_int:08X}") # => 0xDEADBEEF

            # ================================================================
            # PASO 4  ▸ Escribirlos en el Excel con CPUInfoExcel
            #          Columna 31: etiqueta   «D_MemN»
            #          Columna 32: valor hex  «0xXXXXXXXX»
            # ================================================================
            tabla = self.cpu_excel.table          # acceso directo a TableControl
            for fila, valor in enumerate(bloques_32, start=1):
                etiqueta = f"D_Mem{fila-1}"
                tabla.write(fila, 31, etiqueta)   # nombre de la celda
                tabla.write(fila, 32, valor)      # valor de 32 bits

            # Commit masivo al libro (idéntico a reset())
            tabla.execute_all()

            # Mensajes en consola
            self.console.printConsoleLn(f"[INFO] Memoria dinámica cargada: {os.path.basename(archivo)}")
            self.console.printConsoleLn(f"[INFO] Bytes leídos: {byte_len}")
            self.console.printConsoleLn(f"[INFO] Palabras escritas (32 bits): {len(bloques_32)}")

        except Exception as e:
            self.console.printConsoleLn(f"[ERROR] No se pudo cargar la memoria dinámica: {e}")
    
    def _on_obtener_md5(self):
        """Maneja el click del botón Obtener MD5"""
        # Construir la ruta de la carpeta 'out'
        out_path = os.path.join(self.base_dir, 'out')
        
        # Crear la carpeta 'out' si no existe
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        
        # Obtener la ventana principal para el diálogo
        root = self.parent.winfo_toplevel()
        
        # Guardar el estado actual de la ventana
        was_grab = root.grab_current()
        
        # Abrir el diálogo de selección de archivos
        archivo_seleccionado = filedialog.askopenfilename(
            parent=root,
            title="Seleccionar archivo para calcular MD5",
            initialdir=out_path
        )
        
        # Restaurar el estado de la ventana
        if was_grab:
            was_grab.grab_set()
        
        # Si se seleccionó un archivo
        if archivo_seleccionado:
            try:
                # Calcular MD5
                md5_hash = self.calc_md5(archivo_seleccionado)
                
                # Mostrar resultado en la consola
                self.console.printConsoleLn(f"[INFO] Archivo seleccionado: {os.path.basename(archivo_seleccionado)}")
                self.console.printConsoleLn(f"[INFO] MD5: {md5_hash}")
                
            except Exception as e:
                self.console.printConsoleLn(f"[ERROR] No se pudo calcular el MD5: {str(e)}")
        else:
            self.console.printConsoleLn("[INFO] No se seleccionó ningún archivo")
    
    def calc_md5(self, filepath):
        """Calcula el hash MD5 de un archivo"""
        md5_hash = hashlib.md5()
        
        # Leer el archivo en bloques para manejar archivos grandes
        with open(filepath, "rb") as f:
            # Leer en bloques de 4096 bytes
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        
        return md5_hash.hexdigest()
    
    def printConsoleLn(self, value):
        """Método público para imprimir en la consola desde fuera de la vista"""
        if self.console:
            self.console.printConsoleLn(value)
    
    # ─────────────────────────────────────────────────────────────────────────────
    def _to_uint32(self, value) -> int:
        """
        Convierte 'value' (int o str) a un entero sin signo de 32 bits.
        Acepta:
            • int           (se devuelve tal cual & 0xFFFFFFFF)
            • "0x…" / "0X…" (hexadecimal)
            • "0b…" / "0B…" (binario)
            • "1234…"       (decimal)
        """
        if isinstance(value, int):
            return value & 0xFFFFFFFF

        if not isinstance(value, str):
            raise ValueError(f"Tipo no soportado: {type(value)}")

        v = value.strip()
        if v.lower().startswith("0x"):
            return int(v, 16) & 0xFFFFFFFF
        if v.lower().startswith("0b"):
            return int(v, 2)  & 0xFFFFFFFF
        return int(v) & 0xFFFFFFFF
    
    def _on_encriptar_tea(self):
        """Encripta todos los bloques de memoria dinámica con TEA y genera un .enc."""
        try:
            tbl = self.cpu_excel.table

            # ─── Delta ───────────────────────────────────────────────
            delta_val = self.cpu_excel.read_d0_safe()[1]   # segundo elemento de la tupla
            delta     = self._to_uint32(delta_val)

            # ─── Clave k[0..3] ───────────────────────────────────────
            k = []
            for fn in (self.cpu_excel.read_k0_0,
                    self.cpu_excel.read_k0_1,
                    self.cpu_excel.read_k0_2,
                    self.cpu_excel.read_k0_3):
                k.append(self._to_uint32(fn()[1]))

            # ─── Recorremos la memoria dinámica ──────────────────────
            fila = 1
            words_after = []

            while True:
                t0 = tbl.read_immediate(fila,     32)
                t1 = tbl.read_immediate(fila + 1, 32)

                if not t0 or not t0[1]:
                    break            # fin de datos

                if not t1 or not t1[1]:
                    self.console.printConsoleLn("[WARN] Número impar de palabras; última sin encriptar.")
                    break

                v0 = self._to_uint32(t0[1])
                v1 = self._to_uint32(t1[1])

                v0, v1 = self.tea_encripcion(v0, v1, delta, k)

                tbl.write(fila,     32, f"0x{v0:08X}")
                tbl.write(fila + 1, 32, f"0x{v1:08X}")

                words_after.extend([v0, v1])
                fila += 2

            if not words_after:
                self.console.printConsoleLn("[WARN] No se encontraron datos para encriptar.")
                return

            tbl.execute_all()

            # ─── Generar .enc ─────────────────────────────────────────
            out_bytes = bytearray(w.to_bytes(4, "big") for w in words_after)

            out_path = os.path.join(self.base_dir, "out")
            os.makedirs(out_path, exist_ok=True)

            root = self.parent.winfo_toplevel()
            was_grab = root.grab_current()

            file_name = filedialog.asksaveasfilename(
                parent=root,
                title="Guardar archivo encriptado",
                initialdir=out_path,
                defaultextension=".enc",
                filetypes=[("Encrypted file", "*.enc"), ("All files", "*.*")]
            )

            if was_grab:
                was_grab.grab_set()

            if file_name:
                with open(file_name, "wb") as f:
                    f.write(out_bytes)
                self.console.printConsoleLn(f"[INFO] Archivo encriptado guardado en: {file_name}")
            else:
                self.console.printConsoleLn("[INFO] Guardado cancelado.")

        except Exception as e:
            self.console.printConsoleLn(f"[ERROR] Encriptación fallida: {e}")
    
    # ─────────────────────────────────────────────────────────────────────────────
    # TEA de 32 rondas: encripta un bloque de 64 bits (dos palabras de 32 bits)
    # ─────────────────────────────────────────────────────────────────────────────
    def tea_encripcion(self, v0: int, v1: int, delta: int, k: list[int]) -> tuple[int, int]:
        """Devuelve (v0', v1') después de 32 rondas de TEA."""
        sum_  = 0
        mask  = 0xFFFFFFFF  # para simular overflow de 32 bits
        for _ in range(32):
            sum_ = (sum_ + delta) & mask
            v0   = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum_) ^ ((v1 >> 5) + k[1]))) & mask
            v1   = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum_) ^ ((v0 >> 5) + k[3]))) & mask
        return v0, v1