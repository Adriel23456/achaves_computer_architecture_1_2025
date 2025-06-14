# control_unit.py  (fragmento clave)
# ════════════════════════════════════════════════════════════════════
class ControlUnit:
    WIDTH = {           # ancho de cada línea (igual que antes) …
        "RegWriteS":1,"RegWriteR":1,"MemOp":2,"MemWriteG":1,"MemWriteD":1,
        "MemWriteV":1,"MemWriteP":1,"MemByte":1,"PCSrc":1,
        "ALUSrc":6,"PrintEn":2,"ComS":1,"LogOut":1,"BranchE":1,"FlagsUpd":1,
        "BranchOp":3,"ImmediateOp":1,"RegisterInB":2,"RegisterInA":1,
    }
    def reset(self):
        # Señales de control (salidas)
        self.RegWriteS = 0b0
        self.RegWriteR = 0b0
        self.MemOp = 0b00
        self.MemWriteG = 0b0
        self.MemWriteD = 0b0
        self.MemWriteV = 0b0
        self.MemWriteP = 0b0
        self.MemByte = 0b0
        self.PCSrc = 0b0
        self.ALUSrc = 0b000000
        self.PrintEn = 0b00
        self.ComS = 0b0
        self.LogOut = 0b0
        self.BranchE = 0b0
        self.FlagsUpd = 0b0


        # Señales adicionales del datapath extendido
        self.BranchOp = 0b000
        self.ImmediateOp = 0b0
        self.RegisterInB = 0b00
        self.RegisterInA = 0b0


    # ------------ setters masked by WIDTH (igual que en canvas) -----
    def __setattr__(self,k,v):
        if k in self.WIDTH: v &= (1<<self.WIDTH[k])-1
        super().__setattr__(k,v)

    # ------------ macros de configuración común --------------------
    def first_part(self):
        self.BranchOp = 0b111
        self.MemOp    = 0b11
        self.PrintEn  = 0b11

    def branches(self):
        self.ImmediateOp = 1
        self.BranchE     = 1
        self.PCSrc       = 1
        self.FlagsUpd    = 1
        self.MemOp       = 0b11
        self.PrintEn     = 0b11

    def memory_instructions(self):
        self.ImmediateOp = 1
        self.BranchOp    = 0b111
        self.FlagsUpd    = 1
        self.PrintEn     = 0b11

    def last(self):
        self.BranchOp = 0b111
        self.FlagsUpd = 1      # se invertirá al final

    # ------------ tabla CFG ----------------------------------------
    CFG: dict[int, dict[str, int | str]] = {
        # 1) Aritmética / lógica R-R (Rose)
        0b00000000: {"pattern":"ARITH_RR", "macro":"first_part"},    # ADD
        0b00000001: {"RegisterInB":0b10, "RegWriteS":1, "macro":"first_part"},          # ADDS (no pattern)
        0b00000010: {"ALUSrc":0b000001, "pattern":"ARITH_RR", "macro":"first_part"},    # SUB
        0b00000011: {"ALUSrc":0b000010, "pattern":"ARITH_RR", "macro":"first_part"},    # ADC
        0b00000100: {"ALUSrc":0b000011, "pattern":"ARITH_RR", "macro":"first_part"},    # SBC
        0b00000101: {"ALUSrc":0b000100, "pattern":"ARITH_RR", "macro":"first_part"},    # MUL
        0b00000110: {"ALUSrc":0b000101, "pattern":"ARITH_RR", "macro":"first_part"},    # DIV
        0b00000111: {"ALUSrc":0b000110, "pattern":"ARITH_RR", "macro":"first_part"},    # AND
        0b00001000: {"ALUSrc":0b000111, "pattern":"ARITH_RR", "macro":"first_part"},    # ORR
        0b00001001: {"ALUSrc":0b001000, "pattern":"ARITH_RR", "macro":"first_part"},    # EOR
        0b00001010: {"ALUSrc":0b001001, "pattern":"ARITH_RR", "macro":"first_part"},    # BIC
        0b00001011: {"ALUSrc":0b001010, "pattern":"ARITH_RR", "macro":"first_part"},    # LSL
        0b00001100: {"ALUSrc":0b001011, "pattern":"ARITH_RR", "macro":"first_part"},    # LSR
        0b00001101: {"ALUSrc":0b001100, "pattern":"ARITH_RR", "macro":"first_part"},    # ASR
        0b00001110: {"ALUSrc":0b001101, "pattern":"ARITH_RR", "macro":"first_part"},    # ROR

        # 2) Aritmética inmediata (Papaya)
        0b00001111: {"ALUSrc":0b000000, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # ADDI
        0b00010000: {"ALUSrc":0b000001, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # SUBI
        0b00010001: {"ALUSrc":0b000010, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # ADCI
        0b00010010: {"ALUSrc":0b000011, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # SBCI
        0b00010011: {"ALUSrc":0b000100, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # MULI
        0b00010100: {"ALUSrc":0b000101, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # DIVI
        0b00010101: {"ALUSrc":0b000110, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # ANDI
        0b00010110: {"ALUSrc":0b000111, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # ORRI
        0b00010111: {"ALUSrc":0b001000, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # EORI
        0b00011000: {"ALUSrc":0b001001, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # BICI
        0b00011001: {"ALUSrc":0b001010, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # LSLI
        0b00011010: {"ALUSrc":0b001011, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # LSRI
        0b00011011: {"ALUSrc":0b001100, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # ASRI
        0b00011100: {"ALUSrc":0b001101, "ImmediateOp":1, "pattern":"ARITH_RS", "macro":"first_part"}, # RORI

        # 3) MOV / MVN / inmediatos
        0b00011101: {"ALUSrc":0b001110, "FlagsUpd":1, "pattern":"MOV_R", "macro":"first_part"},        # MOV  (Lilac, sí depende de Special)
        0b00011110: {"ALUSrc":0b001111, "FlagsUpd":1, "pattern":"MOV_R", "macro":"first_part"},        # MVN  (Lilac, sí depende de Special)
        0b00011111: {"ALUSrc":0b001110, "ImmediateOp":1, "FlagsUpd":1, "pattern":"MOV_I", "macro":"first_part"}, # MOVI (Green, no depende de Special)
        0b00100000: {"ALUSrc":0b001111, "ImmediateOp":1, "FlagsUpd":1, "pattern":"MOV_I", "macro":"first_part"}, # MVNI (Green, no depende de Special)

        # 4) Comparación / test (Blue, Orange, etc.)
        0b00100001: {"ALUSrc":0b010000, "pattern":"CMP_RR", "macro":"first_part"},    # CMP
        0b00100010: {"RegisterInA":0b1, "RegisterInB":0b11, "ALUSrc":0b010000, "ComS":0b1},         # CMPS (direct)
        0b00100011: {"ALUSrc":0b010001, "pattern":"CMP_RR", "macro":"first_part"},    # CMN
        0b00100100: {"ALUSrc":0b010010, "pattern":"CMP_RR", "macro":"first_part"},    # TST
        0b00100101: {"ALUSrc":0b010011, "pattern":"CMP_RR", "macro":"first_part"},    # TEQ
        0b00100110: {"ALUSrc":0b010000, "ImmediateOp":1, "pattern":"CMP_RR", "macro":"first_part"}, # CMPI
        0b00100111: {"ALUSrc":0b010001, "ImmediateOp":1, "pattern":"CMP_RR", "macro":"first_part"}, # CMNI
        0b00101000: {"ALUSrc":0b010010, "ImmediateOp":1, "pattern":"CMP_RR", "macro":"first_part"}, # TSTI
        0b00101001: {"ALUSrc":0b010011, "ImmediateOp":1, "pattern":"CMP_RR", "macro":"first_part"}, # TEQI

        # 5) Saltos
        0b00101010: {"macro":"branches"},  # B
        0b00101011: {"BranchOp":0b001, "macro":"branches"},  # BEQ
        0b00101100: {"BranchOp":0b010, "macro":"branches"},  # BNE
        0b00101101: {"BranchOp":0b011, "macro":"branches"},  # BLT
        0b00101110: {"BranchOp":0b100, "macro":"branches"},  # BGT

        # 6) SWI / NOP  (sin pattern, macro directo)
        0b00101111: {"RegisterInA":0b1, "FlagsUpd":0b1, "macro":"first_part"}, # SWI (directo, como en tu elif)
        0b00110000: {"RegisterInA":0b1, "FlagsUpd":0b1, "macro":"first_part"}, # NOP (directo)

        # 7) Transferencia memoria (DarkGreen, con casos LDR/STR/LDRB/STRB)
        0b00110001: {"macro":"memory_instructions", "pattern":"MEM_ACCESS"}, # LDR
        0b00110010: {"macro":"memory_instructions", "MemOp":0b11, "pattern":"MEM_ACCESS"}, # STR
        0b00110011: {"macro":"memory_instructions", "MemByte":0b1, "pattern":"MEM_ACCESS"}, # LDRB
        0b00110100: {"macro":"memory_instructions", "MemOp":0b11, "MemByte":0b1, "pattern":"MEM_ACCESS"}, # STRB

        # 8) PRINT / LOGOUT / STRK / STRPASS  (Pink y otras, directos)
        0b00110101: {"macro":"last", "ImmediateOp":1, "pattern":"PRINT"}, # PRINTI
        0b00110110: {"macro":"last", "ImmediateOp":1, "PrintEn":0b01, "pattern":"PRINT"}, # PRINTS
        0b00110111: {"macro":"last", "ImmediateOp":1, "PrintEn":0b10, "pattern":"PRINT"}, # PRINTB
        0b00111000: {"macro":"last", "ImmediateOp":1, "MemOp":0b11, "PrintEn":0b11, "LogOut":0b1}, # LOGOUT
        0b00111001: {"macro":"last", "MemOp":0b11, "PrintEn":0b11, "MemWriteV":0b1}, # STRK (directo)
        0b00111010: {"macro":"last", "MemOp":0b11, "PrintEn":0b11, "MemWriteP":0b1}, # STRPASS (directo)
    }
    
    # ------------ generación principal -----------------------------
    def generate_signals(self, special: int, op: int):
        self.reset()                              # clean slate
        entry = self.CFG.get(op)
        if entry is None:
            raise ValueError(f"Opcode 0x{op:02x} no definido")

        # 1) aplica las llaves simples del CFG
        for k,v in entry.items():
            if k in ("pattern","macro"): continue
            setattr(self,k,v)

        # 2) dispara la macro común (si la hay)
        if (m := entry.get("macro")):
            getattr(self, m)()                    # llama first_part/…

        # 3) interpreta los 4 bits Special según el patrón
        if (p := entry.get("pattern")):
            self._apply_pattern(special, p, op)

        # 4) NOT final a FlagsUpd
        self.FlagsUpd ^= 1

    # ------------ patrones Special ---------------------------------
    def _apply_pattern(self, spec: int, pat: str, op: int):
        b0, b1, b2, b3 = [(spec >> i) & 1 for i in range(4)]

        if pat == "ARITH_RR":
            self.RegisterInA = b2 ^ 1
            self.RegisterInB = b1
            self._set_reg_write(b3)
        elif pat == "ARITH_RS":
            self.RegisterInA = b2 ^ 1
            self._set_reg_write(b3)
        elif pat == "MOV_R":   # Lilac: sí depende de b1
            self.RegisterInB = b1
            self._set_reg_write(b3)
        elif pat == "MOV_I":   # Green: NO depende de Special
            self._set_reg_write(b3)
        elif pat == "CMP_RR":  # BLUE
            self.RegisterInA = b2 ^ 1
            self.RegisterInB = b1
            # No _set_reg_write, no immediate
        elif pat == "CMP_RS":  # ORANGE
            self.RegisterInA = b2 ^ 1
            # ¡NO se ajusta RegisterInB aquí!
        elif pat == "PRINT":
            self.RegisterInA = b2 ^ 1
            self._set_mem_op(b0)
        elif pat == "MEM_ACCESS":
            self.RegisterInA = b2 ^ 1
            if op in (0b00110001, 0b00110011):   # LDR / LDRB
                self._set_mem_op(b0)
                self._set_reg_write(b3)
            else:                               # STR / STRB
                self.RegisterInB = b1
                self._set_mem_write(b0)
        else:
            raise ValueError(f"Patrón '{pat}' desconocido")
        

    # ------------ helpers compuestos -------------------------------
    def _set_reg_write(self,b):
        self.RegWriteS, self.RegWriteR = b, b^1
    def _set_mem_write(self, b):
        # b = 0 → escribir en memoria general
        # b = 1 → escribir en memoria dinámica
        self.MemWriteG = 1 if b == 0 else 0
        self.MemWriteD = 1 if b == 1 else 0
    def _set_mem_op(self, b):
        # b = 0 → general → MemOp = 00
        # b = 1 → dinámica → MemOp = 01
        self.MemOp = 0b00 if b == 0 else 0b01