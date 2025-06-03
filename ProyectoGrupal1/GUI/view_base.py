"""
view_base.py - Vista base de la aplicación con sidebar
"""
import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path
from GUI.controller import ViewController
from GUI.design import DesignManager

class Application:
    def __init__(self, base_dir, config_path):
        self.base_dir = base_dir
        self.config_path = config_path
        self.config = self._load_config()
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Aplicación de Análisis")
        
        # Configurar diseño
        self.design_manager = DesignManager(self.base_dir, self.config)
        
        # Aplicar configuración inicial
        self._apply_window_config()
        
        # Crear contenedores principales
        self._create_main_containers()
        
        # Configurar controlador de vistas
        self.controller = ViewController(
            self.content_frame, 
            self.base_dir, 
            self.config,
            self.design_manager,
            self._on_config_change
        )
        
        # Crear sidebar
        self._create_sidebar()
        
        # Cargar vista inicial
        self.controller.show_view("Presentación")
        
        # Configurar eventos
        self._setup_events()
        
    def _load_config(self):
        """Carga la configuración desde el archivo JSON"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_config(self):
        """Guarda la configuración actual en el archivo JSON"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
    
    def _apply_window_config(self):
        """Aplica la configuración de ventana"""
        window_config = self.config['window']
        
        # Configurar geometría
        self.root.geometry(f"{window_config['width']}x{window_config['height']}+{window_config['x']}+{window_config['y']}")
        
        # Configurar fullscreen si es necesario
        if window_config['fullscreen']:
            self.root.attributes('-fullscreen', True)
        
        # Configurar tema
        self.design_manager.apply_theme(self.root, self.config['theme']['current'])
    
    def _create_main_containers(self):
        """Crea los contenedores principales de la aplicación"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar frame con estilo personalizado
        self.sidebar_frame = ttk.Frame(
            self.main_frame, 
            width=self.config['sidebar']['width'],
            style='Sidebar.TFrame'
        )
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        
        # Content frame
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _create_sidebar(self):
        """Crea el sidebar con los botones de navegación"""
        # Obtener colores del tema actual
        colors = self.design_manager.get_colors()
        
        # Título del sidebar
        title_frame = tk.Frame(self.sidebar_frame, bg=colors['sidebar_bg'])
        title_frame.pack(fill=tk.X, pady=(20, 10))
        
        title_label = tk.Label(
            title_frame,
            text="MENÚ",
            font=self.design_manager.get_font('title'),
            bg=colors['sidebar_bg'],
            fg=colors['sidebar_button_fg']
        )
        title_label.pack()
        
        # Separador
        separator = ttk.Separator(self.sidebar_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Frame para los botones
        buttons_frame = tk.Frame(self.sidebar_frame, bg=colors['sidebar_bg'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Botones del sidebar
        self.sidebar_buttons = {}
        views = ["Presentación", "Compilador", "CPU", "Análisis", "Configuración", "Créditos"]
        
        for i, view_name in enumerate(views):
            # Frame para cada botón (para mejor control del padding)
            btn_frame = tk.Frame(buttons_frame, bg=colors['sidebar_bg'])
            btn_frame.pack(fill=tk.X, pady=2)
            
            btn = ttk.Button(
                btn_frame,
                text=view_name,
                command=lambda v=view_name: self._on_view_button_click(v),
                style='Sidebar.TButton'
            )
            btn.pack(fill=tk.X, padx=5)
            self.sidebar_buttons[view_name] = btn
        
        # Marcar el primer botón como activo
        self._update_active_button("Presentación")
        
        # Frame inferior (para futuros elementos)
        bottom_frame = tk.Frame(self.sidebar_frame, bg=colors['sidebar_bg'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    def _on_view_button_click(self, view_name):
        """Maneja el click en un botón del sidebar"""
        self.controller.show_view(view_name)
        self._update_active_button(view_name)
    
    def _update_active_button(self, active_view):
        """Actualiza el estilo del botón activo"""
        for view_name, button in self.sidebar_buttons.items():
            if view_name == active_view:
                button.configure(style='Active.Sidebar.TButton')
            else:
                button.configure(style='Sidebar.TButton')
    
    def _setup_events(self):
        """Configura los eventos de la ventana"""
        # Guardar configuración al cambiar tamaño o posición
        self.root.bind('<Configure>', self._on_window_configure)
        
        # Atajos de teclado
        self.root.bind('<F11>', lambda e: self._toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self._exit_fullscreen())
        
        # Cerrar aplicación correctamente
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _on_window_configure(self, event):
        """Maneja los cambios de configuración de la ventana"""
        if event.widget == self.root:
            # Actualizar configuración solo si no estamos en fullscreen
            if not self.root.attributes('-fullscreen'):
                self.config['window']['width'] = self.root.winfo_width()
                self.config['window']['height'] = self.root.winfo_height()
                self.config['window']['x'] = self.root.winfo_x()
                self.config['window']['y'] = self.root.winfo_y()
                self._save_config()
    
    def _on_config_change(self, key, value):
        """Callback cuando la configuración cambia desde una vista"""
        if key == 'fullscreen':
            self.root.attributes('-fullscreen', value)
            self.config['window']['fullscreen'] = value
        elif key == 'theme':
            self.config['theme']['current'] = value
            self.design_manager.apply_theme(self.root, value)
            # Recrear sidebar para aplicar nuevos estilos
            for widget in self.sidebar_frame.winfo_children():
                widget.destroy()
            self._create_sidebar()
        elif key == 'font_size':
            self.config['theme']['font_size'] = value
            self.design_manager.update_font_size(value)
            # Actualizar fuentes en toda la aplicación
            self._refresh_fonts()
        
        self._save_config()
    
    def _refresh_fonts(self):
        """Actualiza las fuentes en toda la aplicación"""
        # Actualizar sidebar
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()
        self._create_sidebar()
        
        # Notificar al controlador para actualizar la vista actual
        self.controller.refresh_current_view()
    
    def _toggle_fullscreen(self):
        """Alterna el modo pantalla completa"""
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)
        self.config['window']['fullscreen'] = not current
        self._save_config()
    
    def _exit_fullscreen(self):
        """Sale del modo pantalla completa"""
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
            self.config['window']['fullscreen'] = False
            self._save_config()
    
    def _on_closing(self):
        """Maneja el cierre de la aplicación"""
        self._save_config()
        self.root.quit()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()