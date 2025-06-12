# GUI/Views/cpu.py ─ Vista del CPU con diagrama interactivo
import tkinter as tk
from GUI.Components.styled_button      import StyledButton
from GUI.Components.memory_table_view  import MemoryTableView
from GUI.Components.signals_table_view import SignalsTableView

class CPUView:
    # ──────────────────────────────────────────────────────────────────────────
    #  Constructor
    # ──────────────────────────────────────────────────────────────────────────
    def __init__(self, parent, base_dir, config,
                 design_manager, on_config_change,
                 cpu_excel, controller):

        # ── inyección de dependencias ────────────────────────────────────────
        self.parent           = parent
        self.base_dir         = base_dir
        self.config           = config
        self.design_manager   = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel        = cpu_excel
        self.controller       = controller

        # ── ventanas secundarias ─────────────────────────────────────────────
        self.memory_window  : tk.Toplevel | None = None
        self.signals_window : tk.Toplevel | None = None

        # ── referencias a componentes ────────────────────────────────────────
        self.diagram       = None
        self.memory_table  = None
        self.signals_table = None

        # ── caché de lecturas iniciales (opcional) ───────────────────────────
        self.memory_cache  = None
        self.signals_cache = None

        # ── construcción de la UI principal ──────────────────────────────────
        self._create_ui()

    # ═════════════════════════════════════════════════════════════════════════
    #  Construcción de la interfaz
    # ═════════════════════════════════════════════════════════════════════════
    def _create_ui(self):
        colors = self.design_manager.get_colors()

        main_frame           = tk.Frame(self.parent, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_rowconfigure(0, weight=0)   # top
        main_frame.grid_rowconfigure(1, weight=1)   # center
        main_frame.grid_rowconfigure(2, weight=0)   # bottom
        main_frame.grid_columnconfigure(0, weight=1)

        self._create_top_section(main_frame)
        self._create_center_section(main_frame)
        self._create_bottom_section(main_frame)

    # ──────────────────────────────────────────────────────────────────────
    #  Sección superior (botones)
    # ──────────────────────────────────────────────────────────────────────
    def _create_top_section(self, parent):
        colors = self.design_manager.get_colors()

        top_frame = tk.Frame(parent, bg=colors['bg'], height=60)
        top_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=(20, 10))
        top_frame.grid_propagate(False)

        container = tk.Frame(top_frame, bg=colors['bg'])
        container.place(relx=0.5, rely=0.5, anchor='center')

        StyledButton(container, text="Mostrar Memorias",
                     command=self._toggle_memories_window,
                     design_manager=self.design_manager).pack(side=tk.LEFT, padx=10)

        StyledButton(container, text="Mostrar Señales",
                     command=self._toggle_signals_window,
                     design_manager=self.design_manager).pack(side=tk.LEFT, padx=10)

    # ──────────────────────────────────────────────────────────────────────
    #  Sección central (diagrama)
    # ──────────────────────────────────────────────────────────────────────
    def _create_center_section(self, parent):
        colors = self.design_manager.get_colors()

        center_frame = tk.Frame(parent, bg=colors['bg'])
        center_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

        # import local para evitar dependencias circulares
        from GUI.Components.cpu_pipeline_diagram import CPUPipelineDiagram

        self.diagram = CPUPipelineDiagram(center_frame,
                                          self.design_manager,
                                          self.cpu_excel)
        self.diagram.pack(fill=tk.BOTH, expand=True)
        self.diagram.update_signals()           # carga inicial

    # ──────────────────────────────────────────────────────────────────────
    #  Sección inferior (ejecución)
    # ──────────────────────────────────────────────────────────────────────
    def _create_bottom_section(self, parent):
        colors = self.design_manager.get_colors()

        bottom_frame = tk.Frame(parent, bg=colors['bg'], height=60)
        bottom_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(10, 20))
        bottom_frame.grid_propagate(False)

        container = tk.Frame(bottom_frame, bg=colors['bg'])
        container.place(relx=0.5, rely=0.5, anchor='center')

        StyledButton(container, text="Ejecutar Un Ciclo",
                     command=self._on_execute_cycle,
                     design_manager=self.design_manager).pack(side=tk.LEFT, padx=10)

        StyledButton(container, text="Ejecutar Todo",
                     command=self._on_execute_all,
                     design_manager=self.design_manager).pack(side=tk.LEFT, padx=10)

    # ═════════════════════════════════════════════════════════════════════
    #  Caché inicial
    # ═════════════════════════════════════════════════════════════════════
    def _load_initial_values(self):
        self.controller.print_console("[CPU] Cargando valores iniciales…")
        self.memory_cache  = MemoryTableView(tk.Frame(), self.design_manager, self.cpu_excel)
        self.signals_cache = SignalsTableView(tk.Frame(), self.design_manager, self.cpu_excel)
        self.controller.print_console("[CPU] Valores iniciales cargados en caché")

    # ═════════════════════════════════════════════════════════════════════
    #  Ventana de Memorias (creación / toggle)
    # ═════════════════════════════════════════════════════════════════════
    def _toggle_memories_window(self):
        if self.memory_window and self.memory_window.winfo_exists():
            # alternar visibilidad sin destruir
            if self.memory_window.state() == "withdrawn":
                self.memory_window.deiconify()
            else:
                self.memory_window.withdraw()
        else:
            self._create_memory_window()

    def _create_memory_window(self):
        colors = self.design_manager.get_colors()
        root   = self.parent.winfo_toplevel()

        self.memory_window = tk.Toplevel(root)
        self.memory_window.title("Vista de Memorias")

        # 90 % del tamaño de la ventana principal
        width  = int(root.winfo_width()  * 0.9)
        height = int(root.winfo_height() * 0.9)
        x = root.winfo_x() + 50
        y = root.winfo_y() + 50
        self.memory_window.geometry(f"{width}x{height}+{x}+{y}")
        self.memory_window.configure(bg=colors['bg'])
        self.memory_window.transient(root)

        main = tk.Frame(self.memory_window, bg=colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main, text="Vista de Memorias del CPU",
                 font=self.design_manager.get_font('title'),
                 bg=colors['bg'], fg=colors['fg']).pack(pady=(0, 20))

        self.memory_table = MemoryTableView(main, self.design_manager, self.cpu_excel)
        self.memory_table.pack(fill=tk.BOTH, expand=True)

        # si el usuario cierra la ventana ► ocultar, no destruir
        self.memory_window.protocol("WM_DELETE_WINDOW",
                                    self.memory_window.withdraw)

    # ═════════════════════════════════════════════════════════════════════
    #  Ventana de Señales (creación / toggle)
    # ═════════════════════════════════════════════════════════════════════
    def _toggle_signals_window(self):
        if self.signals_window and self.signals_window.winfo_exists():
            if self.signals_window.state() == "withdrawn":
                self.signals_window.deiconify()
            else:
                self.signals_window.withdraw()
        else:
            self._create_signals_window()

    def _create_signals_window(self):
        colors = self.design_manager.get_colors()
        root   = self.parent.winfo_toplevel()

        self.signals_window = tk.Toplevel(root)
        self.signals_window.title("Vista de Señales")

        width  = int(root.winfo_width()  * 0.9)
        height = int(root.winfo_height() * 0.9)
        x = root.winfo_x() + 100
        y = root.winfo_y() + 100
        self.signals_window.geometry(f"{width}x{height}+{x}+{y}")
        self.signals_window.configure(bg=colors['bg'])
        self.signals_window.transient(root)

        main = tk.Frame(self.signals_window, bg=colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main, text="Vista de Señales del Pipeline",
                 font=self.design_manager.get_font('title'),
                 bg=colors['bg'], fg=colors['fg']).pack(pady=(0, 20))

        self.signals_table = SignalsTableView(main, self.design_manager, self.cpu_excel)
        self.signals_table.pack(fill=tk.BOTH, expand=True)

        self.signals_window.protocol("WM_DELETE_WINDOW",
                                     self.signals_window.withdraw)

    # ═════════════════════════════════════════════════════════════════════
    #  Actualización de vistas y temas
    # ═════════════════════════════════════════════════════════════════════
    def _update_all_views(self):
        if self.diagram:
            self.diagram.update_signals()
        if self.memory_table and self.memory_window.state() != "withdrawn":
            self.memory_table.update_all_memories()
        if self.signals_table and self.signals_window.state() != "withdrawn":
            self.signals_table.update_all_signals()

    def update_theme(self):
        if self.diagram:
            self.diagram.update_theme()

        for win in (self.memory_window, self.signals_window):
            if win and win.winfo_exists():
                colors = self.design_manager.get_colors()
                win.configure(bg=colors['bg'])
                self._update_window_theme(win)

    def _update_window_theme(self, window):
        colors = self.design_manager.get_colors()
        for child in window.winfo_children():
            w_class = child.winfo_class()
            if w_class == 'Frame':
                child.configure(bg=colors['bg'])
                self._update_window_theme(child)
            elif w_class == 'Label':
                try:
                    if child.cget('font') == self.design_manager.get_font('title'):
                        child.configure(bg=colors['bg'], fg=colors['fg'])
                    else:
                        bg = colors['entry_bg'] if child.master.cget('bg') == colors['entry_bg'] else colors['bg']
                        fg = colors['entry_fg'] if bg == colors['entry_bg'] else colors['fg']
                        child.configure(bg=bg, fg=fg)
                except:
                    child.configure(bg=colors['bg'], fg=colors['fg'])
    
    def _on_execute_cycle(self):
        """Maneja el evento de ejecutar un ciclo"""
        #Paso 1: Cargar memorias y señales, desde el excel
        
        #Paso 2:Ejecutar SOLO 1 ciclo
        
        #Paso 3:Cargar todas las señales y memorias en excel
        
        #Paso 4:Actualizar diagrama, memorias y señales
        self.diagram.update_signals()
        self._load_initial_values()
        self.controller.print_console("[CPU] Se ejecutó un ciclo")
    
    def _on_execute_all(self):
        """Maneja el evento de ejecutar todo"""
        
        #Paso 1: Cargar memorias y señales, desde el excel
        
        #Paso 2:Ejecutar hasta que no existan mas instrucciones
        
        #Paso 3:Cargar todas las señales y memorias en excel
        
        #Paso 4:Actualizar diagrama, memorias y señales
        self.diagram.update_signals()
        self._load_initial_values()
        self.controller.print_console("[CPU] Se ejecutó todo el programa")