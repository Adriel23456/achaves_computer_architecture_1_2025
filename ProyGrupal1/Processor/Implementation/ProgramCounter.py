class Mux:
    def __init__(self):
        self.input0 = 0
        self.input1 = 0
        self.select = 0

    def output(self):
        return self.input1 if self.select else self.input0


class ProgramCounter:
    def __init__(self):
        self.pc = 0 #dirección de memoria de la instruccion, HAY QUE TRAER VALORES DEL EXCEL ACÁ O HACER FUNCION APARTE
        self.result_w = 0 #ALUOutW_C
        self.pcsrc_w = 0 #PCSrcW
        self.mux = Mux()
        self.stall = False

    def tick(self):
        if self.stall:
            self.stall = False
            return None
        else:
            self.mux.input0 = self.pc + 8
            self.mux.input1 = self.result_w
            self.mux.select = self.pcsrc_w

            # aplicar salida del MUX como nuevo PC
            self.pc = self.mux.output()

    def stall(self):
        self.stall = True
        return None


    def get_pc(self):
        return self.pc
