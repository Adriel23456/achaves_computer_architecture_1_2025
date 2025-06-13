from PrinterUnit import PrinterUnit  # si está en otro archivo

class Pipeline:
    def __init__(self, program_counter, instruction_memory,
                 register_file, safe_register_file,
                 data_memory, dynamic_memory, vault_memory, login_memory,
                 alu, flags, control_unit, cond_unit, extend):
        
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

        # Leer la instrucción en esa dirección (InstructionMemory debe manejar PC en bytes)
        instruction = self.instruction_memory.read(current_pc)

        # Cargar valores al buffer del próximo ciclo
        self.next_if_id = {
            "pc": current_pc,
            "instruction": instruction
        }

        # Mensaje de depuración
        print(f"FETCH | PC: 0x{current_pc:08X} | Instruction: {instruction:064b}")
        
    def decode(self):
        if self.if_id is None:
            return  # No hay instrucción para decodificar

        instr = self.if_id["instruction"]
        pc = self.if_id["pc"]

        # 1. Decodificar instrucción (tus bits deben extraerse aquí)
        # 63:56 — Opcode
        op = (instr >> 56) & 0xFF            # 8 bits

        # 55:52 — Campo "special"
        special = (instr >> 52) & 0xF        # 4 bits

        # 51:48 — Registro destino
        rd = (instr >> 48) & 0xF             # 4 bits

        # 47:44 — Registro fuente A
        ar1 = (instr >> 44) & 0xF            # 4 bits

        # 43:40 — Registro fuente B
        ar2 = (instr >> 40) & 0xF            # 4 bits

        # 39:8 — Campo inmediato de 32 bits
        imm32 = (instr >> 8) & 0xFFFFFFFF    # 32 bits

        # 2. Generar señales de control
        self.control_unit.generate_signals(special, op)

        ctrl = self.control_unit  # atajo para escribir menos
        # ── Señal externa L (solo este ciclo) ────────
        L_signal = 1 if ctrl.ComS else 0


        # 3. Leer registros (según señales)

        # ── Operando A ─────────────────────────────
        if ctrl.RegisterInA == 1:
            A_intermedio, _ = self.register_file.read(ar1, 0)
        else:
            A_intermedio, _ = self.safe_register_file.read(ar1, 0)

        # Luego: si BranchE está activo, se usa PCF_D en lugar de RD1
        if ctrl.BranchE:
            A = pc  # ← MUX que selecciona PCF_D
        else:
            A = A_intermedio

        # ── Operando B ─────────────────────────────
        src_b = ctrl.RegisterInB  # valor de 2 bits

        # B_intermedio: resultado del MUX RegisterInB
        if src_b == 0b00:
            _, B_intermedio = self.register_file.read(0, ar2)

        elif src_b == 0b01:
            _, B_intermedio = self.safe_register_file.read(0, ar2)

        elif src_b == 0b10:                # VaultMemory
            try:
                B_intermedio = self.vault_memory.read(ar2)
            except PermissionError as e:
                print(f"[DECODE] Acceso bloqueado a Vault: {e}")
                raise

        elif src_b == 0b11:                # LoginMemory
            try:
                B_intermedio = self.login_memory.read(ar2, L_signal)
            except PermissionError as e:
                print(f"[DECODE] Acceso bloqueado a LoginMem: {e}")
                raise
        else:
            B_intermedio = 0         

        # MUX final: ImmediateOp decide si usar inmediato directamente
        if ctrl.ImmediateOp:
            B = imm32
        else:
            B = B_intermedio

        # VaultMemory: ignora `k` (por compatibilidad), guarda `data` si `we` = 1
        self.vault_memory.write(ar2, imm32, ctrl.MemWriteV)

        # LoginMemory: guarda WD (inmediato) en la posición A si WE = 1
        self.login_memory.write(ar2, imm32, ctrl.MemWriteP, L_signal)

        flags_nzcv = self.flags.as_nzcv()

        # 4. Guardar en next_id_ex
        self.next_id_ex = {
            "A": A,
            "B": B,
            "LoginInBlockD": ar2,
            "rd": rd,
            "Rd_Special" : B_intermedio,
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

        }
        print(f"ID : instr=0x{instr:016X}  op={op:02X} sp={special:01X} rd={rd} ar1={ar1} ar2={ar2} imm={imm32:#010X}")

    def execute(self):
        if not self.id_ex:
            return

        # === Cargar info de etapa previa ===
        A = self.id_ex["A"]
        B = self.id_ex["B"]
        login_block_e = self.id_ex["LoginInBlockD"]
        ctrl = self.id_ex["control_signals"]

        # === Calcular carry_in desde FlagsE (6 bits: NZCVSS) ===
        flags_e  = self.id_ex["FlagsE"]
        print(f"[EXEC]  FlagsE_in  = {flags_e:04b}")   
        carry_in = (flags_e >> 1) & 0b1  # bit 1 = Carry

        # === Ejecutar ALU ===
        result, alu_flags_out = self.alu.execute(ctrl["ALUSrc"], A, B, carry_in)

        nzcv = (alu_flags_out[0] << 3) | (alu_flags_out[1] << 2) | (alu_flags_out[2] << 1) | alu_flags_out[3]


        # === CondUnit: evaluar condición de ejecución segura ===
        self.cond_unit.generate_signals(
            ctrl["BranchOp"],
            ctrl["LogOut"],
            ctrl["ComS"],
            login_block_e,
            ctrl["FlagsUpd"],
            nzcv,
            flags_e,
        )
        print(f"[EXEC]  Flags'     = {self.flags.as_nzcv():04b}")
        # === Calcular PCSrc modificado ===
        pcsrc_m = ctrl["PCSrc"] & self.cond_unit.CondExE

        # === Solo pasar señales relevantes a MEM stage ===
        control_signals = {                    # nombres originales
            "RegWriteS": ctrl["RegWriteS"],
            "RegWriteR": ctrl["RegWriteR"],
            "MemOp":     ctrl["MemOp"],
            "MemWriteG": ctrl["MemWriteG"],
            "MemWriteD": ctrl["MemWriteD"],
            "MemByte":   ctrl["MemByte"],
            "PCSrc":     pcsrc_m,
            "PrintEn":   ctrl["PrintEn"],
        }

        # === Guardar resultado para MEM stage ===
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
        print(f"EX  | ALUOut={result:#010X} | Flags[NZCV]={n}{z}{c}{v}")
        print(f"[ALU] code={ctrl["ALUSrc"]:06b} A={A:08X} B={B:08X} => {result:08X} NZCV={alu_flags_out}")

    def mem(self):
        if not self.ex_mem:
            return

        alu_out_ex = self.ex_mem["ALUOut"]
        rd = self.ex_mem["rd"]
        rd_special = self.ex_mem["Rd_Special"]
        ctrl = self.ex_mem["control_signals"]

        # ==== Operación de memoria si corresponde ====
        alu_out = None
        if ctrl["MemOp"] == 0b00:  # LOAD de memoria general
            alu_out = self.data_memory.read(alu_out_ex)
        elif ctrl["MemOp"] == 0b01:  # LOAD de memoria dinámica
            alu_out = self.dynamic_memory.read(alu_out_ex)
        elif ctrl["MemOp"] == 0b10:
            print("No se espera recibir un MemOP de 10")

        WD_G = 0
        if ctrl["MemByte"]:
            WD_G = self.extend.uxtb_32_to_32(rd_special)
        else:
            WD_G = rd_special
        self.data_memory.write(alu_out_ex, WD_G, ctrl["MemWriteG"])

        WD_D = 0
        if ctrl["MemByte"]:
            WD_D = self.extend.uxtb_32_to_32(rd_special)
        else:
            WD_D = rd_special
        self.dynamic_memory.write(alu_out_ex, WD_D, ctrl["MemWriteD"])


        control_signals = {                    # nombres originales
            "RegWriteS": ctrl["RegWriteS"],
            "RegWriteR": ctrl["RegWriteR"],
            "MemByte":   ctrl["MemByte"],
            "PCSrc":     ctrl["PCSrc"],
            "PrintEn":   ctrl["PrintEn"],
        }
        val_wb = alu_out if alu_out is not None else alu_out_ex

        # ==== Guardar resultado para WB ====
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

        # === Escritura en registro destino ===
        self.register_file.write(rd, alu_out, ctrl["RegWriteR"])
        self.safe_register_file.write(rd, alu_out, ctrl["RegWriteS"])

        # === Impresión si corresponde ===
        if ctrl["PrintEn"] == 0b00:
            PrinterUnit.print_integer(alu_out)
        elif ctrl["PrintEn"] == 0b01:
            PrinterUnit.print_ascii(alu_out)
        elif ctrl["PrintEn"] == 0b10:
            PrinterUnit.print_binary(alu_out)

        # === Si corresponde salto condicional, actualizar PC ===
        self.pc.result_w = alu_out           # dirección calculada en EX/MEM
        self.pc.pcsrc_w = ctrl["PCSrc"]  # ya AND-eado con CondExE
        print(f"WB | rd={rd} <- {alu_out:#X}")

    def step(self):
        # === 1. Ejecutar etapas del ciclo actual ===
        self.writeback()
        self.mem()
        self.execute()
        self.decode()
        self.fetch()

        # === 2. Aplicar avance de registros entre etapas ===
        self.if_id = self.next_if_id
        self.id_ex = self.next_id_ex
        self.ex_mem = self.next_ex_mem
        self.mem_wb = self.next_mem_wb

        self.next_if_id = None
        self.next_id_ex = None
        self.next_ex_mem = None
        self.next_mem_wb = None

        # === 3. Flanco de reloj para módulos sincronizados ===
        self.pc.tick()
        self.register_file.tick()
        self.safe_register_file.tick()
        self.vault_memory.tick()
        self.login_memory.tick()
        self.data_memory.tick()
        self.dynamic_memory.tick()

        # === 4. Verificar salto condicional después del tick ===
        branch_taken = bool(self.pc.pcsrc_w)
        if branch_taken:
            self.if_id = None
            self.id_ex = None
            self.next_if_id = None  # ← también este, para evitar fetch basura

        # === 5. Actualizar contador de ciclos ===
        self.clock_cycle += 1
        # 6. Halt por SWI
        if getattr(self, "halt_requested", False):
            print("### SWI: ejecución detenida ###")
            # Vaciar registros para que run_all detecte pipeline vacío
            self.if_id = self.id_ex = self.ex_mem = self.mem_wb = None
            self.next_if_id = self.next_id_ex = self.next_ex_mem = self.next_mem_wb = None

    def flush_pipeline(self):
        self.if_id = None
        self.id_ex = None
        self.ex_mem = None
        self.mem_wb = None





        


