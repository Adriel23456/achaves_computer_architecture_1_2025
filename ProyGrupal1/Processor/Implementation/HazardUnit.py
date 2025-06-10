import ALU
import PipeLine
import ProgramCounter


class HazardUnit:
    def __init__(self, pipe_line_fetch: PipeLine, pipe_line_decode: PipeLine, pipe_line_execution: PipeLine, pipe_line_memory: PipeLine, alu: ALU, pc: ProgramCounter):
        self.pc: ProgramCounter = pc
        self.fetch: PipeLine = pipe_line_fetch
        self.decode: PipeLine = pipe_line_decode
        self.execution: PipeLine = pipe_line_execution
        self.memory: PipeLine = pipe_line_memory
        self.ALU: ALU = alu
        self.stallCallsCounter = 0

    def call_stall(self):
        self.fetch.stall()
        self.pc.stall()
        return

    def call_bubble(self):
        self.stallCallsCounter = 2
        return

    def call_forwarding(self): #trae instruccion de alu a decode
        #TODO >>>>> no veo la salida de la alu hacia atras (el decode), no se como hacerlo, si alguien sabe pues me dice y lo intento
        return

    def check(self): #comprobar que no se quiere escribir en r que se vayan a leer en el mismo ciclo
        if (self.fetch.RD1 == self.decode.RW) or (self.fetch.RD2 == self.decode.RW): #esto valores se pueden acceder, no se calculan
            self.call_bubble()
            return

    def tick(self):
        #aca se hace el bubble
        #hace 2 stalls cuando la instr usa el mismo registro de lectura con una instruccion que lo esta usando para escritura
        if self.stallCallsCounter == 0:
            self.check()
            return

        if self.stallCallsCounter > 0: #hay que llamar al stall 2 veces para el registro
            self.stallCallsCounter -= 1
            self.call_stall()
            return

        return None