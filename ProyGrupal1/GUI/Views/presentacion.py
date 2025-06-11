"""
presentacion.py - Vista de presentación de la aplicación
"""
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
import hashlib
import os
import time
from GUI.Components.styled_console import StyledConsole
from GUI.Components.styled_button import StyledButton

class PresentacionView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel, controller):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        self.controller = controller
        
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
            command=self._on_encriptar_tea,
            design_manager=self.design_manager
        )
        btn_enc_test.pack(side=tk.LEFT, padx=5)
        
        # Botón "Prueba de Desencriptación"
        btn_enc_test = StyledButton(
            buttons_container,
            text="Prueba de Desencriptación",
            command=self._on_desencriptar_tea,
            design_manager=self.design_manager
        )
        btn_enc_test.pack(side=tk.LEFT, padx=5)
        
        #Botón "Vaciar"
        btn_clear = StyledButton(
            buttons_container,
            text="Vaciar",
            command=self._on_clear_console,
            design_manager=self.design_manager
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Agregar texto de bienvenida
        self._add_welcome_message()
    
    def _add_welcome_message(self):
        """Agrega un mensaje de bienvenida a la consola"""
        self.console.printConsoleLn("=== Simulador de CPU - Grupo 5 ===")
        self.console.printConsoleLn("")
    
    def _on_cargar_memoria(self):
        """Maneja el click del botón Cargar Memoria Dinámica"""
        # 1) Diálogo para elegir el archivo
        out_path = os.path.join(self.base_dir)
        root = self.parent.winfo_toplevel()
        was_grab = root.grab_current()
        
        archivo = filedialog.askopenfilename(
            parent=root,
            title="Seleccionar archivo como memoria dinámica",
            initialdir=out_path
        )
        
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
            # Leer todos los bytes del archivo
            with open(archivo, "rb") as f:
                data = f.read()

            byte_len = len(data)
            if byte_len == 0:
                raise ValueError("El archivo está vacío")

            # Alinear a múltiplo de 8 bytes (64 bits)
            resto = byte_len % 8
            if resto != 0:
                pad = 8 - resto
                data += b"\x00" * pad
                byte_len += pad

            # Construir ruta al archivo dynamic_mem.bin
            current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            parent_dir = current_dir.parent.parent
            assets_dir = parent_dir / "Assets"
            bin_file = assets_dir / "dynamic_mem.bin"
            
            # Crear directorio Assets si no existe
            os.makedirs(assets_dir, exist_ok=True)
            
            # Escribir los datos al archivo binario
            with open(bin_file, 'wb') as f:
                f.write(data)

            # Mensajes en consola
            self.console.printConsoleLn(f"[INFO] Memoria dinámica cargada: {os.path.basename(archivo)}")
            self.console.printConsoleLn(f"[INFO] Bytes escritos: {byte_len}")
            self.console.printConsoleLn(f"[INFO] Bloques de 64 bits: {byte_len // 8}")

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
    
    def _on_clear_console(self):
        """Vacía completamente la consola de presentación."""
        if not self.console:
            return
        self.console.clear()
    
    def printConsoleLn(self, value):
        """Método público para imprimir en la consola desde fuera de la vista"""
        if self.console:
            self.console.printConsoleLn(value)
    
    # ─────────────────────────────────────────────────────────────────────────────
    # Parseo para obtener valores decimales apropiados
    # ─────────────────────────────────────────────────────────────────────────────
    def _parse_tea_value(self, value) -> int:
        """
        Parsea un valor para usarlo en TEA.
        NO convierte entre signo/sin signo, solo parsea el string a int.
        
        Args:
            value: int o str con el valor
            
        Returns:
            int: Valor parseado
        """
        if isinstance(value, int):
            return value
            
        if not isinstance(value, str):
            raise ValueError(f"Tipo no soportado: {type(value)}")
            
        v = value.strip()
        
        if v.lower().startswith("0x"):
            return int(v, 16)
        elif v.lower().startswith("0b"):
            return int(v, 2)
        elif v.lower().startswith("0d"):
            return int(v[2:])
        else:
            return int(v)

    # ─────────────────────────────────────────────────────────────────────────────
    # Encriptación TEA usando memoria dinámica desde cpu_excel
    # ─────────────────────────────────────────────────────────────────────────────
    def _on_encriptar_tea(self):
        """
        Lee cada bloque de 64 bits desde la memoria dinámica,
        aplica TEA y guarda el resultado.
        """
        start_time = time.time()
        try:
            # 1) Leer delta y claves (ya vienen con signo correcto)
            delta = self._parse_tea_value(self.cpu_excel.read_d0_safe()[1])
            k = [self._parse_tea_value(fn()[1]) for fn in (
                self.cpu_excel.read_k0_0,
                self.cpu_excel.read_k0_1,
                self.cpu_excel.read_k0_2,
                self.cpu_excel.read_k0_3
            )]

            # 2) Verificar archivo
            current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            parent_dir = current_dir.parent.parent
            bin_file = parent_dir / "Assets" / "dynamic_mem.bin"

            if not bin_file.exists():
                self.console.printConsoleLn("[ERROR] No se encontró dynamic_mem.bin.")
                return

            file_size = os.path.getsize(bin_file)
            num_blocks = file_size // 8

            # 3) Procesar bloques
            encrypted = bytearray()
            
            for block_idx in range(num_blocks):
                addr0 = block_idx * 8
                addr1 = block_idx * 8 + 4
                
                # Leer valores (ya vienen con signo correcto)
                v0 = self._parse_tea_value(self.cpu_excel.read_dynamic_memory(f"0x{addr0:X}"))
                v1 = self._parse_tea_value(self.cpu_excel.read_dynamic_memory(f"0x{addr1:X}"))
                
                # TEA trabaja con los valores tal como están
                v0_enc, v1_enc = self.tea_encripcion(v0, v1, delta, k)
                
                # Guardar resultado (interpretar como bytes)
                encrypted.extend((v0_enc & 0xFFFFFFFF).to_bytes(4, "little", signed=False))
                encrypted.extend((v1_enc & 0xFFFFFFFF).to_bytes(4, "little", signed=False))
                
                if (block_idx + 1) % 10 == 0:
                    self.console.printConsoleLn(f"[INFO] Procesados {block_idx + 1}/{num_blocks} bloques")

            # 4) Guardar
            out_dir = parent_dir / "out"
            out_dir.mkdir(exist_ok=True)
            out_path = out_dir / "dynamic_mem.enc"
            out_path.write_bytes(encrypted)

            self.console.printConsoleLn(f"[INFO] Archivo encriptado: {out_path}")
            self.console.printConsoleLn(f"[INFO] Bloques procesados: {num_blocks}")
            
            elapsed = time.time() - start_time
            self.console.printConsoleLn(f"[TIMER] Encriptación TEA duró {elapsed:.3f} segundos")

        except Exception as e:
            elapsed = time.time() - start_time
            self.console.printConsoleLn(f"[TIMER] Encriptación TEA abortada tras {elapsed:.3f} s")
            self.console.printConsoleLn(f"[ERROR] Encriptación fallida: {e}")
            
    # ─────────────────────────────────────────────────────────────────────────────
    # Des-encriptar usando memoria dinámica desde cpu_excel
    # ─────────────────────────────────────────────────────────────────────────────
    def _on_desencriptar_tea(self):
        """
        Lee cada bloque de 64 bits desde la memoria dinámica usando
        cpu_excel.read_dynamic_memory(), aplica 32 rondas inversas TEA
        y guarda el resultado en out/dynamic_mem.denc.
        """
        start_time = time.time()
        try:
            # 1) Delta y clave desde el Excel (idénticos a los usados para cifrar)
            delta = self._parse_tea_value(self.cpu_excel.read_d0_safe()[1])
            k = [self._parse_tea_value(fn()[1]) for fn in (
                self.cpu_excel.read_k0_0,
                self.cpu_excel.read_k0_1,
                self.cpu_excel.read_k0_2,
                self.cpu_excel.read_k0_3
            )]
            
            # 2) Verificar que existe el archivo de memoria dinámica
            current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            parent_dir  = current_dir.parent.parent
            bin_file    = parent_dir / "Assets" / "dynamic_mem.bin"

            if not bin_file.exists():
                self.console.printConsoleLn("[ERROR] No se encontró dynamic_mem.bin. "
                                            "Primero cargue la memoria.")
                return
                
            # Obtener tamaño del archivo
            file_size = os.path.getsize(bin_file)
            num_blocks = file_size // 8

            # 3) Leer memoria dinámica usando cpu_excel y des-encriptar
            decrypted = bytearray()
            
            for block_idx in range(num_blocks):
                # Calcular direcciones
                addr0 = block_idx * 8
                addr1 = block_idx * 8 + 4
                
                # Leer valores (ya vienen con signo correcto)
                v0 = self._parse_tea_value(self.cpu_excel.read_dynamic_memory(f"0x{addr0:X}"))
                v1 = self._parse_tea_value(self.cpu_excel.read_dynamic_memory(f"0x{addr1:X}"))
                
                # Aplicar TEA inverso
                v0_dec, v1_dec = self.tea_desencripcion(v0, v1, delta, k)
                
                # Agregar al resultado
                decrypted.extend(v0_dec.to_bytes(4, "little"))
                decrypted.extend(v1_dec.to_bytes(4, "little"))
                
                # Mensaje de progreso
                if (block_idx + 1) % 10 == 0:
                    self.console.printConsoleLn(f"[INFO] Procesados {block_idx + 1}/{num_blocks} bloques")

            if not decrypted:
                self.console.printConsoleLn("[WARN] No se encontraron datos para desencriptar.")
                return

            # 4) Guardar resultado
            out_path = parent_dir / "out" / "dynamic_mem.denc"
            out_path.write_bytes(decrypted)
            
            self.console.printConsoleLn(f"[INFO] Archivo desencriptado generado en: {out_path}")
            self.console.printConsoleLn(f"[INFO] Total de bloques desencriptados: {num_blocks}")
            
            elapsed = time.time() - start_time
            self.console.printConsoleLn(f"[TIMER] Desencriptación TEA duró {elapsed:.3f} segundos")
        except Exception as e:
            elapsed = time.time() - start_time
            self.console.printConsoleLn(f"[TIMER] Desencriptación TEA abortada tras {elapsed:.3f} s")
            self.console.printConsoleLn(f"[ERROR] Desencriptación fallida: {e}")

    # ─────────────────────────────────────────────────────────────────────────────
    # Algoritmo TEA de 32 rondas (sin cambios, sólo mensajes de depuración)
    # ─────────────────────────────────────────────────────────────────────────────
    def tea_encripcion(self, v0: int, v1: int, delta: int, k: list[int]) -> tuple[int, int]:
        """Devuelve (v0', v1') después de 32 rondas de TEA."""
        sum_ = 0
        mask = 0xFFFFFFFF
        for rnd in range(32):
            sum_ = (sum_ + delta) & mask
            v0   = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum_) ^ ((v1 >> 5) + k[1]))) & mask
            v1   = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum_) ^ ((v0 >> 5) + k[3]))) & mask
        return v0, v1
    
    # ─────────────────────────────────────────────────────────────────────────────
    # Algoritmo TEA – 32 rondas inversas (des-encriptar 64 bits)
    # ─────────────────────────────────────────────────────────────────────────────
    def tea_desencripcion(self, v0: int, v1: int, delta: int,
                          k: list[int]) -> tuple[int, int]:
        """
        Des-encripta un bloque (v0,v1) con 32 rondas TEA.
        Retorna las dos palabras originales.
        """
        mask  = 0xFFFFFFFF
        sum_  = (delta * 32) & mask       # valor inicial: delta * Nº rondas

        for rnd in range(32):
            v1 = (v1 - (((v0 << 4) + k[2]) ^ (v0 + sum_) ^ ((v0 >> 5) + k[3]))) & mask
            v0 = (v0 - (((v1 << 4) + k[0]) ^ (v1 + sum_) ^ ((v1 >> 5) + k[1]))) & mask
            sum_ = (sum_ - delta) & mask
        return v0, v1