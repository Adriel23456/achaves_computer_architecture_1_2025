class PrinterUnit:

    @staticmethod
    def print_integer(value: int):
        print(f"[INT] {value}")

    @staticmethod
    def print_ascii(value: int):
        char = chr(value & 0xFF)  # Solo el byte menos significativo
        print(f"[ASCII] {char}")

    @staticmethod
    def print_binary(value: int):
        print(f"[BIN] {value:032b}")

