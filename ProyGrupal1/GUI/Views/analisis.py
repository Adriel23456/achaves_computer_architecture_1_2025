"""
analisis.py - Vista de análisis con rutas críticas, cálculo de frecuencia
              y comparación de rendimiento.
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_scrollbar import ScrollableFrame
from GUI.Components.styled_widgets   import StyledLabel
from GUI.Components.styled_textbox   import StyledTextBox
from GUI.Components.styled_graph     import StyledGraph


class AnalisisView:
    # ──────────────────────────────────────────────────────────────
    #  Métricas base de la última ejecución
    # ──────────────────────────────────────────────────────────────
    CPU_CYCLES   = 3_280_748                     # ciclos simulados
    CPU_TIME_S   = 236.489                       # s   (≈ 13 873 ciclos/s)
    PY_TIME_S    = 0.040                         # s   en Python nativo

    def __init__(
        self, parent, base_dir, config,
        design_manager, on_config_change,
        cpu_excel, controller
    ):
        self.parent           = parent
        self.base_dir         = base_dir
        self.config           = config
        self.design_manager   = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel        = cpu_excel
        self.controller       = controller

        # Para la gráfica (time vs cycles)
        self.timing_pts = {
            "Python"         : [(0, 0.0), (self.CPU_CYCLES, self.PY_TIME_S)],
            "CPU (Simulación)": [(0, 0.0), (self.CPU_CYCLES, self.CPU_TIME_S)],
        }

        self._create_ui()

    # ════════════════════════════════════════════════════════════════
    #  Construcción de la interfaz
    # ════════════════════════════════════════════════════════════════
    def _create_ui(self):
        root = self.design_manager.create_styled_frame(self.parent)
        root.pack(fill=tk.BOTH, expand=True)

        StyledLabel(
            root,
            "ANÁLISIS DE EFICIENCIA DEL DISEÑO",
            self.design_manager,
            font_type="title"
        ).pack(pady=(20, 15))

        scroll = ScrollableFrame(root, self.design_manager)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self._create_critical_paths_section(scroll.interior)
        self._create_frequency_calculation_section(scroll.interior)
        self._create_performance_comparison_section(scroll.interior)

    # ──────────────────────────────────────────────────────────────
    #  1. Rutas críticas
    # ──────────────────────────────────────────────────────────────
    def _create_critical_paths_section(self, parent):
        section = ttk.LabelFrame(
            parent,
            text="1. RUTAS CRÍTICAS Y TIEMPOS DE SINCRONIZACIÓN (Pipeline 5-etapas)",
            padding=15
        )
        section.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        theory = StyledTextBox(section, self.design_manager,
                               title="Parámetros de Tiempo en Lógica Secuencial")
        theory.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        content = [
            ("PIPELINE COMPLETO (5 ETAPAS)\n", "subtitle"),
            ("• IF  – Instruction Fetch\n", None),
            ("• ID  – Instruction Decode & Register Read\n", None),
            ("• EX  – Execute / ALU\n", None),
            ("• MEM – Memory Access\n", None),
            ("• WB  – Write-Back\n\n", None),

            ("PARÁMETROS FUNDAMENTALES\n\n", "subtitle"),
            ("• t", None), ("ccq", "code"), (": 20 ps   ", "emphasis"),
            ("(Clock→Q min)\n", None),
            ("• t", None), ("pcq", "code"), (": 60 ps   ", "emphasis"),
            ("(Clock→Q max)\n", None),
            ("• t", None), ("setup", "code"), (": 80 ps   ", "emphasis"),
            ("(Setup)\n", None),
            ("• t", None), ("hold", "code"), (": 20 ps   ", "emphasis"),
            ("(Hold)\n\n", None),

            ("ECUACIÓN DEL PERÍODO MÍNIMO:\n", "subtitle"),
            ("T ≥ t_pcq + t_pd + t_setup\n\n", "equation"),

            ("ANÁLISIS DE RUTAS CRÍTICAS (28 nm)\n\n", "subtitle"),
        ]
        theory.insert_formatted_content(content)

        self._create_critical_paths_table(section)

    def _create_critical_paths_table(self, parent):
        colors = self.design_manager.get_colors()
        tbl    = tk.Frame(parent, bg=colors["bg"])
        tbl.pack(fill=tk.BOTH, expand=True, pady=10)

        for c in range(6):
            tbl.grid_columnconfigure(c, weight=1)

        headers = ("Etapa", "t_pcq", "t_pd", "t_setup", "Total", "ƒ_max")
        for c, h in enumerate(headers):
            tk.Label(
                tbl, text=h,
                font=self.design_manager.get_font("bold"),
                bg=colors["sidebar_bg"], fg=colors["sidebar_button_fg"],
                padx=10, pady=8, relief=tk.RIDGE, borderwidth=1
            ).grid(row=0, column=c, sticky="ew")

        rows = [
            ("PC→IF",   "60 ps", " 40 ps", "80 ps", "180 ps", "5.55 GHz"),
            ("IF→ID",   "60 ps", "240 ps", "80 ps", "380 ps", "2.63 GHz"),
            ("ID→EX",   "60 ps", "200 ps", "80 ps", "340 ps", "2.94 GHz"),
            ("EX→MEM",  "60 ps", "720 ps", "80 ps", "860 ps", "1.16 GHz"),  # crítica
            ("MEM→WB",  "60 ps", "120 ps", "80 ps", "260 ps", "3.85 GHz"),
        ]

        for r, row in enumerate(rows, 1):
            critical = (row[0] == "EX→MEM")
            bg       = colors["select_bg"] if critical else colors["entry_bg"]
            fg       = colors["select_fg"] if critical else colors["entry_fg"]
            fnt      = self.design_manager.get_font("bold" if critical else "normal")
            for c, val in enumerate(row):
                tk.Label(tbl, text=val, font=fnt,
                         bg=bg, fg=fg, padx=10, pady=6,
                         relief=tk.RIDGE, borderwidth=1
                         ).grid(row=r, column=c, sticky="ew")

        StyledLabel(
            parent,
            "⚠️  RUTA CRÍTICA: EX→MEM (acceso a memoria)  →  ƒₘₐₓ ≈ 1.16 GHz",
            self.design_manager, font_type="bold"
        ).pack(anchor="w", pady=(10, 0))

    # ──────────────────────────────────────────────────────────────
    #  2. Frecuencia
    # ──────────────────────────────────────────────────────────────
    def _create_frequency_calculation_section(self, parent):
        section = ttk.LabelFrame(
            parent,
            text="2. CÁLCULO Y DETERMINACIÓN DE FRECUENCIA DE RELOJ",
            padding=15
        )
        section.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        calc = StyledTextBox(section, self.design_manager,
                             title="Análisis de Frecuencia y Slack")
        calc.pack(fill=tk.BOTH, expand=True)

        content = [
            ("CÁLCULO DE ƒₘₐₓ\n\n", "subtitle"),
            ("Ruta crítica EX→MEM:\n", None),
            ("T = 860 ps  ⇒  ƒₘₐₓ = 1/860 ps ≈ ", None),
            ("1.16 GHz\n\n", "emphasis"),

            ("SLACK A 1 GHz (T = 1 ns)\n\n", "subtitle"),
            ("Slack EX→MEM = 1 000 ps − 860 ps = ", None),
            ("140 ps\n\n", "emphasis"),

            ("VERIFICACIÓN HOLD\n\n", "subtitle"),
            ("t_hold − t_ccq = 0 ps  ≤  t_cd,min (100 ps)  ✓\n\n", None),

            ("RECOMENDACIONES\n\n", "subtitle"),
            ("• Dividir MEM en 2 micro-etapas o usar caché rápida\n", None),
            ("• Flip-flops de bajo t_pcq en la ruta crítica\n", None),
        ]
        calc.insert_formatted_content(content)

    # ──────────────────────────────────────────────────────────────
    #  3. Comparación rendimiento
    # ──────────────────────────────────────────────────────────────
    def _create_performance_comparison_section(self, parent):
        section = ttk.LabelFrame(
            parent,
            text="3. COMPARACIÓN DE RENDIMIENTO: PYTHON vs CPU (Simulación)",
            padding=15
        )
        section.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        note = StyledTextBox(section, self.design_manager, title="Contexto de la Comparación")
        note.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        note_content = [
            ("Métrica global para 1 423 bloques de 64 bit TEA\n\n", "subtitle"),
            ("• CPU (Simulación): 3 280 748 ciclos  →  236.489 s  (", None),
            ("13 873 ciclos / s", "emphasis"), (")\n", None),
            ("• Python nativo   : 3 280 748 ‘ciclos lógicos’ → 0.040 s\n\n", None),
            ("La simulación es miles de veces más lenta por la emulación\n"
             "ciclo-a-ciclo del pipeline, controles de seguridad y trazado\n"
             "completo del estado interno.\n", None),
        ]
        note.insert_formatted_content(note_content)

        # Gráfica tiempo-vs-ciclos
        self.graph = StyledGraph(
            section,
            self.design_manager,
            title="Tiempo de ejecución vs. Ciclos (0 → 3 280 748)"
        )
        self.graph.pack(fill=tk.BOTH, expand=True)
        self._plot_comparison_data()

        self._create_summary_table(section)

    # ──────────────────────────────────────────────────────────────
    #  Gráfica
    # ──────────────────────────────────────────────────────────────
    def _plot_comparison_data(self):
        self.graph.plot_lines(
            self.timing_pts,
            title="Comparación global (misma cantidad de ciclos)",
            xlabel="Ciclos de reloj",
            ylabel="Tiempo (segundos)"
        )

    # ──────────────────────────────────────────────────────────────
    #  Tabla resumen
    # ──────────────────────────────────────────────────────────────
    def _create_summary_table(self, parent):
        colors = self.design_manager.get_colors()
        frame  = tk.Frame(parent, bg=colors["bg"])
        frame.pack(fill=tk.X, pady=(15, 0))

        StyledLabel(
            frame, "TABLA RESUMEN DE TIEMPOS",
            self.design_manager, font_type="bold"
        ).pack(pady=(0, 10))

        table = tk.Frame(frame, bg=colors["bg"])
        table.pack()

        for c in range(4):
            table.grid_columnconfigure(c, weight=1)

        headers = ("Implementación", "Tiempo total", "Ciclos equivalentes", "Factor")
        for c, h in enumerate(headers):
            tk.Label(
                table, text=h,
                font=self.design_manager.get_font("bold"),
                bg=colors["sidebar_bg"], fg=colors["sidebar_button_fg"],
                padx=20, pady=8, relief=tk.RIDGE, borderwidth=1
            ).grid(row=0, column=c, sticky="ew")

        rows = [
            ("Python nativo",
             f"{self.PY_TIME_S:.3f} s",
             f"{self.CPU_CYCLES:,}",
             "1 ×"),
            ("CPU (Simulación)",
             f"{self.CPU_TIME_S:.3f} s",
             f"{self.CPU_CYCLES:,}",
             "≈ 5 900 ×"),
        ]

        for r, row in enumerate(rows, 1):
            for c, val in enumerate(row):
                tk.Label(
                    table, text=val,
                    font=self.design_manager.get_font("bold" if c == 3 else "normal"),
                    bg=colors["entry_bg"],
                    fg=colors["sidebar_button_active_bg"] if c == 3 else colors["entry_fg"],
                    padx=20, pady=6, relief=tk.RIDGE, borderwidth=1
                ).grid(row=r, column=c, sticky="ew")

    # ──────────────────────────────────────────────────────────────
    #  Cambio de tema
    # ──────────────────────────────────────────────────────────────
    def update_theme(self):
        if hasattr(self, "graph"):
            self.graph.update_theme()
            self._plot_comparison_data()