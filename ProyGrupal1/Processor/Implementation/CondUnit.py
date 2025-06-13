from AuthenticationUnit import AuthenticationProcess

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
            n, z, c, v = ALUFlagsOut          # tupla Flags
            self.flags.update_alu(n, z, c, v)
        
        nzcv = self.flags.as_nzcv() if FlagsUpdE else flags_e   # <- valor correcto

        self._handle_branching(BranchOpE, nzcv)                # pasa nzcv
        self._handle_security(LogOutE, ComSE, LoginBlockE, ALUFlagsOut)

    def _handle_branching(self, BranchOpE: int, nzcv: int):
        #verifica las condiciones para el manejor de branches junto con sus flags
        if BranchOpE == 0b000:  # B
            self.CondExE = 0b1
        elif BranchOpE == 0b001:  # BEQ (Z=1)
            self.CondExE = (nzcv >> 2) & 0b1  # Z flag
        elif BranchOpE == 0b010:  # BNE (Z=0)
            self.CondExE = ((nzcv >> 2) & 0b1) ^ 0b1  # Inverted Z
        elif BranchOpE == 0b011:  # BLT (N!=V)
            n_flag = (nzcv >> 3) & 0b1
            v_flag = nzcv & 0b1
            self.CondExE = n_flag ^ v_flag
        elif BranchOpE == 0b100:  # BGT (Z=0 N=V)
            z_flag = (nzcv >> 2) & 0b1
            n_flag = (nzcv >> 3) & 0b1
            v_flag = nzcv & 0b1
            self.CondExE = (z_flag ^ 0b1) & (n_flag ^ v_flag ^ 0b1)
        else:
            self.CondExE = 0b0

    def _handle_security(self, LogOutE: int, ComSE: int,
                         LoginBlockE: int, ALUFlagsOut: int):
        login_block_ba = bytearray([LoginBlockE])
        com_se_ba = bytearray([ComSE])
        alu_flags_ba = bytearray([ALUFlagsOut])
        logout_ba = bytearray([LogOutE])

        # en buena teoria esta vara llama al singleton del autenticador, hay que verificar si funciona
        S1, S2 = self.auth_process.login_proceso(
            login_block_ba, com_se_ba, alu_flags_ba, logout_ba
        )
        # esto devuelve el 0b00 correspondiente a las banteras
        self.SafeFlagsOut = (S1 << 1) | S2