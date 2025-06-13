# GUI/Views/cpu.py ─ Vista del CPU con diagrama interactivo
import time
from pathlib import Path, PurePath
import tkinter as tk
from GUI.Components.styled_button      import StyledButton
from GUI.Components.memory_table_view  import MemoryTableView
from GUI.Components.signals_table_view import SignalsTableView
import struct
from ExtraPrograms.Processor.Implementation.Processor import Procesador
from ExtraPrograms.Processor.Security_Control.AuthenticationUnit import AuthenticationProcess

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
        #Paso 0: Asegurar la existencia de memoria de instrucciones y archivo de instrucciones
        current_file = self.controller.get_current_file() #Archivo de las instrucciones en crudo
        instruction_mem_path = Path(self.base_dir) / "Assets" / "instruction_mem.bin"
        if not current_file or not Path(current_file).exists() or not instruction_mem_path.exists():
            self.controller.print_console(
                "[ERROR] Fallo en la detección de memoria de instrucción o archivo de instrucciones")
            return
        
        # Lista limpia de instrucciones fuente (líneas no vacías, sin \n)
        try:
            with open(current_file, encoding="utf-8") as f:
                all_lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        except Exception as e:
            self.controller.print_console(f"[ERROR] No se pudo leer el archivo de instrucciones: {e}")
            return
        # Filtramos las etiquetas (líneas que empiezan con '.')
        instructions = [ln for ln in all_lines if not ln.startswith('.')]
        
        # Paso 1  ▸ Avanzar el pipeline una etapa
        _, fetch_prev   = self.cpu_excel.read_state_fetch()
        self.cpu_excel.write_state_decode(fetch_prev)
        _, decode_prev  = self.cpu_excel.read_state_decode()
        self.cpu_excel.write_state_execute(decode_prev)
        _, exec_prev    = self.cpu_excel.read_state_execute()
        self.cpu_excel.write_state_memory(exec_prev)
        _, mem_prev     = self.cpu_excel.read_state_memory()
        self.cpu_excel.write_state_writeBack(mem_prev)
        
        # Calcular la nueva instruccion del Fetch
        _, pcf_raw = self.cpu_excel.read_pcf()
        # Normalizar a entero sin signo
        try:
            if isinstance(pcf_raw, int):
                pcf_val = pcf_raw & 0xFFFFFFFF
            else:
                pcf_val = int(str(pcf_raw), 0) & 0xFFFFFFFF
        except Exception:
            pcf_val = 0
        line_idx   = pcf_val // 8
        fetch_value = instructions[line_idx] if 0 <= line_idx < len(instructions) else "NOP"
        self.cpu_excel.write_state_fetch(fetch_value)

        self.cpu_excel.table.execute_all()
    
        #Paso 2: Cargar memorias y señales, desde el excel, al ejecutador
        self._load_from_excel_to_executor()
        
        #Paso 3: Ejecutar SOLO 1 ciclo, pero si es un SWI en writeback entonces no hacer nada!
        if hasattr(self, 'cpu_instance'):
            # Verificar si hay SWI en writeback
            _, wb_instr = self.cpu_excel.read_state_writeBack()
            if wb_instr and "SWI" not in str(wb_instr):
                self.cpu_instance.pipeline.step()
            else:
                self.controller.print_console("[CPU] SWI detectado en WriteBack, ciclo omitido")
        
        #Paso 4: Cargar todas las señales y memorias de vuelta al excel
        self._save_from_executor_to_excel()
        
        #Paso 5:Actualizar diagrama, memorias y señales
        self.diagram.update_signals()
        self._load_initial_values()
        self.controller.print_console("[CPU] Se ejecutó un ciclo")
    
    def _on_execute_all(self):
        """Maneja el evento de ejecutar todo"""
        #Paso 0: Asegurar la existencia de memoria de instrucciones y archivo de instrucciones
        from pathlib import Path, PurePath
        start_time = time.time()
        current_file = self.controller.get_current_file() #Archivo de las instrucciones en crudo
        instruction_mem_path = Path(self.base_dir) / "Assets" / "instruction_mem.bin"
        if not current_file or not Path(current_file).exists() or not instruction_mem_path.exists():
            self.controller.print_console(
                "[ERROR] Fallo en la detección de memoria de instrucción o archivo de instrucciones")
            return
        
        # Lista limpia de instrucciones fuente (líneas no vacías, sin \n)
        try:
            with open(current_file, encoding="utf-8") as f:
                instructions_src = [ln.strip() for ln in f.readlines() if ln.strip()]
        except Exception as e:
            self.controller.print_console(f"[ERROR] No se pudo leer el archivo de instrucciones: {e}")
            return
        
        #Paso 1: Cargar memorias y señales, desde el excel, al ejecutador
        self._load_from_excel_to_executor()
        
        #Paso 2: Ejecutar hasta que no existan mas instrucciones o sea, si es un SWI en writeback entonces no hacer nada!
        if hasattr(self, 'cpu_instance'):
            max_cycles = 1000
            for cycle in range(max_cycles):
                # Verificar si hay SWI en alguna etapa
                has_swi = False
                for state_reader in ['read_state_fetch', 'read_state_decode', 
                                'read_state_execute', 'read_state_memory', 
                                'read_state_writeBack']:
                    _, instr = getattr(self.cpu_excel, state_reader)()
                    if instr and "SWI" in str(instr):
                        has_swi = True
                        break
                
                if has_swi:
                    self.controller.print_console("[CPU] SWI detectado, deteniendo ejecución")
                    break
                    
                # Ejecutar un ciclo del procesador
                self.cpu_instance.pipeline.step()
                
                # Verificar si el pipeline está vacío
                pipeline = self.cpu_instance.pipeline
                if all(stage is None for stage in (
                    pipeline.if_id, pipeline.id_ex, 
                    pipeline.ex_mem, pipeline.mem_wb
                )):
                    self.controller.print_console("[CPU] Pipeline vacío, ejecución completa")
                    break
        
        #Paso 3: Cargar todas las señales y memorias de vuelta al excel
        self._save_from_executor_to_excel()
        
        #Paso 4:Actualizar cual seria la ultima posicion del pipeline
        self.cpu_excel.write_state_fetch('NOP')
        self.cpu_excel.write_state_decode('NOP')
        self.cpu_excel.write_state_execute('NOP')
        self.cpu_excel.write_state_memory('NOP')
        self.cpu_excel.write_state_writeBack('NOP')
        self.cpu_excel.table.execute_all()
        
        #Paso 4:Actualizar diagrama, memorias y señales
        self.diagram.update_signals()
        self._load_initial_values()
        self.controller.print_console("[CPU] Se ejecutó todo el programa restante")
        elapsed = time.time() - start_time
        self.controller.print_console(f"[TIMER] Ejecución duró {elapsed:.3f} segundos")
        
    def _parse_excel_value(self, data_type, value):
        """
        Convierte valores del Excel al formato esperado por el procesador.
        
        Args:
            data_type: Tipo de dato retornado por Excel (DataType enum)
            value: Valor leído del Excel
            
        Returns:
            int: Valor convertido a entero de 32/64 bits según corresponda
        """
        if value is None:
            return 0
            
        # Si ya es entero, usarlo directamente
        if isinstance(value, int):
            return value & 0xFFFFFFFF  # Asegurar 32 bits
        
        # Si es string, convertir según formato
        if isinstance(value, str):
            value = value.strip()
            if value.startswith('0x'):
                return int(value, 16) & 0xFFFFFFFF
            elif value.startswith('0b'):
                return int(value, 2) & 0xFFFFFFFF
            elif value.startswith('0d'):
                return int(value[2:]) & 0xFFFFFFFF
            else:
                # Intentar como decimal
                try:
                    return int(value) & 0xFFFFFFFF
                except:
                    return 0
        
        return 0

    def _extract_bit_field(self, value, start_bit, num_bits):
        """Extrae un campo de bits de un valor."""
        mask = (1 << num_bits) - 1
        return (value >> start_bit) & mask

    def _load_from_excel_to_executor(self):
        """
        Carga todo el estado desde Excel al procesador.
        Este es el PASO 2 de la ejecución del ciclo.
        """
        try:
            # Verificar que tengamos el procesador
            if not hasattr(self, 'cpu_instance'):
                # Crear instancia del procesador si no existe
                self.cpu_instance = Procesador()
                self.controller.print_console("[CPU] Procesador inicializado")
            
            cpu = self.cpu_instance
            
            # ═══════════════════════════════════════════════════════════════
            # 1. CARGAR REGISTROS GENERALES (R0-R15)
            # ═══════════════════════════════════════════════════════════════
            for i in range(16):
                method_name = f'read_r{i}'
                if hasattr(self.cpu_excel, method_name):
                    data_type, value = getattr(self.cpu_excel, method_name)()
                    reg_value = self._parse_excel_value(data_type, value)
                    cpu.register_file.regs[i] = reg_value
                    
            # ═══════════════════════════════════════════════════════════════
            # 2. CARGAR REGISTROS SEGUROS (W1-W9, D0)
            # ═══════════════════════════════════════════════════════════════
            for i in range(1, 10):
                method_name = f'read_w{i}'
                if hasattr(self.cpu_excel, method_name):
                    data_type, value = getattr(self.cpu_excel, method_name)()
                    reg_value = self._parse_excel_value(data_type, value)
                    cpu.safe_register_file._regs[i-1] = reg_value
                    
            # D0 (constante TEA)
            data_type, value = self.cpu_excel.read_d0_safe()
            cpu.safe_register_file._regs[9] = self._parse_excel_value(data_type, value)
            
            # ═══════════════════════════════════════════════════════════════
            # 3. CARGAR LLAVES CRIPTOGRÁFICAS (Vault Memory)
            # ═══════════════════════════════════════════════════════════════
            for key_idx in range(4):
                for block_idx in range(4):
                    method_name = f'read_k{key_idx}_{block_idx}'
                    if hasattr(self.cpu_excel, method_name):
                        data_type, value = getattr(self.cpu_excel, method_name)()
                        vault_value = self._parse_excel_value(data_type, value)
                        mem_idx = key_idx * 4 + block_idx
                        cpu.vault_memory._mem[mem_idx] = vault_value
            
            # ═══════════════════════════════════════════════════════════════
            # 4. CARGAR BLOQUES DE CONTRASEÑA (Login Memory)
            # ═══════════════════════════════════════════════════════════════
            for i in range(1, 9):
                method_name = f'read_p{i}'
                if hasattr(self.cpu_excel, method_name):
                    data_type, value = getattr(self.cpu_excel, method_name)()
                    login_value = self._parse_excel_value(data_type, value)
                    # IMPORTANTE: P1 va en índice 0, P2 en índice 1, etc.
                    cpu.login_memory._mem[i-1] = login_value
                    # Debug opcional
                    self.controller.print_console(f"[LOAD] P{i} → LoginMem[{i-1}] = {login_value}")
            
            # ═══════════════════════════════════════════════════════════════
            # 5. CARGAR MEMORIA GENERAL (64 bloques)
            # ═══════════════════════════════════════════════════════════════
            for i in range(64):
                mem_value = self.cpu_excel.read_memory_block(i)
                cpu.data_memory._mem[i] = mem_value & 0xFFFFFFFF
            
            # ═══════════════════════════════════════════════════════════════
            # 6. CARGAR SEÑALES DEL PIPELINE
            # ═══════════════════════════════════════════════════════════════
            
            # Program Counter
            data_type, value = self.cpu_excel.read_pcf()
            pcf_value = self._parse_excel_value(data_type, value)
            cpu.pc._pc = pcf_value
            
            # Flags (NZCV)
            data_type, value = self.cpu_excel.read_flagse()
            flags_value = self._parse_excel_value(data_type, value)
            if isinstance(flags_value, int):
                cpu.flags.N = (flags_value >> 3) & 1
                cpu.flags.Z = (flags_value >> 2) & 1
                cpu.flags.C = (flags_value >> 1) & 1
                cpu.flags.V = flags_value & 1
            
            # SafeFlags (S1, S2)
            data_type, value = self.cpu_excel.read_safeflagsout()
            safe_flags = self._parse_excel_value(data_type, value)
            if isinstance(safe_flags, int):
                cpu.flags.S1 = (safe_flags >> 1) & 1
                cpu.flags.S2 = safe_flags & 1
            
            # ═══════════════════════════════════════════════════════════════
            # 7. CARGAR ESTADO DE AUTENTICACIÓN
            # ═══════════════════════════════════════════════════════════════
            auth = cpu.cond_unit.auth_process
            
            # Timer
            data_type, value = self.cpu_excel.read_timer_safe()
            timer_value = self._parse_excel_value(data_type, value)
            # El timer se manejará internamente en AuthenticationProcess
            
            # Block Status
            data_type, value = self.cpu_excel.read_block_statusOut()
            block_status = self._parse_excel_value(data_type, value)
            auth.set_block_states(block_status & 0xFF)
            
            # Intentos disponibles
            data_type, value = self.cpu_excel.read_attempts_available()
            attempts = self._parse_excel_value(data_type, value)
            auth.try_counter = attempts & 0xF
            
            # ═══════════════════════════════════════════════════════════════
            # 8. CARGAR MEMORIAS DINÁMICAS (desde archivos .bin)
            # ═══════════════════════════════════════════════════════════════
            
            # Memoria dinámica
            dynamic_mem_path = Path(self.base_dir) / "Assets" / "dynamic_mem.bin"
            if dynamic_mem_path.exists():
                with open(dynamic_mem_path, 'rb') as f:
                    data = f.read()
                    # Cargar en bloques de 64 bits (8 bytes)
                    for i in range(0, min(len(data), 512), 8):  # Max 64 bloques x 8 bytes
                        if i + 8 <= len(data):
                            block_data = struct.unpack('<Q', data[i:i+8])[0]
                            cpu.dynamic_memory._mem[i//8] = block_data
            
            # Memoria de instrucciones
            instruction_mem_path = Path(self.base_dir) / "Assets" / "instruction_mem.bin"
            if instruction_mem_path.exists():
                instructions = self._bin_to_prog_list(str(instruction_mem_path))
                cpu.instruction_memory.load(instructions, start_addr=0)
            
            self.controller.print_console("[CPU] Estado cargado desde Excel al procesador")
            
        except Exception as e:
            self.controller.print_console(f"[ERROR] Error cargando estado: {e}")
            import traceback
            traceback.print_exc()

    def _bin_to_prog_list(self, bin_path: str):
        """Convierte archivo binario a lista de instrucciones de 64 bits."""
        data = Path(bin_path).read_bytes()
        if len(data) % 8:
            raise ValueError("El archivo no tiene múltiplos de 8 bytes.")
        
        words = []
        for i in range(0, len(data), 8):
            word = struct.unpack(">Q", data[i:i+8])[0]  # 64-bit big-endian
            words.append(word)
        return words

    def _save_from_executor_to_excel(self):
        """
        Guarda todo el estado desde el procesador al Excel.
        Este es el PASO 4 de la ejecución del ciclo.
        """
        try:
            if not hasattr(self, 'cpu_instance'):
                self.controller.print_console("[ERROR] No hay procesador activo")
                return
                
            cpu = self.cpu_instance
            
            # ═══════════════════════════════════════════════════════════════
            # 1. GUARDAR REGISTROS GENERALES
            # ═══════════════════════════════════════════════════════════════
            for i in range(16):
                method_name = f'write_r{i}'
                if hasattr(self.cpu_excel, method_name):
                    value = cpu.register_file.regs[i]
                    getattr(self.cpu_excel, method_name)(f"0x{value:08X}")
            
            # ═══════════════════════════════════════════════════════════════
            # 2. GUARDAR REGISTROS SEGUROS
            # ═══════════════════════════════════════════════════════════════
            for i in range(1, 10):
                method_name = f'write_w{i}'
                if hasattr(self.cpu_excel, method_name):
                    value = cpu.safe_register_file._regs[i-1]
                    getattr(self.cpu_excel, method_name)(f"0x{value:08X}")
            
            # ═══════════════════════════════════════════════════════════════
            # 3. GUARDAR MEMORIA GENERAL
            # ═══════════════════════════════════════════════════════════════
            for i in range(64):
                value = cpu.data_memory._mem[i]
                self.cpu_excel.write_memory_block(i, value, "hex")
            
            # ═══════════════════════════════════════════════════════════════
            # 4. GUARDAR FLAGS Y ESTADOS
            # ═══════════════════════════════════════════════════════════════
            
            # Program Counter
            self.cpu_excel.write_pcf(f"0x{cpu.pc._pc:08X}")
            
            # Flags NZCV
            flags_value = (cpu.flags.N << 3) | (cpu.flags.Z << 2) | (cpu.flags.C << 1) | cpu.flags.V
            self.cpu_excel.write_flagse(f"0b{flags_value:04b}")
            
            # SafeFlags
            safe_flags = (cpu.flags.S1 << 1) | cpu.flags.S2
            self.cpu_excel.write_safeflagsout(f"0b{safe_flags:02b}")
            
            # Authentication state
            auth = cpu.cond_unit.auth_process
            self.cpu_excel.write_block_statusOut(f"0b{auth.get_block_states():08b}")
            self.cpu_excel.write_attempts_available(f"0b{auth.try_counter:04b}")
            
            # Ejecutar todas las escrituras pendientes
            self.cpu_excel.table.execute_all()
            
            # ═══════════════════════════════════════════════════════════════
            # 5. GUARDAR MEMORIAS DINÁMICAS
            # ═══════════════════════════════════════════════════════════════
            
            # Guardar memoria dinámica
            dynamic_mem_path = Path(self.base_dir) / "Assets" / "dynamic_mem.bin"
            with open(dynamic_mem_path, 'wb') as f:
                for block in cpu.dynamic_memory._mem:
                    f.write(struct.pack('<Q', block & 0xFFFFFFFFFFFFFFFF))
            
            self.controller.print_console("[CPU] Estado guardado del procesador al Excel")
            
        except Exception as e:
            self.controller.print_console(f"[ERROR] Error guardando estado: {e}")
    
    def _debug_authentication_state(self):
        """Función auxiliar para depurar el estado de autenticación"""
        if not hasattr(self, 'cpu_instance'):
            return
        
        cpu = self.cpu_instance
        self.controller.print_console("\n[DEBUG] Estado de Autenticación:")
        
        # Mostrar registros R1-R8
        for i in range(1, 9):
            val = cpu.register_file.regs[i]
            self.controller.print_console(f"  R{i} = 0x{val:08X} ({val})")
        
        # Mostrar contenido de LoginMemory (P1-P8)
        self.controller.print_console("\n[DEBUG] LoginMemory (Contraseñas):")
        for i in range(8):
            try:
                # Necesitamos L=1 para leer sin S1/S2
                val = cpu.login_memory._mem[i]  # Acceso directo para debug
                self.controller.print_console(f"  P{i+1} (índice {i}) = 0x{val:08X} ({val})")
            except:
                pass
        
        # Mostrar flags
        flags = cpu.flags
        self.controller.print_console(f"\n[DEBUG] Flags: N={flags.N} Z={flags.Z} C={flags.C} V={flags.V}")
        self.controller.print_console(f"[DEBUG] SafeFlags: S1={flags.S1} S2={flags.S2}")
        
        # Mostrar estado de autenticación
        auth = cpu.cond_unit.auth_process
        self.controller.print_console(f"[DEBUG] Intentos: {auth.try_counter}/15")
        self.controller.print_console(f"[DEBUG] Bloques validados: {bin(auth.get_block_states())}")