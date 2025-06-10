# GUI/Views/analisis.py
"""
analisis.py - Vista de análisis con rutas críticas, cálculo de frecuencia y comparación de rendimiento
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_scrollbar import ScrollableFrame
from GUI.Components.styled_widgets import StyledLabel
from GUI.Components.styled_textbox import StyledTextBox
from GUI.Components.styled_graph import StyledGraph

class AnalisisView:
    def __init__(self, parent, base_dir, config, design_manager, on_config_change, cpu_excel):
        self.parent = parent
        self.base_dir = base_dir
        self.config = config
        self.design_manager = design_manager
        self.on_config_change = on_config_change
        self.cpu_excel = cpu_excel
        
        # Datos de tiempo para la gráfica
        self.timing_data = {
            'Python': {
                'Encriptación': 2.127,
                'Desencriptación': 11.106
            },
            'CPU': {
                'Encriptación': 25.458,
                'Desencriptación': 54.458
            }
        }
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario de la vista"""
        # Frame principal con scroll
        root_frame = self.design_manager.create_styled_frame(self.parent)
        root_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        title_label = StyledLabel(
            root_frame,
            "ANÁLISIS DE EFICIENCIA DEL DISEÑO",
            self.design_manager,
            font_type='title'
        )
        title_label.pack(pady=(20, 15))
        
        # Frame scrollable para el contenido
        scroll = ScrollableFrame(root_frame, self.design_manager)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Crear las tres secciones principales
        self._create_critical_paths_section(scroll.interior)
        self._create_frequency_calculation_section(scroll.interior)
        self._create_performance_comparison_section(scroll.interior)
    
    def _create_critical_paths_section(self, parent):
        """Sección 1: Rutas críticas y tiempos de sincronización"""
        # Frame de la sección
        section_frame = ttk.LabelFrame(
            parent, 
            text="1. RUTAS CRÍTICAS Y TIEMPOS DE SINCRONIZACIÓN",
            padding=15
        )
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Teoría de parámetros de tiempo
        theory_box = StyledTextBox(
            section_frame,
            self.design_manager,
            title="Parámetros de Tiempo en Lógica Secuencial"
        )
        theory_box.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Contenido formateado
        content = [
            ("PARÁMETROS FUNDAMENTALES\n\n", "subtitle"),
            ("• Contaminación Clock→Q (t", None),
            ("ccq", "code"),
            ("): ", None),
            ("20 ps", "emphasis"),
            ("\n  Tiempo MÍNIMO desde el flanco de reloj hasta la salida Q\n\n", None),
            
            ("• Propagación Clock→Q (t", None),
            ("pcq", "code"),
            ("): ", None),
            ("60 ps", "emphasis"),
            ("\n  Tiempo MÁXIMO desde el flanco hasta Q estable\n\n", None),
            
            ("• Setup Time (t", None),
            ("setup", "code"),
            ("): ", None),
            ("80 ps", "emphasis"),
            ("\n  Tiempo previo al flanco donde D debe estar estable\n\n", None),
            
            ("• Hold Time (t", None),
            ("hold", "code"),
            ("): ", None),
            ("20 ps", "emphasis"),
            ("\n  Tiempo posterior al flanco donde D debe permanecer estable\n\n", None),
            
            ("ECUACIÓN DEL PERÍODO MÍNIMO:\n", "subtitle"),
            ("T_C ≥ t_pcq + t_pd + t_setup", "equation"),
            ("\n\n", None),
            
            ("ANÁLISIS DE RUTAS CRÍTICAS (Tecnología 28nm)\n\n", "subtitle"),
        ]
        theory_box.insert_formatted_content(content)
        
        # Tabla de rutas críticas
        self._create_critical_paths_table(section_frame)
    
    def _create_critical_paths_table(self, parent):
        """Crea la tabla de análisis de rutas críticas"""
        # Frame para la tabla
        table_frame = tk.Frame(parent, bg=self.design_manager.get_colors()['bg'])
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Configurar grid
        for i in range(6):
            table_frame.grid_columnconfigure(i, weight=1)
        
        # Headers
        headers = ["Etapa", "t_pcq", "t_pd", "t_setup", "Total", "f_max"]
        colors = self.design_manager.get_colors()
        
        for i, header in enumerate(headers):
            label = tk.Label(
                table_frame,
                text=header,
                font=self.design_manager.get_font('bold'),
                bg=colors['sidebar_bg'],
                fg=colors['sidebar_button_fg'],
                padx=10,
                pady=8,
                relief=tk.RIDGE,
                borderwidth=1
            )
            label.grid(row=0, column=i, sticky='ew')
        
        # Datos de las rutas
        routes_data = [
            ("IF→ID", "60 ps", "240 ps", "80 ps", "440 ps", "2.27 GHz"),
            ("ID→EX", "60 ps", "200 ps", "80 ps", "340 ps", "2.94 GHz"),
            ("EX→MEM", "60 ps", "500 ps", "80 ps", "640 ps", "1.56 GHz")
        ]
        
        # Filas de datos
        for row_idx, (stage, tpcq, tpd, tsetup, total, fmax) in enumerate(routes_data, 1):
            # Resaltar ruta crítica
            is_critical = row_idx == 3
            bg_color = colors['select_bg'] if is_critical else colors['entry_bg']
            fg_color = colors['select_fg'] if is_critical else colors['entry_fg']
            
            data = [stage, tpcq, tpd, tsetup, total, fmax]
            for col_idx, value in enumerate(data):
                label = tk.Label(
                    table_frame,
                    text=value,
                    font=self.design_manager.get_font('bold' if is_critical else 'normal'),
                    bg=bg_color,
                    fg=fg_color,
                    padx=10,
                    pady=6,
                    relief=tk.RIDGE,
                    borderwidth=1
                )
                label.grid(row=row_idx, column=col_idx, sticky='ew')
        
        # Nota sobre la ruta crítica
        note_frame = tk.Frame(parent, bg=colors['bg'])
        note_frame.pack(fill=tk.X, pady=(10, 0))
        
        note_label = StyledLabel(
            note_frame,
            "⚠️ RUTA CRÍTICA: EX→MEM con 640 ps determina la frecuencia máxima del sistema",
            self.design_manager,
            font_type='bold'
        )
        note_label.pack(anchor='w')
    
    def _create_frequency_calculation_section(self, parent):
        """Sección 2: Cálculo de frecuencia de reloj"""
        # Frame de la sección
        section_frame = ttk.LabelFrame(
            parent,
            text="2. CÁLCULO Y DETERMINACIÓN DE FRECUENCIA DE RELOJ",
            padding=15
        )
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Caja de cálculos
        calc_box = StyledTextBox(
            section_frame,
            self.design_manager,
            title="Análisis de Frecuencia y Slack"
        )
        calc_box.pack(fill=tk.BOTH, expand=True)
        
        # Contenido de cálculos
        content = [
            ("CÁLCULO DE FRECUENCIA MÁXIMA\n\n", "subtitle"),
            ("Basado en la ruta crítica EX→MEM:\n", None),
            ("• T_período = 640 ps\n", None),
            ("• f_max = 1 / T_período\n", None),
            ("• f_max = 1 / 640×10⁻¹² s\n", None),
            ("• ", None),
            ("f_max = 1.56 GHz", "emphasis"),
            ("\n\n", None),
            
            ("ANÁLISIS DE SLACK @ 1.2 GHz\n\n", "subtitle"),
            ("Período objetivo: T = 833 ps\n\n", None),
            
            ("• Slack IF→ID: ", None),
            ("833 - 440 = ", "code"),
            ("393 ps", "emphasis"),
            (" (Amplio margen)\n", None),
            
            ("• Slack ID→EX: ", None),
            ("833 - 340 = ", "code"),
            ("493 ps", "emphasis"),
            (" (Muy holgado)\n", None),
            
            ("• Slack EX→MEM: ", None),
            ("833 - 640 = ", "code"),
            ("193 ps", "emphasis"),
            (" (Margen ajustado)\n\n", None),
            
            ("VERIFICACIÓN DE HOLD\n\n", "subtitle"),
            ("Restricción: t_cd ≥ t_hold - t_ccq\n", None),
            ("• t_cd,min = 100 ps\n", None),
            ("• t_hold - t_ccq = 20 - 20 = 0 ps\n", None),
            ("• 100 ps ≥ 0 ps ✓ ", None),
            ("No hay violación de hold", "emphasis"),
            ("\n\n", None),
            
            ("RECOMENDACIONES DE OPTIMIZACIÓN\n\n", "subtitle"),
            ("1. ", None),
            ("Pipeline adicional", "emphasis"),
            (": Dividir etapa EX→MEM para alcanzar >2 GHz\n", None),
            ("2. ", None),
            ("Memoria más rápida", "emphasis"),
            (": Reducir t_pd,Mem de 300ps\n", None),
            ("3. ", None),
            ("Celdas optimizadas", "emphasis"),
            (": Usar flip-flops con menor t_pcq en ruta crítica\n", None),
        ]
        calc_box.insert_formatted_content(content)
    
    def _create_performance_comparison_section(self, parent):
        """Sección 3: Comparación de rendimiento Python vs CPU"""
        # Frame de la sección
        section_frame = ttk.LabelFrame(
            parent,
            text="3. COMPARACIÓN DE RENDIMIENTO: PYTHON vs CPU",
            padding=15
        )
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Nota sobre la comparación
        note_box = StyledTextBox(
            section_frame,
            self.design_manager,
            title="Contexto de la Comparación"
        )
        note_box.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        note_content = [
            ("IMPORTANTE: ", "emphasis"),
            ("Los tiempos mostrados reflejan la perspectiva de SIMULACIÓN\n\n", None),
            
            ("• ", None),
            ("Python", "emphasis"),
            (": Ejecución nativa optimizada del algoritmo TEA\n", None),
            
            ("• ", None),
            ("CPU", "emphasis"),
            (": Simulación ciclo a ciclo de la microarquitectura pipeline\n\n", None),
            
            ("La diferencia es esperada debido a:\n", None),
            ("  - Overhead de simulación de cada instrucción\n", None),
            ("  - Emulación de pipeline y unidades funcionales\n", None),
            ("  - Verificación de cada acceso a memoria\n", None),
            ("  - Tracking completo del estado del procesador\n", None),
        ]
        note_box.insert_formatted_content(note_content)
        
        # Gráfica de comparación
        self.graph = StyledGraph(
            section_frame,
            self.design_manager,
            title="Tiempos de Ejecución: Encriptación y Desencriptación TEA"
        )
        self.graph.pack(fill=tk.BOTH, expand=True)
        
        # Plotear los datos
        self._plot_comparison_data()
        
        # Tabla resumen
        self._create_summary_table(section_frame)
    
    def _plot_comparison_data(self):
        """Plotea los datos de comparación en la gráfica"""
        # Crear gráfica de líneas para mejor visualización
        line_data = {
            'Python': [
                (1, self.timing_data['Python']['Encriptación']),
                (2, self.timing_data['Python']['Desencriptación'])
            ],
            'CPU (Simulación)': [
                (1, self.timing_data['CPU']['Encriptación']),
                (2, self.timing_data['CPU']['Desencriptación'])
            ]
        }
        
        self.graph.plot_lines(
            line_data,
            title="Comparación de Tiempos de Ejecución",
            xlabel="Operación (1: Encriptación, 2: Desencriptación)",
            ylabel="Tiempo (segundos)"
        )
    
    def _create_summary_table(self, parent):
        """Crea tabla resumen de tiempos"""
        # Frame para la tabla
        table_frame = tk.Frame(parent, bg=self.design_manager.get_colors()['bg'])
        table_frame.pack(fill=tk.X, pady=(15, 0))
        
        colors = self.design_manager.get_colors()
        
        # Título de la tabla
        title = StyledLabel(
            table_frame,
            "TABLA RESUMEN DE TIEMPOS",
            self.design_manager,
            font_type='bold'
        )
        title.pack(pady=(0, 10))
        
        # Frame para la tabla real
        data_frame = tk.Frame(table_frame, bg=colors['bg'])
        data_frame.pack()
        
        # Configurar grid
        for i in range(4):
            data_frame.grid_columnconfigure(i, weight=1)
        
        # Headers
        headers = ["Implementación", "Encriptación", "Desencriptación", "Factor"]
        for i, header in enumerate(headers):
            label = tk.Label(
                data_frame,
                text=header,
                font=self.design_manager.get_font('bold'),
                bg=colors['sidebar_bg'],
                fg=colors['sidebar_button_fg'],
                padx=20,
                pady=8,
                relief=tk.RIDGE,
                borderwidth=1
            )
            label.grid(row=0, column=i, sticky='ew')
        
        # Datos
        rows_data = [
            ("Python", "2.127 seg", "11.106 seg", "1x"),
            ("CPU (Simulación)", "25.458 seg", "54.458 seg", "~5x-12x más lento"),
        ]
        
        for row_idx, (impl, enc, dec, factor) in enumerate(rows_data, 1):
            data = [impl, enc, dec, factor]
            for col_idx, value in enumerate(data):
                # Resaltar el factor
                font_type = 'bold' if col_idx == 3 else 'normal'
                fg_color = colors['sidebar_button_active_bg'] if col_idx == 3 else colors['entry_fg']
                
                label = tk.Label(
                    data_frame,
                    text=value,
                    font=self.design_manager.get_font(font_type),
                    bg=colors['entry_bg'],
                    fg=fg_color,
                    padx=20,
                    pady=6,
                    relief=tk.RIDGE,
                    borderwidth=1
                )
                label.grid(row=row_idx, column=col_idx, sticky='ew')
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        # La mayoría de componentes se actualizan automáticamente
        # Solo necesitamos actualizar la gráfica
        if hasattr(self, 'graph'):
            self.graph.update_theme()
            self._plot_comparison_data()