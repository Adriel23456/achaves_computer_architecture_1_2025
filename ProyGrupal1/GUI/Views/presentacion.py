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
        
        # Agregar texto de bienvenida
        self._add_welcome_message()
    
    def _add_welcome_message(self):
        """Agrega un mensaje de bienvenida a la consola"""
        self.console.printConsoleLn("=== Simulador de CPU - Grupo 5 ===")
        self.console.printConsoleLn("")
    
    def _on_cargar_memoria(self):
        """Maneja el click del botón Cargar Memoria Dinámica"""
        # Construir la ruta de la carpeta
        out_path = os.path.join(self.base_dir)
        # Obtener la ventana principal para el diálogo
        root = self.parent.winfo_toplevel()
        # Guardar el estado actual de la ventana
        was_grab = root.grab_current()
        # Abrir el diálogo de selección de archivos
        archivo_seleccionado = filedialog.askopenfilename(
            parent=root,
            title="Seleccionar archivo como memoria dinámica",
            initialdir=out_path
        )
        # Restaurar el estado de la ventana
        if was_grab:
            was_grab.grab_set()
        # Si se seleccionó un archivo
        if archivo_seleccionado:
            try:
                # Determinar que el archivo sea divisible por 8 bytes (tiene que tener bloques cerrados de 64 bits), si no es divisible por 64, entonces rellenar los bits faltantes con ceros
                
                # Obtener todos los bloques de 32bits del archivo y ponerlos en una lista
                
                # Escribir en el excel todos los valores de los bloques de 32bits usando el formato correcto
                
                # Mostrar resultado en la consola
                self.console.printConsoleLn(f"[INFO] Memoria dinámica cargada: {os.path.basename(archivo_seleccionado)}")
            except Exception as e:
                self.console.printConsoleLn(f"[ERROR] No se pudo cargar la memoria dinámica: {str(e)}")
        else:
            self.console.printConsoleLn("[INFO] No se seleccionó ningún archivo")
    
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