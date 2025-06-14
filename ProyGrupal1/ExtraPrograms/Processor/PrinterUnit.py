# ExtraPrograms/Processor/PrinterUnit.py
class PrinterUnit:
    """
    Encapsula TODA la salida del procesador.
    Siempre existe un controller, por lo que imprimimos
    vía controller.print_console() sin ‘plan B’.
    """

    def __init__(self, controller):
        self.controller = controller            # referencia directa

    # ----------------------------------------------------------
    # utilidades de impresión
    # ----------------------------------------------------------
    def log(self, msg: str) -> None:
        self.controller.print_console(msg)

    # —----- instrucciones PRINT* ------
    def print_integer(self, value: int):
        self.controller.print_console(f"[INT] {value}")

    def print_ascii(self, value: int):
        # 8 bytes little-endian → primer ASCII imprimible
        for b in value.to_bytes(8, "little"):
            if 32 <= b <= 126:
                self.controller.print_console(chr(b))
                return
        self.controller.print_console(".")

    def print_binary(self, value: int):
        self.controller.print_console(f"[BIN] {value:032b}")
        