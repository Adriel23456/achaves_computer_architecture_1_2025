# ExtraPrograms/Processor/PipeLine.py - VERSIÓN SEGURA
from ExtraPrograms.Processor.PrinterUnit import PrinterUnit

class Pipeline:
    def __init__(self, program_counter, instruction_memory,
                 register_file, safe_register_file,
                 data_memory, dynamic_memory, vault_memory, login_memory,
                 alu, flags, control_unit, cond_unit, extend, controller):
        
        # ─── Módulos principales ────────────────────────────
        self.pc = program_counter
        self.instruction_memory = instruction_memory
        self.register_file = register_file
        self.safe_register_file = safe_register_file
        self.data_memory = data_memory
        self.dynamic_memory = dynamic_memory
        self.vault_memory = vault_memory
        self.login_memory = login_memory
        self.alu = alu
        self.flags = flags
        self.control_unit = control_unit
        self.cond_unit = cond_unit
        self.extend = extend
        self.printer_unit = PrinterUnit(controller)

        # ─── Registros de etapa ─────────────────────────────
        self.if_id = None
        self.id_ex = None
        self.ex_mem = None
        self.mem_wb = None

        # ─── Buffers para el siguiente ciclo ────────────────
        self.next_if_id = None
        self.next_id_ex = None
        self.next_ex_mem = None
        self.next_mem_wb = None

        # ─── Ciclo de reloj y estadísticas ─────────────────
        self.clock_cycle = 0
        self.instructions_completed = 0

        self.flush_pipeline()

    def fetch(self):
        # No sobreescribimos si ya hay una instrucción pendiente en IF/ID
        if self.if_id is not None and self.next_if_id is not None:
            print("[STALL] FETCH detenido: IF/ID aún en uso.")
            return

        # Obtener dirección actual del Program Counter
        current_pc = self.pc.get_pc()

        # Leer la instrucción en esa dirección
        instruction = self.instruction_memory.read(current_pc)

        # Cargar valores al buffer del próximo ciclo
        self.next_if_id = {
            "pc": current_pc,
            "instruction": instruction
        }
        
    def decode(self):
        if self.if_id is None:
            return  # No hay instrucción para decodificar

        instr = self.if_id["instruction"]
        pc = self.if_id["pc"]

        # 1. Decodificar instrucción
        op = (instr >> 56) & 0xFF            # 8 bits
        special = (instr >> 52) & 0xF        # 4 bits
        rd = (instr >> 48) & 0xF             # 4 bits
        ar1 = (instr >> 44) & 0xF            # 4 bits
        ar2 = (instr >> 40) & 0xF            # 4 bits
        imm32 = (instr >> 8) & 0xFFFFFFFF    # 32 bits

        # 2. Generar señales de control
        self.control_unit.generate_signals(special, op)
        ctrl = self.control_unit
        
        # ── Señal externa L (solo este ciclo) ────────
        L_signal = 1 if ctrl.ComS else 0

        # 3. Leer registros (según señales)
        
        # ══════════════════════════════════════════════════════════
        # VERIFICACIÓN DE SEGURIDAD PREVIA
        # ══════════════════════════════════════════════════════════
        security_violation = False
        security_msg = ""
        
        # Verificar si se intenta acceder a recursos protegidos sin permisos
        if ctrl.RegisterInA == 0 and self.flags.enabled() != 1:
            # Intenta leer de registro seguro sin permisos
            security_violation = True
            security_msg = f"[SECURITY] Intento de leer registro seguro w{ar1} sin SafeFlags"
            
        if ctrl.RegisterInB in [0b01, 0b10] and self.flags.enabled() != 1:
            # RegisterInB = 01: SafeRegisterFile
            # RegisterInB = 10: VaultMemory
            security_violation = True
            if ctrl.RegisterInB == 0b01:
                security_msg = f"[SECURITY] Intento de leer registro seguro w{ar2} sin SafeFlags"
            else:
                security_msg = f"[SECURITY] Intento de leer VaultMemory[{ar2}] sin SafeFlags"
                
        if ctrl.RegisterInB == 0b11 and not (self.flags.enabled() == 1 or L_signal):
            # LoginMemory necesita SafeFlags O L
            security_violation = True
            security_msg = f"[SECURITY] Intento de leer LoginMemory[{ar2}] sin SafeFlags ni L"

        # ── Operando A ─────────────────────────────
        if ctrl.RegisterInA == 1:
            # Registro normal - siempre permitido
            A_intermedio, _ = self.register_file.read(ar1, 0)
        else:
            # Registro seguro - verificar permisos
            A_intermedio, _ = self.safe_register_file.read(ar1, 0)
            if A_intermedio == 0 and self.flags.enabled() != 1:
                print(f"[DECODE] Acceso bloqueado a registro seguro w{ar1}")

        # MUX para branch
        if ctrl.BranchE:
            A = pc
        else:
            A = A_intermedio

        # ── Operando B ─────────────────────────────
        src_b = ctrl.RegisterInB

        if src_b == 0b00:
            # Registro normal - siempre permitido
            _, B_intermedio = self.register_file.read(0, ar2)

        elif src_b == 0b01:
            # Registro seguro - verificar permisos
            _, B_intermedio = self.safe_register_file.read(0, ar2)
            if B_intermedio == 0 and self.flags.enabled() != 1:
                print(f"[DECODE] Acceso bloqueado a registro seguro w{ar2}")

        elif src_b == 0b10:
            # VaultMemory - verificar permisos
            B_intermedio = self.vault_memory.read(ar2)
            if B_intermedio == 0 and self.flags.enabled() != 1:
                print(f"[DECODE] Acceso bloqueado a VaultMemory[{ar2}]")

        elif src_b == 0b11:
            # LoginMemory - verificar permisos (SafeFlags O L)
            B_intermedio = self.login_memory.read(ar2, L_signal)
            if B_intermedio == 0 and not (self.flags.enabled() == 1 or L_signal):
                print(f"[DECODE] Acceso bloqueado a LoginMemory[{ar2}]")

        # MUX final: ImmediateOp decide si usar inmediato
        if ctrl.ImmediateOp:
            B = imm32
        else:
            B = B_intermedio

        # Intentos de escritura en memorias protegidas
        # VaultMemory: ignora si no hay permisos
        self.vault_memory.write(ar2, imm32, ctrl.MemWriteV)
        
        # LoginMemory: ignora si no hay permisos
        self.login_memory.write(ar2, imm32, ctrl.MemWriteP, L_signal)

        flags_nzcv = self.flags.as_nzcv()

        # 4. Guardar en next_id_ex
        self.next_id_ex = {
            "A": A,
            "B": B,
            "LoginInBlockD": ar2,
            "rd": rd,
            "Rd_Special": B_intermedio,
            "control_signals": {
                "LogOut": ctrl.LogOut,
                "ComS": ctrl.ComS,
                "PrintEn": ctrl.PrintEn,
                "RegWriteS": ctrl.RegWriteS,
                "RegWriteR": ctrl.RegWriteR,
                "MemOp": ctrl.MemOp,
                "MemWriteG": ctrl.MemWriteG,
                "MemWriteD": ctrl.MemWriteD,
                "MemByte": ctrl.MemByte,
                "PCSrc": ctrl.PCSrc,
                "FlagsUpd": ctrl.FlagsUpd,
                "BranchOp": ctrl.BranchOp,
                "ALUSrc": ctrl.ALUSrc,
            },
            "FlagsE": flags_nzcv,
            "opcode": op,
            "security_violation": security_violation,
            "security_msg": security_msg
        }
        
        # Log de seguridad si hubo violación
        if security_violation:
            print(security_msg)

    def execute(self):
        if not self.id_ex:
            return

        # Cargar info de etapa previa
        A = self.id_ex["A"]
        B = self.id_ex["B"]
        login_block_e = self.id_ex["LoginInBlockD"]
        ctrl = self.id_ex["control_signals"]

        # Verificar si hubo violación de seguridad
        if self.id_ex.get("security_violation", False):
            print(f"[EXECUTE] {self.id_ex.get('security_msg', 'Security violation')}")

        # Calcular carry_in desde FlagsE
        flags_e = self.id_ex["FlagsE"]
        carry_in = (flags_e >> 1) & 0b1

        # Ejecutar ALU
        result, alu_flags_out = self.alu.execute(ctrl["ALUSrc"], A, B, carry_in)
        nzcv = (alu_flags_out[0] << 3) | (alu_flags_out[1] << 2) | (alu_flags_out[2] << 1) | alu_flags_out[3]

        # CondUnit: evaluar condición
        self.cond_unit.generate_signals(
            ctrl["BranchOp"],
            ctrl["LogOut"],
            ctrl["ComS"],
            login_block_e,
            ctrl["FlagsUpd"],
            nzcv,
            flags_e,
        )
        
        # Calcular PCSrc modificado
        pcsrc_m = ctrl["PCSrc"] & self.cond_unit.CondExE

        # Pasar señales a MEM
        control_signals = {
            "RegWriteS": ctrl["RegWriteS"],
            "RegWriteR": ctrl["RegWriteR"],
            "MemOp": ctrl["MemOp"],
            "MemWriteG": ctrl["MemWriteG"],
            "MemWriteD": ctrl["MemWriteD"],
            "MemByte": ctrl["MemByte"],
            "PCSrc": pcsrc_m,
            "PrintEn": ctrl["PrintEn"],
        }

        self.next_ex_mem = {
            "ALUOut": result,
            "rd": self.id_ex["rd"],
            "control_signals": control_signals,
            "Rd_Special": self.id_ex["Rd_Special"],
        }

        # Flags para depuración
        n, z, c, v = alu_flags_out
        if (self.id_ex.get("opcode") == 0x2F):    
            self.halt_requested = True

    def mem(self):
        if not self.ex_mem:
            return

        alu_out_ex = self.ex_mem["ALUOut"]
        rd = self.ex_mem["rd"]
        rd_special = self.ex_mem["Rd_Special"]
        ctrl = self.ex_mem["control_signals"]

        # Operación de memoria
        alu_out = None
        if ctrl["MemOp"] == 0b00:  # LOAD de memoria general
            alu_out = self.data_memory.read(alu_out_ex)
        elif ctrl["MemOp"] == 0b01:  # LOAD de memoria dinámica
            # CRÍTICO: La memoria dinámica retornará 0 si no hay permisos
            alu_out = self.dynamic_memory.read(alu_out_ex)
            if alu_out == 0 and self.flags.enabled() != 1:
                print(f"[MEM] Lectura de memoria dinámica bloqueada por falta de SafeFlags")
        elif ctrl["MemOp"] == 0b10:
            print("No se espera recibir un MemOP de 10")

        # Preparar datos para escritura
        WD_G = 0
        if ctrl["MemByte"]:
            WD_G = self.extend.uxtb_32_to_32(rd_special)
        else:
            WD_G = rd_special
        self.data_memory.write(alu_out_ex, WD_G, ctrl["MemWriteG"])

        # Escritura en memoria dinámica (se bloqueará si no hay permisos)
        WD_D = 0
        if ctrl["MemByte"]:
            WD_D = self.extend.uxtb_32_to_32(rd_special)
        else:
            WD_D = rd_special
        self.dynamic_memory.write(alu_out_ex, WD_D, ctrl["MemWriteD"])

        control_signals = {
            "RegWriteS": ctrl["RegWriteS"],
            "RegWriteR": ctrl["RegWriteR"],
            "MemByte": ctrl["MemByte"],
            "PCSrc": ctrl["PCSrc"],
            "PrintEn": ctrl["PrintEn"],
        }
        val_wb = alu_out if alu_out is not None else alu_out_ex

        self.next_mem_wb = {
            "ALUOut": val_wb,
            "rd": rd,
            "control_signals": control_signals,
        }

    def writeback(self):
        if not self.mem_wb:
            return

        alu_out = self.mem_wb["ALUOut"]
        rd = self.mem_wb["rd"]
        ctrl = self.mem_wb["control_signals"]

        if ctrl["MemByte"]:
            alu_out = self.extend.uxtb_32_to_32(alu_out)

        # Escritura en registros
        self.register_file.write(rd, alu_out, ctrl["RegWriteR"])
        # CRÍTICO: La escritura en registro seguro se bloqueará si no hay permisos
        self.safe_register_file.write(rd, alu_out, ctrl["RegWriteS"])

        # Impresión si corresponde
        if ctrl["PrintEn"] == 0b00:
            self.printer_unit.print_integer(alu_out)
        elif ctrl["PrintEn"] == 0b01:
            self.printer_unit.print_ascii(alu_out)
        elif ctrl["PrintEn"] == 0b10:
            self.printer_unit.print_binary(alu_out)

        # Si corresponde salto condicional, actualizar PC
        self.pc.result_w = alu_out
        self.pc.pcsrc_w = ctrl["PCSrc"]

    def step(self):
        # 1. Ejecutar etapas del ciclo actual
        self.writeback()
        self.mem()
        self.execute()
        self.decode()
        self.fetch()

        # 2. Aplicar avance de registros entre etapas
        self.if_id = self.next_if_id
        self.id_ex = self.next_id_ex
        self.ex_mem = self.next_ex_mem
        self.mem_wb = self.next_mem_wb

        self.next_if_id = None
        self.next_id_ex = None
        self.next_ex_mem = None
        self.next_mem_wb = None

        # 3. Flanco de reloj para módulos sincronizados
        self.pc.tick()
        self.register_file.tick()
        self.safe_register_file.tick()
        self.vault_memory.tick()
        self.login_memory.tick()
        self.data_memory.tick()
        self.dynamic_memory.tick()

        # 4. Verificar salto condicional después del tick
        branch_taken = bool(self.pc.pcsrc_w)
        if branch_taken:
            self.if_id = None
            self.id_ex = None
            self.next_if_id = None

        # 5. Actualizar contador de ciclos
        self.clock_cycle += 1
        
        # 6. Halt por SWI
        if getattr(self, "halt_requested", False):
            self.if_id = self.id_ex = self.ex_mem = self.mem_wb = None
            self.next_if_id = self.next_id_ex = self.next_ex_mem = self.next_mem_wb = None

    def flush_pipeline(self):
        self.if_id = None
        self.id_ex = None
        self.ex_mem = None
        self.mem_wb = None
        