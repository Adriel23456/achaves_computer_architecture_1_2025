"""
configuracion.py - Vista de configuración de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox

class ConfiguracionView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        
        # Variables de control
        self.window_width_var = tk.StringVar(value=str(config['window']['width']))
        self.window_height_var = tk.StringVar(value=str(config['window']['height']))
        self.font_size_var = tk.IntVar(value=config['theme']['font_size'])
        self.fullscreen_var = tk.BooleanVar(value=config['window']['fullscreen'])
        self.theme_var = tk.StringVar(value=config['theme']['current'])
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario de la vista"""
        # Frame principal con padding
        main_frame = self.design_manager.create_styled_frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = self.design_manager.create_styled_label(
            main_frame,
            "CONFIGURACIÓN",
            font_type='title'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de contenido con scroll
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Aplicar colores del tema
        colors = self.design_manager.get_colors()
        canvas.configure(bg=colors['content_bg'])
        
        # Sección: Tamaño de ventana
        self._create_window_size_section(scrollable_frame)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=tk.X, pady=20)
        
        # Sección: Tamaño de fuente
        self._create_font_size_section(scrollable_frame)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=tk.X, pady=20)
        
        # Sección: Pantalla completa
        self._create_fullscreen_section(scrollable_frame)
        
        # Separador
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=tk.X, pady=20)
        
        # Sección: Tema
        self._create_theme_section(scrollable_frame)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_window_size_section(self, parent):
        """Crea la sección de configuración del tamaño de ventana"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=10)
        
        # Título de sección
        section_label = self.design_manager.create_styled_label(
            section_frame,
            "Tamaño de Ventana",
            font_type='bold'
        )
        section_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para controles
        controls_frame = ttk.Frame(section_frame)
        controls_frame.pack(fill=tk.X, padx=20)
        
        # Ancho
        width_frame = ttk.Frame(controls_frame)
        width_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(width_frame, text="Ancho:", width=15).pack(side=tk.LEFT)
        width_entry = ttk.Entry(width_frame, textvariable=self.window_width_var, width=10)
        width_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(width_frame, text="píxeles").pack(side=tk.LEFT)
        
        # Alto
        height_frame = ttk.Frame(controls_frame)
        height_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(height_frame, text="Alto:", width=15).pack(side=tk.LEFT)
        height_entry = ttk.Entry(height_frame, textvariable=self.window_height_var, width=10)
        height_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(height_frame, text="píxeles").pack(side=tk.LEFT)
        
        # Botón aplicar
        apply_button = self.design_manager.create_styled_button(
            controls_frame,
            "Aplicar Tamaño",
            self._apply_window_size
        )
        apply_button.pack(pady=10)
    
    def _create_font_size_section(self, parent):
        """Crea la sección de configuración del tamaño de fuente"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=10)
        
        # Título de sección
        section_label = self.design_manager.create_styled_label(
            section_frame,
            "Tamaño de Fuente",
            font_type='bold'
        )
        section_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para controles
        controls_frame = ttk.Frame(section_frame)
        controls_frame.pack(fill=tk.X, padx=20)
        
        # Frame para el slider
        slider_frame = ttk.Frame(controls_frame)
        slider_frame.pack(fill=tk.X, pady=5)
        
        # Etiqueta de valor actual
        value_label = ttk.Label(slider_frame, text=f"Tamaño: {self.font_size_var.get()}pt")
        value_label.pack()
        
        # Slider
        font_scale = ttk.Scale(
            slider_frame,
            from_=8,
            to=24,
            orient=tk.HORIZONTAL,
            variable=self.font_size_var,
            command=lambda v: value_label.config(text=f"Tamaño: {int(float(v))}pt")
        )
        font_scale.pack(fill=tk.X, pady=5)
        
        # Botón aplicar
        apply_button = self.design_manager.create_styled_button(
            controls_frame,
            "Aplicar Tamaño de Fuente",
            self._apply_font_size
        )
        apply_button.pack(pady=10)
    
    def _create_fullscreen_section(self, parent):
        """Crea la sección de pantalla completa"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=10)
        
        # Título de sección
        section_label = self.design_manager.create_styled_label(
            section_frame,
            "Modo Pantalla Completa",
            font_type='bold'
        )
        section_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para controles
        controls_frame = ttk.Frame(section_frame)
        controls_frame.pack(fill=tk.X, padx=20)
        
        # Checkbox
        fullscreen_check = ttk.Checkbutton(
            controls_frame,
            text="Activar pantalla completa",
            variable=self.fullscreen_var,
            command=self._toggle_fullscreen
        )
        fullscreen_check.pack(pady=5)
        
        # Nota
        note_label = self.design_manager.create_styled_label(
            controls_frame,
            "Nota: Presiona F11 o ESC para salir del modo pantalla completa",
            font_type='small'
        )
        note_label.pack(pady=5)
    
    def _create_theme_section(self, parent):
        """Crea la sección de selección de tema"""
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=10)
        
        # Título de sección
        section_label = self.design_manager.create_styled_label(
            section_frame,
            "Tema de la Aplicación",
            font_type='bold'
        )
        section_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para controles
        controls_frame = ttk.Frame(section_frame)
        controls_frame.pack(fill=tk.X, padx=20)
        
        # Radio buttons para temas
        theme_frame = ttk.Frame(controls_frame)
        theme_frame.pack(pady=5)
        
        dark_radio = ttk.Radiobutton(
            theme_frame,
            text="Tema Oscuro",
            variable=self.theme_var,
            value="dark",
            command=self._change_theme
        )
        dark_radio.pack(side=tk.LEFT, padx=10)
        
        light_radio = ttk.Radiobutton(
            theme_frame,
            text="Tema Claro",
            variable=self.theme_var,
            value="light",
            command=self._change_theme
        )
        light_radio.pack(side=tk.LEFT, padx=10)
        
        # Vista previa de colores
        preview_frame = ttk.LabelFrame(controls_frame, text="Vista previa", padding=10)
        preview_frame.pack(pady=10, fill=tk.X)
        
        self.preview_labels = []
        preview_texts = ["Texto normal", "Botón de muestra", "Entrada de texto"]
        
        for text in preview_texts:
            label = ttk.Label(preview_frame, text=text)
            label.pack(pady=2)
            self.preview_labels.append(label)
    
    def _apply_window_size(self):
        """Aplica el nuevo tamaño de ventana"""
        try:
            width = int(self.window_width_var.get())
            height = int(self.window_height_var.get())
            
            # Validar valores
            if width < 400 or height < 300:
                messagebox.showwarning(
                    "Tamaño inválido",
                    "El tamaño mínimo de la ventana es 400x300 píxeles"
                )
                return
            
            if width > 3840 or height > 2160:
                messagebox.showwarning(
                    "Tamaño inválido",
                    "El tamaño máximo de la ventana es 3840x2160 píxeles"
                )
                return
            
            # Obtener la ventana principal
            root = self.parent.winfo_toplevel()
            
            # Aplicar nuevo tamaño
            root.geometry(f"{width}x{height}")
            
            # Actualizar configuración
            self.config['window']['width'] = width
            self.config['window']['height'] = height
            
            messagebox.showinfo("Éxito", "Tamaño de ventana actualizado")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def _apply_font_size(self):
        """Aplica el nuevo tamaño de fuente"""
        new_size = self.font_size_var.get()
        self.on_config_change('font_size', new_size)
        messagebox.showinfo("Éxito", "Tamaño de fuente actualizado")
    
    def _toggle_fullscreen(self):
        """Activa/desactiva el modo pantalla completa"""
        fullscreen = self.fullscreen_var.get()
        self.on_config_change('fullscreen', fullscreen)
    
    def _change_theme(self):
        """Cambia el tema de la aplicación"""
        new_theme = self.theme_var.get()
        self.on_config_change('theme', new_theme)
        
        # Actualizar vista previa
        self._update_preview()
    
    def _update_preview(self):
        """Actualiza la vista previa de colores"""
        colors = self.design_manager.get_colors(self.theme_var.get())
        
        # Actualizar colores de las etiquetas de vista previa
        for label in self.preview_labels:
            label.configure(
                background=colors['label_bg'],
                foreground=colors['label_fg']
            )