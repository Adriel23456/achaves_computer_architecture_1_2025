"""
design.py - Manejador de diseño y temas de la aplicación
"""
import tkinter as tk
from tkinter import ttk, font
from pathlib import Path

class DesignManager:
    def __init__(self, base_dir, config):
        self.base_dir = base_dir
        self.config = config
        
        # Definir paletas de colores CORREGIDAS
        self.themes = {
            'dark': {
                'bg': '#1e1e1e',
                'fg': '#ffffff',
                'select_bg': '#3a3a3a',
                'select_fg': '#ffffff',
                'button_bg': '#2d2d2d',
                'button_fg': '#ffffff',
                'button_active': '#404040',
                'button_hover': '#353535',
                'entry_bg': '#2d2d2d',
                'entry_fg': '#ffffff',
                'frame_bg': '#1e1e1e',
                'label_bg': '#1e1e1e',
                'label_fg': '#ffffff',
                'sidebar_bg': '#252525',
                'sidebar_button_bg': '#2d2d2d',
                'sidebar_button_fg': '#ffffff',
                'sidebar_button_active_bg': '#007ACC',
                'sidebar_button_active_fg': '#ffffff',
                'content_bg': '#1e1e1e'
            },
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'select_bg': '#e0e0e0',
                'select_fg': '#000000',
                'button_bg': '#f0f0f0',
                'button_fg': '#000000',
                'button_active': '#d0d0d0',
                'button_hover': '#e8e8e8',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'frame_bg': '#ffffff',
                'label_bg': '#ffffff',
                'label_fg': '#000000',
                'sidebar_bg': '#f5f5f5',
                'sidebar_button_bg': '#e8e8e8',
                'sidebar_button_fg': '#000000',
                'sidebar_button_active_bg': '#0078D4',
                'sidebar_button_active_fg': '#ffffff',  # Siempre blanco en botón activo
                'content_bg': '#ffffff'
            }
        }
        
        # Cargar fuentes
        self._load_fonts()
        
        # Configurar estilos ttk
        self.style = ttk.Style()
        self._configure_styles()
    
    def _load_fonts(self):
        """Carga las fuentes personalizadas"""
        font_path = self.base_dir / "assets" / "fonts" / "ttf"
        font_file = font_path / f"{self.config['theme']['font_family']}.ttf"
        
        # Verificar si el archivo de fuente existe
        if not font_file.exists():
            # Buscar cualquier fuente JetBrainsMono disponible
            jetbrains_fonts = list(font_path.glob("JetBrainsMono-*.ttf"))
            if jetbrains_fonts:
                font_file = jetbrains_fonts[0]
                self.config['theme']['font_family'] = font_file.stem
        
        # Crear fuentes
        base_size = self.config['theme']['font_size']
        
        self.fonts = {
            'normal': font.Font(family='Consolas', size=base_size),
            'bold': font.Font(family='Consolas', size=base_size, weight='bold'),
            'title': font.Font(family='Consolas', size=base_size + 4, weight='bold'),
            'small': font.Font(family='Consolas', size=base_size - 2),
            'large': font.Font(family='Consolas', size=base_size + 6)
        }
    
    def _configure_styles(self):
        """Configura los estilos ttk"""
        current_theme = self.config['theme']['current']
        colors = self.themes[current_theme]
        
        # Estilo general
        self.style.configure('TFrame', background=colors['frame_bg'])
        self.style.configure('TLabel', background=colors['label_bg'], foreground=colors['label_fg'])
        
        # Estilos de botones generales - CORREGIDO
        self.style.configure(
            'TButton',
            background=colors['button_bg'],
            foreground=colors['button_fg'],
            borderwidth=1,
            relief='flat',
            padding=(10, 5)
        )
        self.style.map(
            'TButton',
            background=[
                ('active', colors['button_hover']), 
                ('pressed', colors['button_active'])
            ],
            foreground=[
                ('active', colors['button_fg']),  # Mantener el color de texto
                ('pressed', colors['button_fg'])   # Mantener el color de texto
            ]
        )
        
        # Estilo específico para botones del sidebar - CORREGIDO
        self.style.configure(
            'Sidebar.TButton',
            background=colors['sidebar_button_bg'],
            foreground=colors['sidebar_button_fg'],
            borderwidth=0,
            relief='flat',
            padding=(10, 15),  # Más padding vertical
            anchor='w'
        )
        self.style.map(
            'Sidebar.TButton',
            background=[
                ('active', colors['button_hover']), 
                ('pressed', colors['button_active'])
            ],
            foreground=[
                ('active', colors['sidebar_button_fg']),  # Mantener el color de texto
                ('pressed', colors['sidebar_button_fg'])   # Mantener el color de texto
            ]
        )
        
        # Estilo para botón activo del sidebar
        self.style.configure(
            'Active.Sidebar.TButton',
            background=colors['sidebar_button_active_bg'],
            foreground=colors['sidebar_button_active_fg'],
            borderwidth=0,
            relief='flat',
            padding=(10, 15),  # Más padding vertical
            anchor='w'
        )
        self.style.map(
            'Active.Sidebar.TButton',
            background=[
                ('active', colors['sidebar_button_active_bg']), 
                ('pressed', colors['sidebar_button_active_bg'])
            ],
            foreground=[
                ('active', colors['sidebar_button_active_fg']),
                ('pressed', colors['sidebar_button_active_fg'])
            ]
        )
        
        # Estilos de entrada - CORREGIDO
        self.style.configure(
            'TEntry',
            fieldbackground=colors['entry_bg'],
            foreground=colors['entry_fg'],
            insertcolor=colors['entry_fg'],
            borderwidth=1,
            relief='solid'
        )
        
        # Estilos de Combobox
        self.style.configure(
            'TCombobox',
            fieldbackground=colors['entry_bg'],
            foreground=colors['entry_fg'],
            selectbackground=colors['select_bg'],
            selectforeground=colors['select_fg'],
            arrowcolor=colors['fg']
        )
        
        # Estilos de Checkbutton
        self.style.configure(
            'TCheckbutton',
            background=colors['bg'],
            foreground=colors['fg'],
            focuscolor='none'
        )
        self.style.map(
            'TCheckbutton',
            background=[('active', colors['bg'])],
            foreground=[('active', colors['fg'])]
        )
        
        # Estilos de Radiobutton
        self.style.configure(
            'TRadiobutton',
            background=colors['bg'],
            foreground=colors['fg'],
            focuscolor='none'
        )
        self.style.map(
            'TRadiobutton',
            background=[('active', colors['bg'])],
            foreground=[('active', colors['fg'])]
        )
        
        # Estilos de Scale
        self.style.configure(
            'TScale',
            background=colors['bg'],
            troughcolor=colors['button_bg'],
            sliderlength=20,
            borderwidth=0
        )
        
        # Estilos de LabelFrame
        self.style.configure(
            'TLabelframe',
            background=colors['bg'],
            foreground=colors['fg'],
            borderwidth=1,
            relief='solid'
        )
        self.style.configure(
            'TLabelframe.Label',
            background=colors['bg'],
            foreground=colors['fg']
        )
        
        # Estilo para el frame del sidebar
        self.style.configure(
            'Sidebar.TFrame',
            background=colors['sidebar_bg']
        )
        
        # Estilo para separadores
        self.style.configure(
            'TSeparator',
            background=colors['button_bg']
        )
    
    def apply_theme(self, root, theme_name):
        """Aplica un tema a la ventana principal"""
        if theme_name not in self.themes:
            theme_name = 'dark'
        
        colors = self.themes[theme_name]
        
        # Configurar colores de la ventana principal
        root.configure(bg=colors['bg'])
        
        # Actualizar estilos ttk
        self.config['theme']['current'] = theme_name
        self._configure_styles()
        
        # Actualizar estilo global
        root.option_add('*Background', colors['bg'])
        root.option_add('*Foreground', colors['fg'])
        root.option_add('*Entry.Background', colors['entry_bg'])
        root.option_add('*Entry.Foreground', colors['entry_fg'])
        root.option_add('*Text.Background', colors['entry_bg'])
        root.option_add('*Text.Foreground', colors['entry_fg'])
    
    def get_font(self, font_type='normal'):
        """Retorna una fuente específica"""
        return self.fonts.get(font_type, self.fonts['normal'])
    
    def update_font_size(self, new_size):
        """Actualiza el tamaño de todas las fuentes"""
        self.config['theme']['font_size'] = new_size
        
        # Recrear fuentes con nuevo tamaño
        self.fonts = {
            'normal': font.Font(family='Consolas', size=new_size),
            'bold': font.Font(family='Consolas', size=new_size, weight='bold'),
            'title': font.Font(family='Consolas', size=new_size + 4, weight='bold'),
            'small': font.Font(family='Consolas', size=new_size - 2),
            'large': font.Font(family='Consolas', size=new_size + 6)
        }
    
    def get_colors(self, theme=None):
        """Retorna los colores del tema actual o especificado"""
        if theme is None:
            theme = self.config['theme']['current']
        return self.themes.get(theme, self.themes['dark'])
    
    def create_styled_frame(self, parent, **kwargs):
        """Crea un frame con el estilo del tema actual"""
        colors = self.get_colors()
        frame = ttk.Frame(parent, **kwargs)
        return frame
    
    def create_styled_label(self, parent, text, font_type='normal', **kwargs):
        """Crea una etiqueta con el estilo del tema actual"""
        label = ttk.Label(
            parent,
            text=text,
            font=self.get_font(font_type),
            **kwargs
        )
        return label
    
    def create_styled_button(self, parent, text, command, **kwargs):
        """Crea un botón con el estilo del tema actual"""
        button = ttk.Button(
            parent,
            text=text,
            command=command,
            **kwargs
        )
        return button