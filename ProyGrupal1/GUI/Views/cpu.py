"""
cpu.py - Vista del CPU con diagrama interactivo
"""
import tkinter as tk
from tkinter import ttk
import math
from GUI.Components.styled_button import StyledButton

class CPUView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel, controller):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        self.controller = controller
        
        # Windows adicionales
        self.memory_window = None
        self.signals_window = None
        
        # Referencias a componentes
        self.diagram = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario de la vista"""
        colors = self.design_manager.get_colors()
        
        # Frame principal sin padding para usar todo el espacio
        main_frame = tk.Frame(self.parent, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid para las tres secciones
        main_frame.grid_rowconfigure(0, weight=0)  # Top (fijo)
        main_frame.grid_rowconfigure(1, weight=1)  # Center (expandible)
        main_frame.grid_rowconfigure(2, weight=0)  # Bottom (fijo)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # 1. Sección superior
        self._create_top_section(main_frame)
        
        # 2. Sección central
        self._create_center_section(main_frame)
        
        # 3. Sección inferior
        self._create_bottom_section(main_frame)
    
    def _create_top_section(self, parent):
        """Crea la sección superior con botones de visualización"""
        colors = self.design_manager.get_colors()
        
        # Frame para la sección superior
        top_frame = tk.Frame(parent, bg=colors['bg'], height=60)
        top_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=(20, 10))
        top_frame.grid_propagate(False)
        
        # Contenedor centrado para los botones
        buttons_container = tk.Frame(top_frame, bg=colors['bg'])
        buttons_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Botón "Mostrar Memorias"
        btn_memories = StyledButton(
            buttons_container,
            text="Mostrar Memorias",
            command=self._toggle_memories_window,
            design_manager=self.design_manager
        )
        btn_memories.pack(side=tk.LEFT, padx=10)
        
        # Botón "Mostrar Señales"
        btn_signals = StyledButton(
            buttons_container,
            text="Mostrar Señales",
            command=self._toggle_signals_window,
            design_manager=self.design_manager
        )
        btn_signals.pack(side=tk.LEFT, padx=10)
    
    def _create_center_section(self, parent):
        """Crea la sección central con el diagrama interactivo"""
        colors = self.design_manager.get_colors()
        
        # Frame para el diagrama
        center_frame = tk.Frame(parent, bg=colors['bg'])
        center_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        
        # Importar el componente del diagrama del pipeline
        from GUI.Components.cpu_pipeline_diagram import CPUPipelineDiagram
        
        # Crear el componente de diagrama del pipeline
        self.diagram = CPUPipelineDiagram(center_frame, self.design_manager, self.cpu_excel)
        self.diagram.pack(fill=tk.BOTH, expand=True)
        
        # >>> Carga inicial de señales e instrucciones <<<
        self.diagram.update_signals()
    
    def _create_bottom_section(self, parent):
        """Crea la sección inferior con botones de ejecución"""
        colors = self.design_manager.get_colors()
        
        # Frame para la sección inferior
        bottom_frame = tk.Frame(parent, bg=colors['bg'], height=60)
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(10, 20))
        bottom_frame.grid_propagate(False)
        
        # Contenedor centrado para los botones
        buttons_container = tk.Frame(bottom_frame, bg=colors['bg'])
        buttons_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Botón "Ejecutar Un Ciclo"
        btn_cycle = StyledButton(
            buttons_container,
            text="Ejecutar Un Ciclo",
            command=self._on_execute_cycle,
            design_manager=self.design_manager
        )
        btn_cycle.pack(side=tk.LEFT, padx=10)
        
        # Botón "Ejecutar Todo"
        btn_all = StyledButton(
            buttons_container,
            text="Ejecutar Todo",
            command=self._on_execute_all,
            design_manager=self.design_manager
        )
        btn_all.pack(side=tk.LEFT, padx=10)
    
    def _toggle_memories_window(self):
        """Muestra u oculta la ventana de memorias"""
        if self.memory_window and self.memory_window.winfo_exists():
            self.memory_window.destroy()
            self.memory_window = None
        else:
            self._create_memory_window()
    
    def _toggle_signals_window(self):
        """Muestra u oculta la ventana de señales"""
        if self.signals_window and self.signals_window.winfo_exists():
            self.signals_window.destroy()
            self.signals_window = None
        else:
            self._create_signals_window()
    
    def _create_memory_window(self):
        """Crea la ventana de memorias como extensión de la vista principal"""
        colors = self.design_manager.get_colors()
        root = self.parent.winfo_toplevel()
        
        # Crear ventana secundaria
        self.memory_window = tk.Toplevel(root)
        self.memory_window.title("Vista de Memorias")
        
        # Calcular tamaño (90% de la ventana principal)
        main_width = root.winfo_width()
        main_height = root.winfo_height()
        width = int(main_width * 0.9)
        height = int(main_height * 0.9)
        
        # Posicionar ligeramente desplazada de la ventana principal
        x = root.winfo_x() + 50
        y = root.winfo_y() + 50
        
        self.memory_window.geometry(f"{width}x{height}+{x}+{y}")
        self.memory_window.configure(bg=colors['bg'])
        
        # No hacer la ventana modal pero mantenerla encima
        self.memory_window.transient(root)
        
        # Frame principal
        main_frame = tk.Frame(self.memory_window, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Vista de Memorias",
            font=self.design_manager.get_font('title'),
            bg=colors['bg'],
            fg=colors['fg']
        )
        title_label.pack(pady=(0, 20))
        
        # Contenido placeholder
        content_frame = tk.Frame(main_frame, bg=colors['entry_bg'], relief=tk.SOLID, borderwidth=2)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        placeholder_label = tk.Label(
            content_frame,
            text="Vista de Memorias\n\nAquí se mostrarán los contenidos de las memorias del CPU",
            font=self.design_manager.get_font('normal'),
            bg=colors['entry_bg'],
            fg=colors['entry_fg']
        )
        placeholder_label.pack(expand=True)
        
        # Protocolo de cierre
        self.memory_window.protocol("WM_DELETE_WINDOW", lambda: self._toggle_memories_window())
    
    def _create_signals_window(self):
        """Crea la ventana de señales como extensión de la vista principal"""
        colors = self.design_manager.get_colors()
        root = self.parent.winfo_toplevel()
        
        # Crear ventana secundaria
        self.signals_window = tk.Toplevel(root)
        self.signals_window.title("Vista de Señales")
        
        # Calcular tamaño (90% de la ventana principal)
        main_width = root.winfo_width()
        main_height = root.winfo_height()
        width = int(main_width * 0.9)
        height = int(main_height * 0.9)
        
        # Posicionar ligeramente desplazada de la ventana principal
        x = root.winfo_x() + 100
        y = root.winfo_y() + 100
        
        self.signals_window.geometry(f"{width}x{height}+{x}+{y}")
        self.signals_window.configure(bg=colors['bg'])
        
        # No hacer la ventana modal pero mantenerla encima
        self.signals_window.transient(root)
        
        # Frame principal
        main_frame = tk.Frame(self.signals_window, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="Vista de Señales",
            font=self.design_manager.get_font('title'),
            bg=colors['bg'],
            fg=colors['fg']
        )
        title_label.pack(pady=(0, 20))
        
        # Contenido placeholder
        content_frame = tk.Frame(main_frame, bg=colors['entry_bg'], relief=tk.SOLID, borderwidth=2)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        placeholder_label = tk.Label(
            content_frame,
            text="Vista de Señales\n\nAquí se mostrarán las señales del CPU en tiempo real",
            font=self.design_manager.get_font('normal'),
            bg=colors['entry_bg'],
            fg=colors['entry_fg']
        )
        placeholder_label.pack(expand=True)
        
        # Protocolo de cierre
        self.signals_window.protocol("WM_DELETE_WINDOW", lambda: self._toggle_signals_window())
    
    def _on_execute_cycle(self):
        """Maneja el evento de ejecutar un ciclo"""
        #Paso 1: Cargar memorias y señales, desde el excel
        
        #Paso 2:Ejecutar SOLO 1 ciclo
        
        #Paso 3:Cargar todas las señales y memorias en excel
        
        #Paso 4:Actualizar diagrama, memorias y señales
        self.diagram.update_signals()
        self.controller.print_console("[CPU] Se ejecutó un ciclo")
    
    def _on_execute_all(self):
        """Maneja el evento de ejecutar todo"""
        
        #Paso 1: Cargar memorias y señales, desde el excel
        
        #Paso 2:Ejecutar hasta que no existan mas instrucciones
        
        #Paso 3:Cargar todas las señales y memorias en excel
        
        #Paso 4:Actualizar diagrama, memorias y señales
        self.diagram.update_signals()
        self.controller.print_console("[CPU] Se ejecutó todo el programa")
    
    def update_theme(self):
        """Actualiza el tema de todos los componentes"""
        # Actualizar el diagrama
        if hasattr(self, 'diagram'):
            self.diagram.update_theme()
        
        # Actualizar ventanas adicionales si están abiertas
        if self.memory_window and self.memory_window.winfo_exists():
            colors = self.design_manager.get_colors()
            self.memory_window.configure(bg=colors['bg'])
            # Actualizar widgets hijos recursivamente
            self._update_window_theme(self.memory_window)
        
        if self.signals_window and self.signals_window.winfo_exists():
            colors = self.design_manager.get_colors()
            self.signals_window.configure(bg=colors['bg'])
            # Actualizar widgets hijos recursivamente
            self._update_window_theme(self.signals_window)
    
    def _update_window_theme(self, window):
        """Actualiza el tema de una ventana y sus hijos recursivamente"""
        colors = self.design_manager.get_colors()
        
        for child in window.winfo_children():
            widget_class = child.winfo_class()
            
            if widget_class == 'Frame':
                child.configure(bg=colors['bg'])
                self._update_window_theme(child)
            elif widget_class == 'Label':
                # Determinar el tipo de label por su fuente
                try:
                    current_font = child.cget('font')
                    if current_font == self.design_manager.get_font('title'):
                        child.configure(bg=colors['bg'], fg=colors['fg'])
                    else:
                        # Labels normales o en frames de contenido
                        if child.master.cget('bg') == colors['entry_bg']:
                            child.configure(bg=colors['entry_bg'], fg=colors['entry_fg'])
                        else:
                            child.configure(bg=colors['bg'], fg=colors['fg'])
                except:
                    child.configure(bg=colors['bg'], fg=colors['fg'])