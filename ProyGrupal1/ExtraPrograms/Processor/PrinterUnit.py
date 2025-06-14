class PrinterUnit:

    @staticmethod
    def print_integer(value: int):
        print(f"[INT] {value}")

    @staticmethod
    def print_ascii(value: int):
        # convertir el entero en bytes (little-endian, 8 bytes = 64 bits)
        bytes_le = value.to_bytes(8, byteorder='little')

        # buscar el primer byte ASCII imprimible (rango 32–126)
        for b in bytes_le:
            if 32 <= b <= 126:
                print(chr(b))
                return

        # si ninguno era imprimible, mostrar '.'
        print('.')


    @staticmethod
    def print_binary(value: int):
        print(f"[BIN] {value:032b}")

