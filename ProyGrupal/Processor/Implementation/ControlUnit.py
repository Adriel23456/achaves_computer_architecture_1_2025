class ControlUnit:
    def __init__(self):
        self.reset()

    def reset(self):
        # Señales de control (salidas)
        self.RegWrite = 0
        self.MemOp = 0
        self.MemWrite = 0
        self.MemByte = 0
        self.PCSrc = 0
        self.MovOp = 0
        self.ALUSrc = 0
        self.PrintEn = 0
        self.ComS = 0
        self.LogOut = 0

        # Señales adicionales del datapath extendido
        self.ALUOp = 0
        self.BranchOp = 0
        self.ImmediateOp = 0
        self.RegisterInB = 0
        self.RegisterInA = 0
        self.WriteEnM = 0
        self.WriteEnV = 0

    def generate_signals(self, op: int, special: int = 0, funct7: int = 0):
        self.reset()

