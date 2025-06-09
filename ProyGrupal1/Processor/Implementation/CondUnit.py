from AuthenticationUnit import AuthenticationProcess

class CondUnit:
    WIDTH = {
        "CondExE": 1,
        "SafeFlagsOut": 2,
        "Flags": 4,
        "CarryIn": 1
    }

    def __init__(self):
        self.auth_proc = AuthenticationProcess()
        self.reset()
        self.auth_process = AuthenticationProcess()

    def reset(self):
        # salidas
        self.CondExE = 0b0
        self.SafeFlagsOut = 0b00
        self.Flags = 0b0000
        self.CarryIn = 0b0

        # manejo interno de flags
        self._prev_flags = 0b0000

    def __setattr__(self, k, v):
        if k in self.WIDTH:
            v &= (1 << self.WIDTH[k]) - 1
        super().__setattr__(k, v)

    def generate_signals(self, BranchOpE: int, LogOutE: int, ComSE: int,
                         LoginBlockE: int, FlagsUpdE: int, ALUFlagsOut: int,
                         FlagsE: int):


        #está sección de abajo me confunde, entiendo el manejo de salidade banderas pero el tema del carry se me enredó, no sé si está bien
        if FlagsUpdE:
            self.Flags = ALUFlagsOut
        else:
            self.Flags = self._prev_flags

        self._prev_flags = self.Flags

        #settea el carry a partir de las banderas actuales, es el segundo bit
        self.CarryIn = (FlagsE >> 2) & 0b1

        self._handle_branching(BranchOpE)
        self._handle_security(LogOutE, ComSE, LoginBlockE, ALUFlagsOut)

    def _handle_branching(self, BranchOpE: int):
        #verifica las condiciones para el manejor de branches junto con sus flags
        if BranchOpE == 0b000:  # B
            self.CondExE = 0b1
        elif BranchOpE == 0b001:  # BEQ (Z=1)
            self.CondExE = (self.Flags >> 2) & 0b1  # Z flag
        elif BranchOpE == 0b010:  # BNE (Z=0)
            self.CondExE = ((self.Flags >> 2) & 0b1) ^ 0b1  # Inverted Z
        elif BranchOpE == 0b011:  # BLT (N!=V)
            n_flag = (self.Flags >> 3) & 0b1
            v_flag = self.Flags & 0b1
            self.CondExE = n_flag ^ v_flag
        elif BranchOpE == 0b100:  # BGT (Z=0 N=V)
            z_flag = (self.Flags >> 2) & 0b1
            n_flag = (self.Flags >> 3) & 0b1
            v_flag = self.Flags & 0b1
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