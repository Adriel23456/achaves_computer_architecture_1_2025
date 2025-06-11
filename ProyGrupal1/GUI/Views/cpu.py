"""
cpu.py - Vista de CPU
"""
import tkinter as tk
from tkinter import ttk

class CPUView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel, controller):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        self.controller = controller
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario de la vista"""
        # Frame principal
        main_frame = self.design_manager.create_styled_frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contenido temporal
        label = self.design_manager.create_styled_label(
            main_frame,
            "VISTA DE CPU",
            font_type='title'
        )
        label.pack(expand=True)
        
        # Descripción
        desc_label = self.design_manager.create_styled_label(
            main_frame,
            "Esta es la vista de CPU.\nAquí se mostrará información y control del procesador.",
            font_type='normal'
        )
        desc_label.pack(pady=20)