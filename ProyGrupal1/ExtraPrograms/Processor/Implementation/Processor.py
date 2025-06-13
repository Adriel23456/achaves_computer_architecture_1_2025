from ExtraPrograms.Processor.Implementation.PipeLine import Pipeline
from ExtraPrograms.Processor.Implementation.ProgramCounter import ProgramCounter
from ExtraPrograms.Processor.Implementation.InstructionMemory import InstructionMemory
from ExtraPrograms.Processor.Implementation.RegisterFile import RegisterFile
from ExtraPrograms.Processor.Implementation.SafeRegisters import SafeRegisterFile
from ExtraPrograms.Processor.Implementation.DataMemory import DataMemory
from ExtraPrograms.Processor.Implementation.DynamicMemory import DynamicMemory
from ExtraPrograms.Processor.Implementation.VaultMemory import VaultMemory
from ExtraPrograms.Processor.Implementation.LoginMemory import LoginMemory
from ExtraPrograms.Processor.Implementation.ALU import ALU
from ExtraPrograms.Processor.Implementation.Flags import Flags
from ExtraPrograms.Processor.Implementation.ControlUnit import ControlUnit
from ExtraPrograms.Processor.Implementation.CondUnit import CondUnit
from ExtraPrograms.Processor.Implementation.Extend import BinaryZeroExtend

class Procesador:
    def __init__(self):
        """Crea todas las unidades y engancha el pipeline.
        El orden de instanciación **importa** porque varios módulos
        reciben `flags` en su constructor.
        """
        # ---- Estado global de banderas (ALU + seguridad) ----
        self.flags = Flags()

        # ---- Unidades básicas ----
        self.pc                 = ProgramCounter()
        self.instruction_memory = InstructionMemory()
        self.register_file      = RegisterFile()
        self.data_memory        = DataMemory()
        self.dynamic_memory     = DynamicMemory(self.flags)
        self.safe_register_file = SafeRegisterFile(self.flags)
        self.vault_memory       = VaultMemory(self.flags)
        self.login_memory       = LoginMemory(self.flags)
        self.alu                = ALU()
        self.control_unit       = ControlUnit()
        self.extend             = BinaryZeroExtend()   # helper para extensiones
        self.cond_unit          = CondUnit(self.flags)

        # ---- Ensambla el pipeline completo ----
        self.pipeline = Pipeline(
            program_counter      = self.pc,
            instruction_memory   = self.instruction_memory,
            register_file        = self.register_file,
            safe_register_file   = self.safe_register_file,
            data_memory          = self.data_memory,
            dynamic_memory       = self.dynamic_memory,
            vault_memory         = self.vault_memory,
            login_memory         = self.login_memory,
            alu                  = self.alu,
            flags                = self.flags,
            control_unit         = self.control_unit,
            cond_unit            = self.cond_unit,
            extend               = self.extend,
        )

    # ------------------------------------------------------------------
    # Ejecución completa
    # ------------------------------------------------------------------
    def run_all(self, max_cycles: int = 1000):
        """Avanza el *datapath* ciclo a ciclo hasta que el pipeline
        quede vacío (o se alcance `max_cycles`).  Imprime un resumen
        de cada ciclo para depuración rápida.
        """
        for cycle in range(max_cycles):
            print(f"\n===== CYCLE {cycle+1} =====")
            self.pipeline.step()

            if all(stage is None for stage in (
                self.pipeline.if_id,
                self.pipeline.id_ex,
                self.pipeline.ex_mem,
                self.pipeline.mem_wb,
                self.pipeline.next_if_id,
                self.pipeline.next_id_ex,
                self.pipeline.next_ex_mem,
                self.pipeline.next_mem_wb,
            )):
                print("Pipeline vacío. Ejecución completa.")
                break
        else:
            print("Límite de ciclos alcanzado sin completar ejecución.")
            
    def set_state_from_external(self, state_dict):
        """Permite cargar un estado completo desde fuente externa."""
        if 'pc' in state_dict:
            self.pc._pc = state_dict['pc']
        if 'registers' in state_dict:
            for i, val in enumerate(state_dict['registers']):
                if i < 16:
                    self.register_file.regs[i] = val
