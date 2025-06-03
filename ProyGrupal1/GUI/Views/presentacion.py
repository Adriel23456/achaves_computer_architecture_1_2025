"""
presentacion.py - Vista de presentación de la aplicación
"""
import tkinter as tk
from tkinter import ttk

class PresentacionView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario de la vista"""
        # Frame principal
        main_frame = self.design_manager.create_styled_frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contenido temporal
        label = self.design_manager.create_styled_label(
            main_frame,
            "VISTA DE PRESENTACIÓN",
            font_type='title'
        )
        label.pack(expand=True)
        
        # Descripción
        desc_label = self.design_manager.create_styled_label(
            main_frame,
            "Esta es la vista de presentación de la aplicación.\nAquí se mostrará la información inicial del programa.",
            font_type='normal'
        )
        desc_label.pack(pady=20)