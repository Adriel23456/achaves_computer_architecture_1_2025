#!/usr/bin/env python3
"""
calc_32bit_twos_complement.py
Convierte un número decimal con signo a su representación de 32 bits en
complemento a 2 y también muestra la forma hexadecimal de 8 dígitos.

Ahora el programa es interactivo: al ejecutarlo sin argumentos, pedirá el
número desde la consola y validará que esté dentro del rango firmado de
32 bits (−2 147 483 648 a 2 147 483 647).

Uso desde la terminal:
    python calc_32bit_twos_complement.py
"""

BIT_WIDTH = 32
MIN_32 = -(1 << (BIT_WIDTH - 1))          # −2 147 483 648
MAX_32 =  (1 << (BIT_WIDTH - 1)) - 1      #  2 147 483 647
MOD_32 =  1 << BIT_WIDTH                  #  2³²

def decimal_to_twos_complement_32(n: int) -> str:
    """Devuelve la cadena de 32 bits en complemento a 2 para el entero *n*."""
    if n < MIN_32 or n > MAX_32:
        raise ValueError(
            f"El valor {n} está fuera del rango de 32 bits con signo "
            f"({MIN_32} a {MAX_32})."
        )

    unsigned_val = n & (MOD_32 - 1)  # máscara 0xFFFFFFFF
    return f"{unsigned_val:0{BIT_WIDTH}b}"

def main():
    while True:
        try:
            raw = input("Introduce un número decimal dentro del rango de 32 bits \n"
                         "(o pulsa Enter sin escribir nada para salir): ")
            if raw.strip() == "":
                print("Hasta luego!")
                break
            # Permite prefijos 0x, 0b, 0o y signos
            n = int(raw, 0)
            bits = decimal_to_twos_complement_32(n)
            print("\nResultado:")
            print(f"Decimal  : {n}")
            print(f"Binario  : {bits}")
            print(f"Hex      : 0x{int(bits, 2):08X}\n")
        except ValueError as e:
            print(f"\nError: {e}\nInténtalo de nuevo.")
        except (KeyboardInterrupt, EOFError):
            print("\n\nInterrupción detectada. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()