from PipeLine import Pipeline
from ProgramCounter import ProgramCounter
from InstructionMemory import InstructionMemory
from RegisterFile import RegisterFile
from SafeRegisters import SafeRegisterFile
from DataMemory import DataMemory
from DynamicMemory import DynamicMemory
from VaultMemory import VaultMemory
from LoginMemory import LoginMemory
from ALU import ALU
from Flags import Flags
from ControlUnit import ControlUnit
from CondUnit import CondUnit
from Extend import BinaryZeroExtend

class Procesador:
    def __init__(self):
        # === Instancias de módulos ===
        self.pc = ProgramCounter()
        self.instruction_memory = InstructionMemory()
        self.register_file = RegisterFile()
        self.data_memory = DataMemory()
        self.alu = ALU()
        self.flags = Flags()
        self.dynamic_memory = DynamicMemory(self.flags)
        self.safe_register_file = SafeRegisterFile(self.flags)
        self.vault_memory = VaultMemory(self.flags)
        self.login_memory = LoginMemory(self.flags)
        self.control_unit = ControlUnit()
        self.extend = BinaryZeroExtend()  # ← se resuelve helper aquí
        self.cond_unit = CondUnit(self.flags)  # ← se pasa flags

        # === Instancia del pipeline ===
        self.pipeline = Pipeline(
            program_counter=self.pc,
            instruction_memory=self.instruction_memory,
            register_file=self.register_file,
            safe_register_file=self.safe_register_file,
            data_memory=self.data_memory,
            dynamic_memory=self.dynamic_memory,
            vault_memory=self.vault_memory,
            login_memory=self.login_memory,
            alu=self.alu,
            flags=self.flags,
            control_unit=self.control_unit,
            cond_unit=self.cond_unit,
            extend=self.extend
        )
