class BinaryZeroExtend:

    @staticmethod
    def uxtb_32_to_32(input_val, show_bits=False):
        # Convertir input si es string binario
        if isinstance(input_val, str) and input_val.startswith('0b'):
            input_val = int(input_val, 2)

        # Asegurar 32bits
        masked = input_val & 0xFFFFFFFF

        if show_bits:
            print(f"\nEntrada (32 bits):  {BinaryZeroExtend.int_to_bin32(masked)}")

        # Eliminar los 8 bits más significativos y desplazar izquierda
        # Primero eliminamos los 8 bits superiores (AND con 0x00FFFFFF)
        # Luego desplazamos izquierda 8 bits (multiplicar por 256)
        result = (masked & 0x00FFFFFF) << 8

        if show_bits:
            print(f"Máscara (0x00FFFFFF): {BinaryZeroExtend.int_to_bin32(0x00FFFFFF)}")
            print(f"Desplazado << 8:    {BinaryZeroExtend.int_to_bin32(result)}")

        return result

    @staticmethod
    def int_to_bin32(value):
        return f"0b{value & 0xFFFFFFFF:032b}"