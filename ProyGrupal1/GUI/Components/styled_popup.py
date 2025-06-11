"""
styled_popup.py - Componente de ventana popup estilizada
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_button import StyledButton
from GUI.Components.styled_scrollbar import StyledVerticalScrollbar

class StyledPopup(tk.Toplevel):
    """Ventana popup modal estilizada"""
    def __init__(self, parent, design_manager, title="Popup", width_percent=0.85, height_percent=0.85):
        # Obtener la ventana principal
        self.parent_window = parent.winfo_toplevel()
        
        # Inicializar como Toplevel
        super().__init__(self.parent_window)
        
        self.design_manager = design_manager
        self.title(title)
        
        # Configurar como modal
        self.transient(self.parent_window)
        self.grab_set()
        
        # Calcular dimensiones basadas en porcentaje de la ventana principal
        parent_width = self.parent_window.winfo_width()
        parent_height = self.parent_window.winfo_height()
        popup_width = int(parent_width * width_percent)
        popup_height = int(parent_height * height_percent)
        
        # Calcular posición para centrar
        parent_x = self.parent_window.winfo_x()
        parent_y = self.parent_window.winfo_y()
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        
        # Configurar geometría
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        # Evitar redimensionamiento
        self.resizable(False, False)
        
        # Aplicar tema
        colors = design_manager.get_colors()
        self.configure(bg=colors['bg'])
        
        # Crear contenido
        self._create_content()
        
        # Vincular tecla Escape para cerrar
        self.bind('<Escape>', lambda e: self.close())
        
        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        # Focus al popup
        self.focus_set()
    
    def _create_content(self):
        """Crea el contenido del popup - debe ser sobrescrito por subclases"""
        colors = self.design_manager.get_colors()
        
        # Frame principal
        main_frame = tk.Frame(self, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def close(self):
        """Cierra el popup y devuelve el control"""
        self.grab_release()
        self.destroy()


class TextViewerPopup(StyledPopup):
    """Popup específico para mostrar texto con scroll"""
    def __init__(self, parent, design_manager, title="Visor de Texto", content="", read_only=True):
        self.content = content
        self.read_only = read_only
        super().__init__(parent, design_manager, title)
    
    def _create_content(self):
        """Crea el contenido específico para mostrar texto"""
        colors = self.design_manager.get_colors()
        
        # Frame principal
        main_frame = tk.Frame(self, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar grid
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para el texto
        text_frame = tk.Frame(main_frame, bg=colors['bg'], relief=tk.SOLID, borderwidth=1)
        text_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 10))
        text_frame.configure(highlightbackground=colors['button_bg'])
        text_frame.configure(highlightcolor=colors['select_bg'])
        text_frame.configure(highlightthickness=1)
        
        # Scrollbar
        scrollbar = StyledVerticalScrollbar(text_frame, self.design_manager)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Widget de texto
        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=self.design_manager.get_font('normal'),
            bg=colors['entry_bg'],
            fg=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg'],
            yscrollcommand=scrollbar.set,
            state=tk.NORMAL,
            padx=10,
            pady=10,
            borderwidth=0,
            highlightthickness=0
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)
        
        # Insertar contenido
        if self.content:
            self.text_widget.insert('1.0', self.content)
        
        # Si es solo lectura, deshabilitar edición
        if self.read_only:
            self.text_widget.config(state=tk.DISABLED)
        
        # Frame para el botón
        button_frame = tk.Frame(main_frame, bg=colors['bg'])
        button_frame.grid(row=1, column=0, sticky='ew')
        
        # Botón cerrar centrado
        btn_close = StyledButton(
            button_frame,
            text="Cerrar",
            command=self.close,
            design_manager=self.design_manager
        )
        btn_close.pack()