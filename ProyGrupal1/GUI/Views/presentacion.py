"""
presentacion.py - Vista de presentación de la aplicación
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_console import StyledConsole
from GUI.Components.styled_button import StyledButton

class PresentacionView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        
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
        self.console.printConsoleLn("Bienvenido al simulador de CPU.")
        self.console.printConsoleLn("Use los botones inferiores para cargar memoria o calcular MD5.")
        self.console.printConsoleLn("")
    
    def _on_cargar_memoria(self):
        """Maneja el click del botón Cargar Memoria Dinámica"""
        self.console.printConsoleLn("[INFO] Botón 'Cargar Memoria Dinámica' presionado")
        print("Click en Cargar Memoria Dinámica")  # Para debugging
    
    def _on_obtener_md5(self):
        """Maneja el click del botón Obtener MD5"""
        self.console.printConsoleLn("[INFO] Botón 'Obtener MD5' presionado")
        print("Click en Obtener MD5")  # Para debugging
    
    def printConsoleLn(self, value):
        """Método público para imprimir en la consola desde fuera de la vista"""
        if self.console:
            self.console.printConsoleLn(value)