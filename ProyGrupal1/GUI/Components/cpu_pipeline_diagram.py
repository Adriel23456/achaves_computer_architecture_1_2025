"""
cpu_pipeline_diagram.py - Componente del diagrama del pipeline del CPU
"""
import tkinter as tk
import math

class InteractiveDiagram(tk.Frame):
    """Componente base de diagrama interactivo con zoom y pan"""
    def __init__(self, parent, design_manager):
        self.design_manager = design_manager
        colors = design_manager.get_colors()
        
        super().__init__(parent, bg=colors['bg'], relief=tk.SOLID, borderwidth=2)
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        self.configure(highlightthickness=1)
        
        # Variables de estado
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.is_panning = False
        self.last_x = 0
        self.last_y = 0
        
        # Almacenar elementos del diagrama
        self.elements = []
        
        # Canvas principal
        self.canvas = tk.Canvas(
            self,
            bg=colors['entry_bg'],
            highlightthickness=0,
            width=2400,
            height=900
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Configurar eventos
        self._setup_events()
        
        # Dibujar elementos iniciales
        self._draw_grid()
    
    def _setup_events(self):
        """Configura los eventos del canvas"""
        # Zoom con scroll del mouse
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<Button-4>', self._on_mousewheel)
        self.canvas.bind('<Button-5>', self._on_mousewheel)
        
        # Pan con drag del mouse
        self.canvas.bind('<ButtonPress-1>', self._on_button_press)
        self.canvas.bind('<B1-Motion>', self._on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_button_release)
        
        # Redimensionar
        self.canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _draw_grid(self):
        """Dibuja una grilla de fondo"""
        colors = self.design_manager.get_colors()
        
        # Eliminar grilla anterior
        self.canvas.delete('grid')
        
        # Obtener dimensiones del canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Tamaño de la grilla
        grid_size = 50 * self.zoom_level
        
        # Color de la grilla según el tema
        grid_color = colors['button_bg']
        
        # Calcular offset con pan
        offset_x = (self.pan_x % grid_size)
        offset_y = (self.pan_y % grid_size)
        
        # Dibujar líneas verticales
        for x in range(int(offset_x), width, int(grid_size)):
            self.canvas.create_line(
                x, 0, x, height,
                fill=grid_color,
                tags='grid'
            )
        
        # Dibujar líneas horizontales
        for y in range(int(offset_y), height, int(grid_size)):
            self.canvas.create_line(
                0, y, width, y,
                fill=grid_color,
                tags='grid'
            )
        
        # Asegurar que la grilla esté al fondo
        self.canvas.tag_lower('grid')
    
    def _on_mousewheel(self, event):
        """Maneja el zoom con la rueda del mouse"""
        # Obtener posición del mouse
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # Calcular factor de zoom
        if event.delta > 0 or event.num == 4:
            scale_factor = 1.1
        else:
            scale_factor = 0.9
        
        # Limitar el zoom
        new_zoom = self.zoom_level * scale_factor
        if 0.1 <= new_zoom <= 5.0:
            # Actualizar zoom
            self.zoom_level = new_zoom
            
            # Escalar todos los elementos
            self.canvas.scale('all', x, y, scale_factor, scale_factor)
            
            # Actualizar pan para mantener el punto bajo el mouse
            self.pan_x = x - (x - self.pan_x) * scale_factor
            self.pan_y = y - (y - self.pan_y) * scale_factor
            
            # Redibujar grilla
            self._draw_grid()
    
    def _on_button_press(self, event):
        """Inicia el pan"""
        self.is_panning = True
        self.last_x = event.x
        self.last_y = event.y
        self.canvas.configure(cursor='fleur')
    
    def _on_mouse_drag(self, event):
        """Realiza el pan del canvas"""
        if self.is_panning:
            # Calcular desplazamiento
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            
            # Mover todos los elementos
            self.canvas.move('all', dx, dy)
            
            # Actualizar pan
            self.pan_x += dx
            self.pan_y += dy
            
            # Actualizar última posición
            self.last_x = event.x
            self.last_y = event.y
            
            # Redibujar grilla
            self._draw_grid()
    
    def _on_button_release(self, event):
        """Termina el pan"""
        self.is_panning = False
        self.canvas.configure(cursor='')
    
    def _on_canvas_configure(self, event):
        """Maneja el redimensionamiento del canvas"""
        self._draw_grid()
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        
        # Actualizar frame
        self.configure(bg=colors['bg'])
        self.configure(highlightbackground=colors['button_bg'])
        self.configure(highlightcolor=colors['select_bg'])
        
        # Actualizar canvas
        self.canvas.configure(bg=colors['entry_bg'])
        
        # Redibujar grilla
        self._draw_grid()


class CPUPipelineDiagram(InteractiveDiagram):
    """Diagrama específico del pipeline del CPU"""
    def __init__(self, parent, design_manager, cpu_excel):
        super().__init__(parent, design_manager)
        self.cpu_excel = cpu_excel
        
        # Diccionario para almacenar las señales
        self.signals = {
            # Fetch
            'ALUOutW_c': '0x0',
            'PCPlus8F': '0x0',
            "PC'": '0x0',
            'PCF': '0x0',
            'InstrF': '0x0',
            
            # Decode
            'InstrD': '0x0',
            '47:44': '0x0',
            '43:40': '0x0',
            '39:8': '0x0',
            'SrcAD': '0x0',
            'Rd_SpecialD': '0x0',
            'SrcBD': '0x0',
            
            # Execute
            'SrcAE': '0x0',
            'SrcBE': '0x0',
            'ALUResultE': '0x0',
            
            # Memory
            'ALUOutM': '0x0',
            'RD_G_a': '0x0',
            'ALUOutM_O': '0x0'
        }
        
        # Instrucciones actuales por etapa
        self.instructions = {
            'Fetch': 'ADD R1, R1, R2',
            'Decode': 'ADD R2, R2, R3',
            'Execute': 'ADD R3, R2, R3',
            'Memory': 'ADD R3, R3, R4',
            'WriteBack': 'ADD R5, R5, R4'
        }
        
        # Referencias a elementos del diagrama
        self.signal_labels = {}
        self.instruction_labels = {}
        
        # Dibujar el pipeline completo
        self._draw_pipeline()
    
    def _draw_pipeline(self):
        """Dibuja el pipeline completo con sus 5 etapas"""
        # Posición inicial y espaciado entre etapas
        x_start = 100
        y_center = 350
        stage_width = 385  # Aumentado para dar 85px de espacio entre etapas
        
        # Dibujar cada etapa
        self._draw_fetch_stage(x_start - 250, y_center)
        self._draw_decode_stage(x_start - 55 + stage_width, y_center)
        self._draw_execute_stage((x_start + stage_width * 2)-25, y_center)
        self._draw_memory_stage((x_start + stage_width * 3)-75, y_center)
        self._draw_writeback_stage(x_start + stage_width * 4, y_center)
        
        # Dibujar separadores verticales entre etapas
        colors = self.design_manager.get_colors()
        for i in range(1, 5):
            x = x_start + stage_width * i - 85  # 85px de separación como se solicitó
            self._add_line(x, 100, x, 700, color=colors['button_hover'], width=4, dash=(8, 4))
    
    def _draw_fetch_stage(self, x_base, y_center):
        """Dibuja la etapa Fetch"""
        colors = self.design_manager.get_colors()
        
        # Título de la etapa
        self._add_text(x_base + 150, 90, "FETCH", font_size=16, bold=True, color=colors['select_bg'])
        
        # Mux 1
        mux1_x = x_base + 30
        mux1_y = y_center - 42
        self._draw_mux(mux1_x, mux1_y, "1", width=45, height=85)
        
        # Señal ALUOutW_c (flecha celeste) - conectada a entrada "1"
        arrow_x = mux1_x - 80
        arrow_y = mux1_y + 21  # Entrada "1" del mux
        self._add_line(arrow_x, arrow_y, mux1_x, arrow_y, arrow=True, color='cyan', width=3)
        self.signal_labels['ALUOutW_c'] = self._add_signal_label(
            arrow_x - 20, arrow_y - 10, 'ALUOutW_c', self.signals['ALUOutW_c']
        )
        
        # Cable PCPlus8F al "0" del mux - con más separación
        cable_y = mux1_y + 64  # Entrada "0" del mux
        self._add_line(mux1_x - 60, cable_y, mux1_x, cable_y, width=3)
        self.signal_labels['PCPlus8F'] = self._add_signal_label(
            mux1_x - 80, cable_y - 10, 'PCPlus8F', self.signals['PCPlus8F']
        )
        
        # Flip-flop PC
        ff_x = mux1_x + 100
        ff_y = mux1_y
        self._draw_flipflop(ff_x, ff_y, width=45, height=85)
        
        # Cable PC' entre mux y flip-flop
        self._add_line(mux1_x + 45, y_center, ff_x, y_center, width=3)
        self.signal_labels["PC'"] = self._add_signal_label(
            mux1_x + 62, y_center - 10, "PC'", self.signals["PC'"]
        )
        
        # Instruction Memory
        mem_x = ff_x + 120
        mem_y = y_center - 50
        self._draw_rectangle(mem_x, mem_y, 150, 100, "Instruction Memory", fill='#4A90E2')
        self._add_text(mem_x + 20, mem_y + 30, "A", font_size=10)
        self._add_text(mem_x + 130, mem_y + 70, "RD", font_size=10)
        
        # Cable PCF
        self._add_line(ff_x + 45, y_center, mem_x, y_center, width=3)
        self.signal_labels['PCF'] = self._add_signal_label(
            ff_x + 70, y_center - 10, 'PCF', self.signals['PCF']
        )
        
        # Adder (+8) - posicionado más abajo para mejor claridad
        adder_x = ff_x + 20
        adder_y = y_center + 120
        self._draw_adder(adder_x, adder_y, width=50, height=60)
        
        # Conexión PCF al adder - con ángulos claros
        self._add_line(ff_x + 45, y_center, ff_x + 45, adder_y + 15, width=2)
        self._add_line(ff_x + 45, adder_y + 15, adder_x, adder_y + 15, width=2)
        
        # Valor constante 8
        self._add_text(adder_x - 30, adder_y + 45, "8", font_size=10)
        self._add_line(adder_x - 20, adder_y + 45, adder_x, adder_y + 45, width=2)
        
        # Conexión del adder al mux (PCPlus8F) - ruta clara y separada
        self._add_line(adder_x + 50, adder_y + 30, adder_x + 90, adder_y + 30, width=2)
        self._add_line(adder_x + 90, adder_y + 30, adder_x + 90, adder_y + 140, width=2)
        self._add_line(adder_x + 90, adder_y + 140, mux1_x - 110, adder_y + 140, width=2)
        self._add_line(mux1_x - 110, adder_y + 140, mux1_x - 110, cable_y, width=2)
        self._add_line(mux1_x - 110, cable_y, mux1_x - 60, cable_y, width=2)
        
        # Flip-flop final de la etapa
        ff_final_x = mem_x + 200
        ff_final_y = y_center - 42
        self._draw_flipflop(ff_final_x, ff_final_y, width=45, height=85)
        
        # Cable InstrF
        self._add_line(mem_x + 150, y_center, ff_final_x, y_center, width=2)
        self.signal_labels['InstrF'] = self._add_signal_label(
            mem_x + 165, y_center - 10, 'InstrF', self.signals['InstrF']
        )
        
        # Instrucción actual
        self.instruction_labels['Fetch'] = self._add_instruction_box(
            x_base + 50, y_center + 280, 'Fetch', self.instructions['Fetch']
        )
    
    def _draw_decode_stage(self, x_base, y_center):
        """Dibuja la etapa Decode"""
        colors = self.design_manager.get_colors()
        
        # Título de la etapa
        self._add_text(x_base + 150, 90, "DECODE", font_size=16, bold=True, color=colors['select_bg'])
        
        # Línea vertical para InstrD
        line_x = x_base + 40
        line_y_start = y_center - 140
        line_y_end = y_center + 140
        self._add_line(line_x, line_y_start, line_x, line_y_end, width=3)
        
        # Señal InstrD
        self.signal_labels['InstrD'] = self._add_signal_label(
            line_x - 30, line_y_start - 20, 'InstrD', self.signals['InstrD']
        )
        
        # Bloque de registros/memorias seguras
        reg_x = x_base + 100
        reg_y = y_center - 60
        self._draw_rectangle(reg_x, reg_y, 120, 120, "Registers /\nSafe Memories", fill='#28A745')
        
        # Entradas Ar1 y Ar2
        self._add_text(reg_x + 10, reg_y + 30, "Ar1", font_size=9)
        self._add_text(reg_x + 10, reg_y + 60, "Ar2", font_size=9)
        
        # Salidas RDr1 y RDr2
        self._add_text(reg_x + 100, reg_y + 30, "RDr1", font_size=9)
        self._add_text(reg_x + 100, reg_y + 60, "RDr2", font_size=9)
        
        # Cables 47:44 y 43:40 - con mejor separación
        self._add_line(line_x, y_center - 30, reg_x, y_center - 30, width=2)
        self.signal_labels['47:44'] = self._add_signal_label(
            line_x + 25, y_center - 40, '47:44', self.signals['47:44']
        )
        
        self._add_line(line_x, y_center, reg_x, y_center, width=2)
        self.signal_labels['43:40'] = self._add_signal_label(
            line_x + 25, y_center - 10, '43:40', self.signals['43:40']
        )
        
        # Mux 2 - posicionado más abajo para claridad
        mux2_x = x_base + 140
        mux2_y = y_center + 120
        self._draw_mux(mux2_x, mux2_y, "2", width=45, height=85)
        
        # Cable 39:8 al mux (entrada 0) - ruta clara y separada
        self._add_line(line_x, y_center + 60, line_x + 40, y_center + 60, width=2)
        self._add_line(line_x + 40, y_center + 60, line_x + 40, mux2_y + 64, width=2)
        self._add_line(line_x + 40, mux2_y + 64, mux2_x, mux2_y + 64, width=2)
        self.signal_labels['39:8'] = self._add_signal_label(
            line_x + 10, y_center + 50, '39:8', self.signals['39:8']
        )
        
        # Flip-flop final
        ff_final_x = x_base + 280
        ff_final_y = y_center - 42
        self._draw_flipflop(ff_final_x, ff_final_y, width=45, height=85)
        
        # Cables de salida de registros
        # SrcAD - directo al flip-flop
        self._add_line(reg_x + 120, y_center - 30, ff_final_x, y_center - 30, width=2)
        self.signal_labels['SrcAD'] = self._add_signal_label(
            reg_x + 160, y_center - 40, 'SrcAD', self.signals['SrcAD']
        )
        
        # Rd_SpecialD al mux (entrada 1) - con ruta clara
        self._add_line(reg_x + 120, y_center, reg_x + 160, y_center, width=2)
        self._add_line(reg_x + 160, y_center, reg_x + 160, mux2_y + 21, width=2)
        self._add_line(reg_x + 160, mux2_y + 21, mux2_x, mux2_y + 21, width=2)
        self.signal_labels['Rd_SpecialD'] = self._add_signal_label(
            reg_x + 130, y_center + 20, 'Rd_SpecialD', self.signals['Rd_SpecialD']
        )
        
        # SrcBD desde el mux - con ruta clara hacia el flip-flop
        self._add_line(mux2_x + 45, mux2_y + 42, mux2_x + 120, mux2_y + 42, width=2)
        self._add_line(mux2_x + 120, mux2_y + 42, mux2_x + 120, y_center + 30, width=2)
        self._add_line(mux2_x + 120, y_center + 30, ff_final_x, y_center + 30, width=2)
        self.signal_labels['SrcBD'] = self._add_signal_label(
            mux2_x + 70, mux2_y + 32, 'SrcBD', self.signals['SrcBD']
        )
        
        # Instrucción actual
        self.instruction_labels['Decode'] = self._add_instruction_box(
            x_base + 50, y_center + 280, 'Decode', self.instructions['Decode']
        )
    
    def _draw_execute_stage(self, x_base, y_center):
        """Dibuja la etapa Execute"""
        colors = self.design_manager.get_colors()
        
        # Título de la etapa
        self._add_text(x_base + 150, 90, "EXECUTE", font_size=16, bold=True, color=colors['select_bg'])
        
        # ALU
        alu_x = x_base + 80
        alu_y = y_center - 60
        self._draw_alu(alu_x, alu_y, width=100, height=120)
        
        # Señales de entrada
        # SrcAE
        self._add_line(x_base, y_center - 30, alu_x, y_center - 30, width=2)
        self.signal_labels['SrcAE'] = self._add_signal_label(
            x_base + 20, y_center - 40, 'SrcAE', self.signals['SrcAE']
        )
        
        # SrcBE
        self._add_line(x_base, y_center + 30, alu_x, y_center + 30, width=2)
        self.signal_labels['SrcBE'] = self._add_signal_label(
            x_base + 20, y_center + 20, 'SrcBE', self.signals['SrcBE']
        )
        
        # Flip-flop final
        ff_final_x = x_base + 220
        ff_final_y = y_center - 42
        self._draw_flipflop(ff_final_x, ff_final_y, width=45, height=85)
        
        # ALUResultE
        self._add_line(alu_x + 100, y_center, ff_final_x, y_center, width=2)
        self.signal_labels['ALUResultE'] = self._add_signal_label(
            alu_x + 120, y_center - 10, 'ALUResultE', self.signals['ALUResultE']
        )
        
        # Instrucción actual
        self.instruction_labels['Execute'] = self._add_instruction_box(
            x_base + 50, y_center + 280, 'Execute', self.instructions['Execute']
        )
    
    def _draw_memory_stage(self, x_base, y_center):
        """Dibuja la etapa Memory"""
        colors = self.design_manager.get_colors()
        
        # Título de la etapa
        self._add_text(x_base + 150, 90, "MEMORY", font_size=16, bold=True, color=colors['select_bg'])
        
        # Big Memories
        mem_x = x_base + 100
        mem_y = y_center - 100
        self._draw_rectangle(mem_x, mem_y, 120, 80, "Big Memories", fill='#DC3545')
        self._add_text(mem_x + 10, mem_y + 40, "A_G", font_size=9)
        self._add_text(mem_x + 100, mem_y + 40, "RD_G", font_size=9)
        
        # Mux 3 - posicionado más abajo para claridad
        mux3_x = x_base + 120
        mux3_y = y_center + 80
        self._draw_mux(mux3_x, mux3_y, "3", width=45, height=85)
        
        # Señal ALUOutM
        self._add_line(x_base, y_center, x_base + 50, y_center, width=2)
        self.signal_labels['ALUOutM'] = self._add_signal_label(
            x_base + 10, y_center - 10, 'ALUOutM', self.signals['ALUOutM']
        )
        
        # Conexión a memoria - con ruta clara
        self._add_line(x_base + 50, y_center, x_base + 50, mem_y + 40, width=2)
        self._add_line(x_base + 50, mem_y + 40, mem_x, mem_y + 40, width=2)
        
        # Conexión a mux (entrada 0) - con amplia separación
        self._add_line(x_base + 50, y_center, x_base + 50, mux3_y + 64 + 30, width=2)
        self._add_line(x_base + 50, mux3_y + 64 + 30, x_base + 70, mux3_y + 64 + 30, width=2)
        self._add_line(x_base + 70, mux3_y + 64 + 30, x_base + 70, mux3_y + 64, width=2)
        self._add_line(x_base + 70, mux3_y + 64, mux3_x, mux3_y + 64, width=2)
        
        # RD_G_a desde memoria al mux (entrada 1) - ruta bien separada
        self._add_line(mem_x + 120, mem_y + 40, mem_x + 160, mem_y + 40, width=2)
        self._add_line(mem_x + 160, mem_y + 40, mem_x + 160, mux3_y + 21, width=2)
        self._add_line(mem_x + 160, mux3_y + 21, mux3_x, mux3_y + 21, width=2)
        self.signal_labels['RD_G_a'] = self._add_signal_label(
            mem_x + 130, mem_y + 50, 'RD_G_a', self.signals['RD_G_a']
        )
        
        # Flip-flop final
        ff_final_x = x_base + 280
        ff_final_y = y_center - 42
        self._draw_flipflop(ff_final_x, ff_final_y, width=45, height=85)
        
        # ALUOutM_O - con ruta clara
        self._add_line(mux3_x + 45, mux3_y + 42, mux3_x + 140, mux3_y + 42, width=2)
        self._add_line(mux3_x + 140, mux3_y + 42, mux3_x + 140, y_center, width=2)
        self._add_line(mux3_x + 140, y_center, ff_final_x, y_center, width=2)
        self.signal_labels['ALUOutM_O'] = self._add_signal_label(
            mux3_x + 80, mux3_y + 32, 'ALUOutM_O', self.signals['ALUOutM_O']
        )
        
        # Instrucción actual
        self.instruction_labels['Memory'] = self._add_instruction_box(
            x_base + 50, y_center + 280, 'Memory', self.instructions['Memory']
        )
    
    def _draw_writeback_stage(self, x_base, y_center):
        """Dibuja la etapa WriteBack"""
        colors = self.design_manager.get_colors()
        
        # Título de la etapa
        self._add_text(x_base + 150, 90, "WRITEBACK", font_size=16, bold=True, color=colors['select_bg'])
        
        # Flecha celeste (ALUOutW_c)
        arrow_x = x_base + 100
        arrow_y = y_center
        self._add_line(arrow_x, arrow_y, arrow_x - 50, arrow_y, arrow=True, color='cyan', width=3)
        self._add_text(arrow_x - 25, arrow_y - 20, "ALUOutW_c", font_size=10, color='cyan')
        
        # Instrucción actual
        self.instruction_labels['WriteBack'] = self._add_instruction_box(
            x_base + 50, y_center + 280, 'WriteBack', self.instructions['WriteBack']
        )
    
    # Métodos auxiliares para dibujar componentes específicos
    
    def _draw_mux(self, x, y, label, width=45, height=85):
        """Dibuja un multiplexor"""
        colors = self.design_manager.get_colors()
        
        # Cuerpo del mux
        self._draw_rectangle(x, y, width, height, "", fill='#6C757D')
        
        # Etiqueta del mux
        self._add_text(x + width//2, y - 10, f"MUX {label}", font_size=9)
        
        # Etiquetas de entradas con mayor claridad
        # Entrada "1" (arriba)
        self._add_text(x + 10, y + 20, "1", font_size=10, color='white', bold=True)
        # Entrada "0" (abajo)
        self._add_text(x + 10, y + height - 20, "0", font_size=10, color='white', bold=True)
        
        # Indicadores visuales de las entradas
        # Marca para entrada 1
        self.canvas.create_oval(x - 8, y + 18, x + 3, y + 29, fill='white', outline='')
        # Marca para entrada 0
        self.canvas.create_oval(x - 8, y + height - 29, x + 3, y + height - 18, fill='white', outline='')
    
    def _draw_flipflop(self, x, y, width=45, height=85):
        """Dibuja un flip-flop"""
        colors = self.design_manager.get_colors()
        
        # Cuerpo del flip-flop
        self._draw_rectangle(x, y, width, height, "", fill='#6C757D')
        
        # Triángulo interno (símbolo de clock)
        triangle_x = x + width//2
        triangle_y = y + height - 15
        points = [
            triangle_x - 8, triangle_y,
            triangle_x + 8, triangle_y,
            triangle_x, triangle_y - 12
        ]
        self.canvas.create_polygon(points, fill='white', outline='black')
        
        # Etiqueta
        self._add_text(x + width//2, y - 10, "D-FF", font_size=9)
    
    def _draw_adder(self, x, y, width=50, height=60):
        """Dibuja un sumador con forma de trapecio"""
        colors = self.design_manager.get_colors()
        
        # Forma trapezoidal
        points = [
            x, y,
            x + width, y,
            x + width - 10, y + height,
            x + 10, y + height
        ]
        self.canvas.create_polygon(points, fill='#FFC107', outline=colors['fg'], width=2)
        
        # Símbolo +
        self._add_text(x + width//2, y + height//2, "+", font_size=16, bold=True)
    
    def _draw_alu(self, x, y, width=100, height=120):
        """Dibuja la ALU"""
        colors = self.design_manager.get_colors()
        
        # Forma de la ALU (trapecio irregular)
        points = [
            x, y,
            x + width, y,
            x + width - 20, y + height//2,
            x + width, y + height,
            x, y + height,
            x + 20, y + height//2
        ]
        self.canvas.create_polygon(points, fill='#007ACC', outline=colors['fg'], width=2)
        
        # Texto
        self._add_text(x + width//2, y + height//2, "ALU", font_size=14, bold=True, color='white')
    
    def _draw_rectangle(self, x, y, width, height, text="", fill=None):
        """Dibuja un rectángulo"""
        colors = self.design_manager.get_colors()
        if not fill:
            fill = colors['button_bg']
        
        rect = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=fill,
            outline=colors['fg'],
            width=2
        )
        
        if text:
            lines = text.split('\n')
            for i, line in enumerate(lines):
                self._add_text(
                    x + width//2, 
                    y + height//2 - (len(lines)-1)*8 + i*16, 
                    line, 
                    font_size=10, 
                    color='white'
                )
        
        return rect
    
    def _add_line(self, x1, y1, x2, y2, arrow=False, color=None, width=3, dash=None):
        """Agrega una línea al diagrama"""
        colors = self.design_manager.get_colors()
        if not color:
            color = colors['fg']
        
        arrow_config = tk.LAST if arrow else None
        
        line = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=width,
            arrow=arrow_config,
            arrowshape=(16, 20, 6),
            dash=dash
        )
        return line
    
    def _add_text(self, x, y, text, font_size=10, bold=False, color=None):
        """Agrega texto al diagrama"""
        colors = self.design_manager.get_colors()
        if not color:
            color = colors['fg']
        
        font_type = 'bold' if bold else 'normal'
        font = (self.design_manager.get_font(font_type).cget('family'), font_size, 'bold' if bold else 'normal')
        
        text_item = self.canvas.create_text(
            x, y,
            text=text,
            fill=color,
            font=font
        )
        return text_item
    
    def _add_signal_label(self, x, y, signal_name, value):
        """Agrega una etiqueta de señal que se puede actualizar"""
        colors = self.design_manager.get_colors()
        
        # Fondo para la señal - más grande para mejor visibilidad
        bg = self.canvas.create_rectangle(
            x - 2, y - 2, x + 50, y + 16,
            fill=colors['entry_bg'],
            outline=colors['button_bg'],
            width=2
        )
        
        # Texto de la señal
        text = self.canvas.create_text(
            x + 25, y + 7,
            text=value,
            fill=colors['entry_fg'],
            font=('Consolas', 10, 'bold'),
            anchor='center'
        )
        
        return {'bg': bg, 'text': text, 'name': signal_name}
    
    def _add_instruction_box(self, x, y, stage, instruction):
        """Agrega una caja de instrucción para una etapa"""
        colors = self.design_manager.get_colors()
        
        # Caja de instrucción
        box = self.canvas.create_rectangle(
            x, y, x + 200, y + 40,
            fill=colors['entry_bg'],
            outline=colors['fg'],
            width=2
        )
        
        # Texto de la instrucción
        text = self.canvas.create_text(
            x + 100, y + 20,
            text=instruction,
            fill=colors['entry_fg'],
            font=self.design_manager.get_font('normal')
        )
        
        return {'box': box, 'text': text, 'stage': stage}
    
    # Métodos públicos para get/set de señales e instrucciones
    
    def get_signal(self, signal_name):
        """Obtiene el valor de una señal"""
        return self.signals.get(signal_name, '0x0')
    
    def set_signal(self, signal_name, value):
        """Establece el valor de una señal y actualiza la visualización"""
        if signal_name in self.signals:
            self.signals[signal_name] = value
            
            # Actualizar la etiqueta visual si existe
            for label in self.signal_labels.values():
                if label['name'] == signal_name:
                    self.canvas.itemconfig(label['text'], text=value)
                    break
    
    def get_instruction(self, stage):
        """Obtiene la instrucción actual de una etapa"""
        return self.instructions.get(stage, '')
    
    def set_instruction(self, stage, instruction):
        """Establece la instrucción de una etapa y actualiza la visualización"""
        if stage in self.instructions:
            self.instructions[stage] = instruction
            
            # Actualizar la caja visual si existe
            for label in self.instruction_labels.values():
                if label['stage'] == stage:
                    self.canvas.itemconfig(label['text'], text=instruction)
                    break
    
    def update_all_signals(self):
        """Actualiza todas las señales desde cpu_excel"""
        # Aquí podrías leer los valores reales desde cpu_excel
        # Por ahora solo es un placeholder
        pass
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        super().update_theme()
        
        # Actualizar colores de elementos específicos
        colors = self.design_manager.get_colors()
        
        # Actualizar cajas de instrucciones
        for label in self.instruction_labels.values():
            self.canvas.itemconfig(label['box'], fill=colors['entry_bg'], outline=colors['fg'])
            self.canvas.itemconfig(label['text'], fill=colors['entry_fg'])
        
        # Actualizar etiquetas de señales
        for label in self.signal_labels.values():
            self.canvas.itemconfig(label['bg'], fill=colors['entry_bg'], outline=colors['button_bg'])
            self.canvas.itemconfig(label['text'], fill=colors['entry_fg'])
    
    # ----------------------------------------------------------------------
    # cpu_pipeline_diagram.py
    # ----------------------------------------------------------------------
    def update_signals(self):
        """
        Carga desde `self.cpu_excel` **todas** las señales y los nombres de
        instrucción por etapa y refresca el diagrama.
        """
        # -------------------- 1. Señales -------------------------------
        signal_map = {
            # Fetch
            "PC'":          self.cpu_excel.read_pc_prime,
            'PCF':          self.cpu_excel.read_pcf,
            'PCPlus8F':     self.cpu_excel.read_pcplus8f,
            'InstrF':       self.cpu_excel.read_instrf,
            'ALUOutW_c':    self.cpu_excel.read_aluoutw_c,
            # Decode
            'InstrD':       self.cpu_excel.read_instrd,
            '47:44':        self.cpu_excel.read_47_44,
            '43:40':        self.cpu_excel.read_43_40,
            '39:8':         self.cpu_excel.read_39_8,
            'SrcAD':        self.cpu_excel.read_srcad,
            'Rd_SpecialD':  self.cpu_excel.read_rd_speciald,
            'SrcBD':        self.cpu_excel.read_srcbd,
            # Execute
            'SrcAE':        self.cpu_excel.read_srcae,
            'SrcBE':        self.cpu_excel.read_srcbe,
            'ALUResultE':   self.cpu_excel.read_aluresulte,
            # Memory
            'ALUOutM':      self.cpu_excel.read_aluoutm,
            'RD_G_a':       self.cpu_excel.read_rd_g_a,
            'ALUOutM_O':    self.cpu_excel.read_aluoutm_o
        }

        for name, reader in signal_map.items():
            try:
                _dtype, value = reader()
                self.set_signal(name, str(value))
            except Exception as err:
                print(f"[update_signals] ❗No pude leer '{name}': {err}")

        # -------------------- 2. Instrucciones -------------------------
        instr_map = {
            'Fetch':     self.cpu_excel.read_state_fetch,
            'Decode':    self.cpu_excel.read_state_decode,
            'Execute':   self.cpu_excel.read_state_execute,
            'Memory':    self.cpu_excel.read_state_memory,
            'WriteBack': self.cpu_excel.read_state_writeBack
        }

        for stage, reader in instr_map.items():
            try:
                _dtype, instr = reader()
                self.set_instruction(stage, str(instr))
            except Exception as err:
                print(f"[update_signals] ❗No pude leer instrucción '{stage}': {err}")