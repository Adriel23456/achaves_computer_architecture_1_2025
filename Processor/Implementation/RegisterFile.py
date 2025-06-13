class RegisterFile:
    def __init__(self):
        self.regs      = [0] * 16
        self._pending  = None        # ← escritura latched
        # opcional: nombres simbólicos
        self.R0 = 0  # alias a regs[0] si querés un cero hard‐wired

    # ---------------- lectura (combinacional) -----------------
    def read(self, ar1: int, ar2: int) -> tuple[int, int]:
        return self.regs[ar1 & 0xF], self.regs[ar2 & 0xF]

    # ---------------- escribir: se latchea hasta el flanco ----
    def write(self, ar3: int, wdr3: int, regwrite: int):
        if regwrite:                      # 1 = deseo de escribir
            self._pending = (ar3 & 0xF, wdr3 & 0xFFFFFFFF)

    # ---------------- flanco activo de reloj ------------------
    def tick(self):
        if self._pending:
            idx, data = self._pending
            # ejemplo: mantener R0 en 0 si tu ISA lo requiere
            if idx != 0:
                self.regs[idx] = data
            self._pending = None          # se consume

    # -------------- depuración opcional -----------------------
    def debug(self):
        for i in range(0, 16, 4):
            print(" ".join(f"R{i+j:02}:{self.regs[i+j]:08X}" for j in range(4)))
