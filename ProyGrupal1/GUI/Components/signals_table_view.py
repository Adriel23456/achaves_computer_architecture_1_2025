"""
signals_table_view.py - Componente de tabla para visualizar señales del CPU
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_scrollbar import ScrollableFrame
from ExtraPrograms.table_control import DataType

# Mapa de tamaños de señales extraído de la función reset()
SIGNAL_SIZES = {
    # Decode
    "PC'": 32,
    "PCF": 32,
    "PCPlus8F": 32,
    "InstrF": 64,
    
    # Fetch
    "InstrD": 64,
    "PCF_D": 32,
    "55:52": 4,
    "63:56": 8,
    "47:44": 4,
    "43:40": 4,
    "39:8": 32,
    "51:48": 4,
    "MemWriteP": 1,
    "MemWriteV": 1,
    "RegisterInA": 1,
    "RegisterInB": 2,
    "ImmediateOp": 1,
    "BranchE": 1,
    "LogOutD": 1,
    "ComsD": 1,
    "PrintEnD": 2,
    "RegWriteSD": 1,
    "RegWriteRD": 1,
    "MemOpD": 2,
    "MemWriteGD": 1,
    "MemWriteDD": 1,
    "MemByteD": 1,
    "PCSrcD": 1,
    "FlagsUpdD": 1,
    "ALUSrcD": 6,
    "BranchOpD": 3,
    "RdR1_A": 32,
    "RdR2_A": 32,
    "RdW1_A": 32,
    "RdW2_A": 32,
    "Kd_A": 32,
    "Rd_A": 32,
    "SrcAD_0": 32,
    "SrcAD": 32,
    "Rd_SpecialD": 32,
    "SrcBD": 32,
    
    # Execute
    "RegWriteSE": 1,
    "RegWriteRE": 1,
    "MemOpE": 2,
    "MemWriteGE": 1,
    "MemWriteDE": 1,
    "MemByteE": 1,
    "PCSrcE": 1,
    "FlagsUpdE": 1,
    "ALUSrcE": 6,
    "BranchOpE": 3,
    "PrintEnE": 2,
    "ComsE": 1,
    "LogOutE": 1,
    "BranchOpE_2": 3,
    "FlagsE": 4,
    "SrcAE": 32,
    "Rd_SpecialE": 32,
    "SrcBE": 32,
    "Flags'": 4,
    "ALUFlagOut": 4,
    "CarryIn": 1,
    "CondExE": 1,
    "SafeFlagsOut": 2,
    "LoginInBlockE": 4,
    "RdE": 4,
    "ALUResultE": 32,
    "PCSrc_AND_E": 1,
    "Timer_Safe": 32,
    "Block_StatusIn": 8,
    "Block_StatusOut": 8,
    "Attempts_Available": 4,
    
    # Memory
    "RegWriteSM": 1,
    "RegWriteRM": 1,
    "MemOpM": 2,
    "MemWriteGM": 1,
    "MemWriteDM": 1,
    "MemByteM": 1,
    "PCSrcM": 1,
    "PrintEnM": 2,
    "ALUOutM": 32,
    "Rd_SpecialM": 32,
    "RdM": 4,
    "Rd_SpecialM_B": 32,
    "Rd_SpecialM_C": 32,
    "Rd_SpecialM_D": 32,
    "Rd_SpecialM_E": 32,
    "Rd_G_A": 32,
    "Rd_D_A": 32,
    "ALUOutM_O": 32,
    
    # WriteBack
    "RegWriteSM_WB": 1,
    "RegWriteRM_WB": 1,
    "PCSrcM_WB": 1,
    "MemByteM_WB": 1,
    "PrintEnM_WB": 2,
    "ALUOutW": 32,
    "ALUOutW_B": 32,
    "ALUOutW_C": 32,
    "Int_PL": 32,
    "ASCII_PL": 32,
    "B_PL": 32,
    "RdW": 4,
}

class SignalsTableView(tk.Frame):
    """Vista de tabla para mostrar todas las señales del CPU por etapas"""
    
    def __init__(self, parent, design_manager, cpu_excel):
        self.design_manager = design_manager
        self.cpu_excel = cpu_excel
        colors = design_manager.get_colors()
        
        super().__init__(parent, bg=colors['bg'])
        
        # Estructura de datos para las señales por etapa
        self.signal_sections = {
            'Decode': {
                'items': [
                    ("PC'", lambda: self.cpu_excel.read_pc_prime()),
                    ('PCF', lambda: self.cpu_excel.read_pcf()),
                    ('PCPlus8F', lambda: self.cpu_excel.read_pcplus8f()),
                    ('InstrF', lambda: self.cpu_excel.read_instrf()),
                ],
                'labels': []
            },
            'Fetch': {
                'items': [
                    ('InstrD', lambda: self.cpu_excel.read_instrd()),
                    ('PCF_D', lambda: self.cpu_excel.read_pcf_d()),
                    ('55:52', lambda: self.cpu_excel.read_55_52()),
                    ('63:56', lambda: self.cpu_excel.read_63_56()),
                    ('47:44', lambda: self.cpu_excel.read_47_44()),
                    ('43:40', lambda: self.cpu_excel.read_43_40()),
                    ('39:8', lambda: self.cpu_excel.read_39_8()),
                    ('51:48', lambda: self.cpu_excel.read_51_48()),
                    ('MemWriteP', lambda: self.cpu_excel.read_memwritep()),
                    ('MemWriteV', lambda: self.cpu_excel.read_memwritev()),
                    ('RegisterInA', lambda: self.cpu_excel.read_registerina()),
                    ('RegisterInB', lambda: self.cpu_excel.read_registerinb()),
                    ('ImmediateOp', lambda: self.cpu_excel.read_immediateop()),
                    ('BranchE', lambda: self.cpu_excel.read_branche()),
                    ('LogOutD', lambda: self.cpu_excel.read_logoutd()),
                    ('ComsD', lambda: self.cpu_excel.read_comsd()),
                    ('PrintEnD', lambda: self.cpu_excel.read_printend()),
                    ('RegWriteSD', lambda: self.cpu_excel.read_regwritesd()),
                    ('RegWriteRD', lambda: self.cpu_excel.read_regwriterd()),
                    ('MemOpD', lambda: self.cpu_excel.read_memopd()),
                    ('MemWriteGD', lambda: self.cpu_excel.read_memwritegd()),
                    ('MemWriteDD', lambda: self.cpu_excel.read_memwritedd()),
                    ('MemByteD', lambda: self.cpu_excel.read_membyted()),
                    ('PCSrcD', lambda: self.cpu_excel.read_pcsrcd()),
                    ('FlagsUpdD', lambda: self.cpu_excel.read_flagsupdd()),
                    ('ALUSrcD', lambda: self.cpu_excel.read_alusrcd()),
                    ('BranchOpD', lambda: self.cpu_excel.read_branchopd()),
                    ('RdR1_A', lambda: self.cpu_excel.read_rdr1_a()),
                    ('RdR2_A', lambda: self.cpu_excel.read_rdr2_a()),
                    ('RdW1_A', lambda: self.cpu_excel.read_rdw1_a()),
                    ('RdW2_A', lambda: self.cpu_excel.read_rdw2_a()),
                    ('Kd_A', lambda: self.cpu_excel.read_kd_a()),
                    ('Rd_A', lambda: self.cpu_excel.read_rd_a()),
                    ('SrcAD_0', lambda: self.cpu_excel.read_srcad_0()),
                    ('SrcAD', lambda: self.cpu_excel.read_srcad()),
                    ('Rd_SpecialD', lambda: self.cpu_excel.read_rd_speciald()),
                    ('SrcBD', lambda: self.cpu_excel.read_srcbd()),
                ],
                'labels': []
            },
            'Execute': {
                'items': [
                    ('RegWriteSE', lambda: self.cpu_excel.read_regwritese()),
                    ('RegWriteRE', lambda: self.cpu_excel.read_regwritere()),
                    ('MemOpE', lambda: self.cpu_excel.read_memope()),
                    ('MemWriteGE', lambda: self.cpu_excel.read_memwritege()),
                    ('MemWriteDE', lambda: self.cpu_excel.read_memwritede()),
                    ('MemByteE', lambda: self.cpu_excel.read_membytee()),
                    ('PCSrcE', lambda: self.cpu_excel.read_pcsrce()),
                    ('FlagsUpdE', lambda: self.cpu_excel.read_flagsupde()),
                    ('ALUSrcE', lambda: self.cpu_excel.read_alusrce()),
                    ('BranchOpE', lambda: self.cpu_excel.read_branchope()),
                    ('PrintEnE', lambda: self.cpu_excel.read_printene()),
                    ('ComsE', lambda: self.cpu_excel.read_comse()),
                    ('LogOutE', lambda: self.cpu_excel.read_logoute()),
                    ('BranchOpE_2', lambda: self.cpu_excel.read_branchope_2()),
                    ('FlagsE', lambda: self.cpu_excel.read_flagse()),
                    ('SrcAE', lambda: self.cpu_excel.read_srcae()),
                    ('Rd_SpecialE', lambda: self.cpu_excel.read_rd_speciale()),
                    ('SrcBE', lambda: self.cpu_excel.read_srcbe()),
                    ("Flags'", lambda: self.cpu_excel.read_flags_prime()),
                    ('ALUFlagOut', lambda: self.cpu_excel.read_aluflagout()),
                    ('CarryIn', lambda: self.cpu_excel.read_carryin()),
                    ('CondExE', lambda: self.cpu_excel.read_condexe()),
                    ('SafeFlagsOut', lambda: self.cpu_excel.read_safeflagsout()),
                    ('LoginInBlockE', lambda: self.cpu_excel.read_logininblocke()),
                    ('RdE', lambda: self.cpu_excel.read_rde()),
                    ('ALUResultE', lambda: self.cpu_excel.read_aluresulte()),
                    ('PCSrc_AND_E', lambda: self.cpu_excel.read_pcsrc_and_e()),
                    ('Timer_Safe', lambda: self.cpu_excel.read_timer_safe()),
                    ('Block_StatusIn', lambda: self.cpu_excel.read_block_statusIn()),
                    ('Block_StatusOut', lambda: self.cpu_excel.read_block_statusOut()),
                    ('Attempts_Available', lambda: self.cpu_excel.read_attempts_available()),
                ],
                'labels': []
            },
            'Memory': {
                'items': [
                    ('RegWriteSM', lambda: self.cpu_excel.read_regwritesm()),
                    ('RegWriteRM', lambda: self.cpu_excel.read_regwriterm()),
                    ('MemOpM', lambda: self.cpu_excel.read_memopm()),
                    ('MemWriteGM', lambda: self.cpu_excel.read_memwritegm()),
                    ('MemWriteDM', lambda: self.cpu_excel.read_memwritedm()),
                    ('MemByteM', lambda: self.cpu_excel.read_membytem()),
                    ('PCSrcM', lambda: self.cpu_excel.read_pcsrcm()),
                    ('PrintEnM', lambda: self.cpu_excel.read_printenm()),
                    ('ALUOutM', lambda: self.cpu_excel.read_aluoutm()),
                    ('Rd_SpecialM', lambda: self.cpu_excel.read_rd_specialm()),
                    ('RdM', lambda: self.cpu_excel.read_rdm()),
                    ('Rd_SpecialM_B', lambda: self.cpu_excel.read_rd_specialm_b()),
                    ('Rd_SpecialM_C', lambda: self.cpu_excel.read_rd_specialm_c()),
                    ('Rd_SpecialM_D', lambda: self.cpu_excel.read_rd_specialm_d()),
                    ('Rd_SpecialM_E', lambda: self.cpu_excel.read_rd_specialm_e()),
                    ('Rd_G_A', lambda: self.cpu_excel.read_rd_g_a()),
                    ('Rd_D_A', lambda: self.cpu_excel.read_rd_d_a()),
                    ('ALUOutM_O', lambda: self.cpu_excel.read_aluoutm_o()),
                ],
                'labels': []
            },
            'WriteBack': {
                'items': [
                    ('RegWriteSM_WB', lambda: self.cpu_excel.read_regwritesm_wb()),
                    ('RegWriteRM_WB', lambda: self.cpu_excel.read_regwriterm_wb()),
                    ('PCSrcM_WB', lambda: self.cpu_excel.read_pcsrcm_wb()),
                    ('MemByteM_WB', lambda: self.cpu_excel.read_membytem_wb()),
                    ('PrintEnM_WB', lambda: self.cpu_excel.read_printenm_wb()),
                    ('ALUOutW', lambda: self.cpu_excel.read_aluoutw()),
                    ('ALUOutW_B', lambda: self.cpu_excel.read_aluoutw_b()),
                    ('ALUOutW_C', lambda: self.cpu_excel.read_aluoutw_c()),
                    ('Int_PL', lambda: self.cpu_excel.read_int_pl()),
                    ('ASCII_PL', lambda: self.cpu_excel.read_acii_pl()),
                    ('B_PL', lambda: self.cpu_excel.read_b_pl()),
                    ('RdW', lambda: self.cpu_excel.read_rdw()),
                ],
                'labels': []
            }
        }
        
        self._create_ui()
        # Cargar valores iniciales
        self.update_all_signals()
    
    def _create_ui(self):
        """Crea la interfaz de la tabla de señales"""
        colors = self.design_manager.get_colors()
        
        # Frame con scroll
        self.scroll_frame = ScrollableFrame(self, self.design_manager)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear secciones por etapa
        for stage_name in self.signal_sections:
            self._create_stage_section(self.scroll_frame.interior, stage_name)
    
    def _create_stage_section(self, parent, stage_name):
        """Crea una sección para una etapa del pipeline"""
        colors = self.design_manager.get_colors()
        
        # Frame de la sección
        section_frame = tk.LabelFrame(
            parent,
            text=f"Etapa {stage_name}",
            font=self.design_manager.get_font('bold'),
            bg=colors['bg'],
            fg=colors['fg'],
            relief=tk.SOLID,
            borderwidth=2,
            labelanchor='n'
        )
        section_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame para la tabla
        table_frame = tk.Frame(section_frame, bg=colors['bg'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Headers - AHORA SON 4 COLUMNAS
        headers = ['Señal', 'Tipo', 'Tamaño', 'Valor']
        for col, header in enumerate(headers):
            label = tk.Label(
                table_frame,
                text=header,
                font=self.design_manager.get_font('bold'),
                bg=colors['sidebar_bg'],
                fg=colors['sidebar_button_fg'],
                padx=15,
                pady=8,
                relief=tk.RIDGE,
                borderwidth=1
            )
            label.grid(row=0, column=col, sticky='ew')
        
        # Configurar columnas
        table_frame.grid_columnconfigure(0, weight=1, minsize=150)
        table_frame.grid_columnconfigure(1, weight=1, minsize=100)
        table_frame.grid_columnconfigure(2, weight=1, minsize=100)
        table_frame.grid_columnconfigure(3, weight=2, minsize=250)
        
        # Crear filas para cada señal
        row_idx = 1
        for signal_name, read_func in self.signal_sections[stage_name]['items']:
            # Obtener tamaño de la señal
            size_bits = SIGNAL_SIZES.get(signal_name, 32)  # Por defecto 32 bits
            
            # Crear celdas
            cells = {}
            
            # Celda de nombre de señal
            cells['name'] = tk.Label(
                table_frame,
                text=signal_name,
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=15,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1,
                anchor='w'
            )
            cells['name'].grid(row=row_idx, column=0, sticky='ew')
            
            # Celda de tipo
            cells['type'] = tk.Label(
                table_frame,
                text='',
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=15,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1
            )
            cells['type'].grid(row=row_idx, column=1, sticky='ew')
            
            # Celda de tamaño
            cells['size'] = tk.Label(
                table_frame,
                text=f'{size_bits} bits',
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=15,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1
            )
            cells['size'].grid(row=row_idx, column=2, sticky='ew')
            
            # Celda de valor
            cells['value'] = tk.Label(
                table_frame,
                text='',
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=15,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1,
                anchor='w'
            )
            cells['value'].grid(row=row_idx, column=3, sticky='ew')
            
            # Guardar referencias
            self.signal_sections[stage_name]['labels'].append({
                'cells': cells,
                'read_func': read_func,
                'size_bits': size_bits,
                'signal_name': signal_name
            })
            
            row_idx += 1
    
    def _convert_value_to_format(self, value, data_type, size_bits):
        """Convierte un valor decimal al formato especificado por data_type"""
        if value is None:
            return "None"
        
        # Asegurar que el valor sea entero
        if isinstance(value, str):
            # Si ya viene formateado, extraer el valor numérico
            if value.startswith('0x'):
                value = int(value, 16)
            elif value.startswith('0b'):
                value = int(value, 2)
            elif value.startswith('0d'):
                value = int(value[2:])
            else:
                try:
                    value = int(value)
                except:
                    return str(value)  # Si no es convertible, devolver como string
        
        # Convertir según el tipo de dato
        if data_type == DataType.HEX:
            # Calcular cantidad de caracteres hex según el tamaño
            hex_chars = (size_bits + 3) // 4
            # Aplicar máscara para el tamaño correcto
            mask = (1 << size_bits) - 1
            value = value & mask
            return f"0x{value:0{hex_chars}X}"
        
        elif data_type == DataType.BINARY:
            # Aplicar máscara para el tamaño correcto
            mask = (1 << size_bits) - 1
            value = value & mask
            return f"0b{value:0{size_bits}b}"
        
        elif data_type == DataType.INT:
            # Para decimal, mantener el signo si es negativo
            # Verificar si el valor debe interpretarse como negativo
            if size_bits < 32 and value >= (1 << (size_bits - 1)):
                # Es un valor negativo en complemento a 2
                value = value - (1 << size_bits)
            return f"0d{value}"
        
        elif data_type == DataType.STRING:
            return str(value)
        
        else:
            # Por defecto, decimal
            return f"0d{value}"
    
    def update_all_signals(self):
        """Actualiza todos los valores de las señales"""
        for stage_name, stage_data in self.signal_sections.items():
            for label_data in stage_data['labels']:
                try:
                    # Leer valor
                    data_type, value = label_data['read_func']()
                    
                    # Actualizar tipo
                    if data_type == DataType.STRING:
                        type_str = "String"
                    elif data_type == DataType.HEX:
                        type_str = "Hex"
                    elif data_type == DataType.BINARY:
                        type_str = "Binary"
                    elif data_type == DataType.INT:
                        type_str = "Decimal"
                    else:
                        type_str = "Unknown"
                    
                    label_data['cells']['type']['text'] = type_str
                    
                    # Convertir valor al formato correcto
                    display_value = self._convert_value_to_format(
                        value, 
                        data_type, 
                        label_data['size_bits']
                    )
                    
                    # Actualizar valor
                    label_data['cells']['value']['text'] = display_value
                    
                    # Colorear según el valor
                    colors = self.design_manager.get_colors()
                    if value == 0 or value == "0":
                        # Valor cero - color normal
                        for cell in label_data['cells'].values():
                            cell['fg'] = colors['entry_fg']
                    else:
                        # Valor no cero - resaltar solo el valor
                        label_data['cells']['value']['fg'] = colors['sidebar_button_active_bg']
                        label_data['cells']['name']['fg'] = colors['entry_fg']
                        label_data['cells']['type']['fg'] = colors['entry_fg']
                        label_data['cells']['size']['fg'] = colors['entry_fg']
                        
                except Exception as e:
                    # Error al leer
                    label_data['cells']['type']['text'] = "Error"
                    label_data['cells']['value']['text'] = str(e)
                    
                    colors = self.design_manager.get_colors()
                    for cell in label_data['cells'].values():
                        cell['fg'] = colors['select_bg']
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        self.configure(bg=colors['bg'])
        
        # Actualizar scroll frame
        if hasattr(self, 'scroll_frame'):
            self.scroll_frame.update_theme()
        
        # Actualizar todas las celdas
        for stage_data in self.signal_sections.values():
            for label_data in stage_data['labels']:
                for cell in label_data['cells'].values():
                    cell.configure(bg=colors['entry_bg'])