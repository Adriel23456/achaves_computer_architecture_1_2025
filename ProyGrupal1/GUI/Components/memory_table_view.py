"""
memory_table_view.py - Componente de tabla para visualizar memorias del CPU
"""
import tkinter as tk
from tkinter import ttk
from GUI.Components.styled_scrollbar import ScrollableFrame
from ExtraPrograms.table_control import DataType

class MemoryTableView(tk.Frame):
    """Vista de tabla para mostrar todas las memorias del CPU"""
    
    def __init__(self, parent, design_manager, cpu_excel):
        self.design_manager = design_manager
        self.cpu_excel = cpu_excel
        colors = design_manager.get_colors()
        
        super().__init__(parent, bg=colors['bg'])
        
        # Estructura de datos para las memorias
        self.memory_sections = {
            'Registros Generales': {
                'items': [
                    ('R0', lambda: self.cpu_excel.read_r0(), 32),
                    ('R1', lambda: self.cpu_excel.read_r1(), 32),
                    ('R2', lambda: self.cpu_excel.read_r2(), 32),
                    ('R3', lambda: self.cpu_excel.read_r3(), 32),
                    ('R4', lambda: self.cpu_excel.read_r4(), 32),
                    ('R5', lambda: self.cpu_excel.read_r5(), 32),
                    ('R6', lambda: self.cpu_excel.read_r6(), 32),
                    ('R7', lambda: self.cpu_excel.read_r7(), 32),
                    ('R8', lambda: self.cpu_excel.read_r8(), 32),
                    ('R9', lambda: self.cpu_excel.read_r9(), 32),
                    ('R10', lambda: self.cpu_excel.read_r10(), 32),
                    ('R11', lambda: self.cpu_excel.read_r11(), 32),
                    ('R12', lambda: self.cpu_excel.read_r12(), 32),
                    ('R13', lambda: self.cpu_excel.read_r13(), 32),
                    ('R14', lambda: self.cpu_excel.read_r14(), 32),
                    ('R15', lambda: self.cpu_excel.read_r15(), 32),
                ],
                'labels': []
            },
            'Registros Seguros': {
                'items': [
                    ('W1', lambda: self.cpu_excel.read_w1(), 32),
                    ('W2', lambda: self.cpu_excel.read_w2(), 32),
                    ('W3', lambda: self.cpu_excel.read_w3(), 32),
                    ('W4', lambda: self.cpu_excel.read_w4(), 32),
                    ('W5', lambda: self.cpu_excel.read_w5(), 32),
                    ('W6', lambda: self.cpu_excel.read_w6(), 32),
                    ('W7', lambda: self.cpu_excel.read_w7(), 32),
                    ('W8', lambda: self.cpu_excel.read_w8(), 32),
                    ('W9', lambda: self.cpu_excel.read_w9(), 32),
                    ('D0_safe', lambda: self.cpu_excel.read_d0_safe(), 32),
                ],
                'labels': []
            },
            'Memoria de Contraseña': {
                'items': [
                    ('P1', lambda: self.cpu_excel.read_p1(), 32),
                    ('P2', lambda: self.cpu_excel.read_p2(), 32),
                    ('P3', lambda: self.cpu_excel.read_p3(), 32),
                    ('P4', lambda: self.cpu_excel.read_p4(), 32),
                    ('P5', lambda: self.cpu_excel.read_p5(), 32),
                    ('P6', lambda: self.cpu_excel.read_p6(), 32),
                    ('P7', lambda: self.cpu_excel.read_p7(), 32),
                    ('P8', lambda: self.cpu_excel.read_p8(), 32),
                ],
                'labels': []
            },
            'Memoria Criptográfica': {
                'items': [
                    ('K0[0]', lambda: self.cpu_excel.read_k0_0(), 32),
                    ('K0[1]', lambda: self.cpu_excel.read_k0_1(), 32),
                    ('K0[2]', lambda: self.cpu_excel.read_k0_2(), 32),
                    ('K0[3]', lambda: self.cpu_excel.read_k0_3(), 32),
                    ('K1[0]', lambda: self.cpu_excel.read_k1_0(), 32),
                    ('K1[1]', lambda: self.cpu_excel.read_k1_1(), 32),
                    ('K1[2]', lambda: self.cpu_excel.read_k1_2(), 32),
                    ('K1[3]', lambda: self.cpu_excel.read_k1_3(), 32),
                    ('K2[0]', lambda: self.cpu_excel.read_k2_0(), 32),
                    ('K2[1]', lambda: self.cpu_excel.read_k2_1(), 32),
                    ('K2[2]', lambda: self.cpu_excel.read_k2_2(), 32),
                    ('K2[3]', lambda: self.cpu_excel.read_k2_3(), 32),
                    ('K3[0]', lambda: self.cpu_excel.read_k3_0(), 32),
                    ('K3[1]', lambda: self.cpu_excel.read_k3_1(), 32),
                    ('K3[2]', lambda: self.cpu_excel.read_k3_2(), 32),
                    ('K3[3]', lambda: self.cpu_excel.read_k3_3(), 32),
                ],
                'labels': []
            },
            'Memoria General': {
                'items': [],  # Se llenará dinámicamente
                'labels': []
            }
        }
        
        self._create_ui()
        # Cargar valores iniciales
        self.update_all_memories()
    
    def _create_ui(self):
        """Crea la interfaz de la tabla de memorias"""
        colors = self.design_manager.get_colors()
        
        # Frame con scroll
        self.scroll_frame = ScrollableFrame(self, self.design_manager)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear secciones
        for section_name in self.memory_sections:
            self._create_section(self.scroll_frame.interior, section_name)
    
    def _create_section(self, parent, section_name):
        """Crea una sección de memoria con su tabla"""
        colors = self.design_manager.get_colors()
        
        # Frame de la sección
        section_frame = tk.LabelFrame(
            parent,
            text=section_name,
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
        headers = ['Memoria', 'Tipo', 'Tamaño', 'Valor']
        for col, header in enumerate(headers):
            label = tk.Label(
                table_frame,
                text=header,
                font=self.design_manager.get_font('bold'),
                bg=colors['sidebar_bg'],
                fg=colors['sidebar_button_fg'],
                padx=20,
                pady=8,
                relief=tk.RIDGE,
                borderwidth=1
            )
            label.grid(row=0, column=col, sticky='ew')
        
        # Configurar columnas
        table_frame.grid_columnconfigure(0, weight=1, minsize=150)
        table_frame.grid_columnconfigure(1, weight=1, minsize=100)
        table_frame.grid_columnconfigure(2, weight=1, minsize=100)
        table_frame.grid_columnconfigure(3, weight=2, minsize=200)
        
        # Si es memoria general, generarla dinámicamente
        if section_name == 'Memoria General':
            for i in range(64):
                addr = i * 4  # Cada bloque es de 4 bytes
                name = f'M[0x{addr:02X}]'
                # Usar read_memory_at_address con dirección hexadecimal
                read_func = lambda a=addr: self._read_memory_at_hex_address(a)
                self.memory_sections[section_name]['items'].append((name, read_func, 32))
        
        # Crear filas para cada item
        row_idx = 1
        for name, read_func, size_bits in self.memory_sections[section_name]['items']:
            # Celda de nombre
            name_label = tk.Label(
                table_frame,
                text=name,
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=20,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1
            )
            name_label.grid(row=row_idx, column=0, sticky='ew')
            
            # Celda de tipo
            type_label = tk.Label(
                table_frame,
                text='',
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=20,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1
            )
            type_label.grid(row=row_idx, column=1, sticky='ew')
            
            # Celda de tamaño
            size_label = tk.Label(
                table_frame,
                text=f'{size_bits} bits',
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=20,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1
            )
            size_label.grid(row=row_idx, column=2, sticky='ew')
            
            # Celda de valor
            value_label = tk.Label(
                table_frame,
                text='',
                font=self.design_manager.get_font('normal'),
                bg=colors['entry_bg'],
                fg=colors['entry_fg'],
                padx=20,
                pady=6,
                relief=tk.RIDGE,
                borderwidth=1,
                anchor='w'
            )
            value_label.grid(row=row_idx, column=3, sticky='ew')
            
            # Guardar referencias a las etiquetas
            self.memory_sections[section_name]['labels'].append({
                'name': name_label,
                'type': type_label,
                'size': size_label,
                'value': value_label,
                'read_func': read_func,
                'size_bits': size_bits
            })
            
            row_idx += 1
    
    def _read_memory_at_hex_address(self, addr_decimal):
        """Lee memoria usando read_memory_at_address con formato hex"""
        hex_addr = f"0x{addr_decimal:02X}"
        result = self.cpu_excel.read_memory_at_address(hex_addr)
        
        # Parsear el resultado para obtener el tipo y valor
        if result.startswith('0x'):
            return (DataType.HEX, int(result, 16))
        elif result.startswith('0b'):
            return (DataType.BINARY, int(result, 2))
        elif result.startswith('0d'):
            return (DataType.INT, int(result[2:]))
        else:
            return (DataType.INT, 0)
    
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
    
    def update_all_memories(self):
        """Actualiza todos los valores de memoria"""
        for section_name, section_data in self.memory_sections.items():
            for label_data in section_data['labels']:
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
                    
                    label_data['type']['text'] = type_str
                    
                    # Convertir valor al formato correcto
                    display_value = self._convert_value_to_format(
                        value, 
                        data_type, 
                        label_data['size_bits']
                    )
                    
                    # Actualizar valor
                    label_data['value']['text'] = display_value
                    
                    # Colorear según el valor
                    colors = self.design_manager.get_colors()
                    if value == 0 or value == "0":
                        # Valor cero - color normal
                        label_data['value']['fg'] = colors['entry_fg']
                    elif value is None:
                        # Valor vacío - color atenuado
                        label_data['value']['fg'] = colors['button_hover']
                    else:
                        # Valor no cero - resaltar
                        label_data['value']['fg'] = colors['sidebar_button_active_bg']
                        
                except Exception as e:
                    label_data['type']['text'] = "Error"
                    label_data['value']['text'] = str(e)
                    colors = self.design_manager.get_colors()
                    label_data['value']['fg'] = colors['select_bg']
    
    def update_theme(self):
        """Actualiza los colores cuando cambia el tema"""
        colors = self.design_manager.get_colors()
        self.configure(bg=colors['bg'])
        
        # Actualizar scroll frame
        if hasattr(self, 'scroll_frame'):
            self.scroll_frame.update_theme()
        
        # Actualizar todas las etiquetas
        for section_data in self.memory_sections.values():
            for label_data in section_data['labels']:
                # Actualizar colores de fondo y texto
                label_data['name'].configure(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg']
                )
                label_data['type'].configure(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg']
                )
                label_data['size'].configure(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg']
                )
                label_data['value'].configure(
                    bg=colors['entry_bg']
                )