class ProgramCounter:
    def __init__(self):
        self._pc = 0              # ← usá _pc como nombre interno
        self.result_w = 0
        self.pcsrc_w = 0

    def tick(self):
        if self.pcsrc_w:
            self._pc = self.result_w
        else:
            self._pc += 8

        self.result_w = 0
        self.pcsrc_w = 0

    def get_pc(self):
        return self._pc
