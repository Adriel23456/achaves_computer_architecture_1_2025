class BinaryZeroExtend:

    def uxtb_32_to_32(self, input_val, show_bits=False):
        # Convertir input si es string binario
        if isinstance(input_val, str) and input_val.startswith('0b'):
            input_val = int(input_val, 2)

        # Asegurar que input sea de 32 bits
        masked = input_val & 0xFFFFFFFF

        # Extraer el byte menos significativo (LSB)
        result = masked & 0xFF  # Zero-extend automático en Python

        if show_bits:
            print(f"\nEntrada (32 bits):    {BinaryZeroExtend.int_to_bin32(masked)}")
            print(f"Byte menos sig. (LSB): {BinaryZeroExtend.int_to_bin32(result)}")

        return result

    @staticmethod
    def int_to_bin32(value):
        return f"0b{value & 0xFFFFFFFF:032b}"
