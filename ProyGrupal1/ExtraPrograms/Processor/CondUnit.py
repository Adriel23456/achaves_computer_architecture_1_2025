from ExtraPrograms.Processor.AuthenticationUnit import AuthenticationProcess

class CondUnit:
    WIDTH = {
        "CondExE": 1,
        "SafeFlagsOut": 2,
        "Flags": 4
    }

    def __init__(self, flags):
        self.flags = flags
        self.reset()
        self.auth_process = AuthenticationProcess()

    def reset(self):
        # salidas
        self.CondExE = 0b0
        self.SafeFlagsOut = 0b00
        self.Flags = 0b0000


    def __setattr__(self, k, v):
        if k in self.WIDTH:
            v &= (1 << self.WIDTH[k]) - 1
        super().__setattr__(k, v)

    def generate_signals(self, BranchOpE: int, LogOutE: int, ComSE: int,
                         LoginBlockE: int, FlagsUpdE: int, ALUFlagsOut: int,
                         flags_e: int):

        #está sección de abajo me confunde, entiendo el manejo de salidade banderas pero el tema del carry se me enredó, no sé si está bien
        if FlagsUpdE:
            # ALUFlagsOut viene como entero NZCV (bit 3=N … bit 0=V)
            n = (ALUFlagsOut >> 3) & 1
            z = (ALUFlagsOut >> 2) & 1
            c = (ALUFlagsOut >> 1) & 1
            v =  ALUFlagsOut        & 1
            self.flags.update_alu(n, z, c, v)
        
        nzcv = self.flags.as_nzcv() if FlagsUpdE else flags_e   # <- valor correcto

        self._handle_branching(BranchOpE, nzcv)                # pasa nzcv
        self._handle_security(LogOutE, ComSE, LoginBlockE, ALUFlagsOut)
        print(f"[COND] BranchOp={BranchOpE:03b} CondExE={self.CondExE}")

    def _handle_branching(self, BranchOpE: int, nzcv: int):
        """
        Decide CondExE (1 = se ejecuta el branch) según BranchOpE y NZCV.
            nzcv[3] = N, nzcv[2] = Z, nzcv[1] = C, nzcv[0] = V
        """
        N = (nzcv >> 3) & 1
        Z = (nzcv >> 2) & 1
        C = (nzcv >> 1) & 1    # (no se usa todavía, pero lo dejamos por claridad)
        V =  nzcv        & 1

        take = False
        if   BranchOpE == 0b000:          # B   – incondicional
            take = True
        elif BranchOpE == 0b001:          # BEQ – igual  → Z = 1
            take = (Z == 1)
        elif BranchOpE == 0b010:          # BNE – no-igual → Z = 0
            take = (Z == 0)
        elif BranchOpE == 0b011:          # BLT – menor que (signed) → N ≠ V
            take = (N != V)
        elif BranchOpE == 0b100:          # BGT – mayor que → Z = 0 y N = V
            take = (Z == 0 and N == V)
        # 101,110,111: reservados / “no branch”
        self.CondExE = 1 if take else 0

    def _handle_security(self, LogOutE: int, ComSE: int,
                     LoginBlockE: int, ALUFlagsOut: int):
        login_block_ba = bytearray([LoginBlockE])
        com_se_ba = bytearray([ComSE])
        alu_flags_ba = bytearray([ALUFlagsOut])
        logout_ba = bytearray([LogOutE])

        # Llamar al proceso de autenticación
        S1, S2 = self.auth_process.login_proceso(
            login_block_ba, com_se_ba, alu_flags_ba, logout_ba
        )
        
        # CRÍTICO: Sincronizar con el objeto Flags del procesador
        if S1 == 1 and S2 == 1:
            self.flags.login()  # Esto actualiza S1 y S2 en el objeto Flags compartido
            print("[COND] Login exitoso - Flags S1/S2 activados")
        elif LogOutE == 1:
            self.flags.logout()  # Esto limpia S1 y S2 en el objeto Flags compartido
            print("[COND] Logout - Flags S1/S2 desactivados")
        
        # Actualizar SafeFlagsOut para reflejar el estado actual
        self.SafeFlagsOut = (self.flags.S1 << 1) | self.flags.S2
        
        # Para debug
        print(f"[COND] SafeFlagsOut={self.SafeFlagsOut:02b} (S1={self.flags.S1}, S2={self.flags.S2})")