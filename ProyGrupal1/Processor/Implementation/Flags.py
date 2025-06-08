# flags.py

class Flags:
    """
    Flags del procesador (todos como bits de 0 o 1):

    • ALU    : N (negativo), Z (cero), C (acarreo), V (overflow)
    • Seguridad: S1 y S2 → deben estar ambos en 1 para acceso seguro
    • Login   : L → transitorio, se activa con ComS (solo durante CMPS)
    """

    def __init__(self):
        # Flags de la ALU
        self.N = 0
        self.Z = 0
        self.C = 0
        self.V = 0

        # Flags de seguridad
        self.S1 = 0
        self.S2 = 0

        # Flag transitorio (se activa con ComS desde ControlUnit)
        self.L  = 0  # ← debe ser asignado desde afuera, no aquí

    # ────────────────────────────────────────────────
    # Seguridad
    # ────────────────────────────────────────────────
    def login(self):
        """Activa S1 y S2 (login exitoso)."""
        self.S1 = 1
        self.S2 = 1

    def logout(self):
        """Apaga S1 y S2 (logout o falla de autenticación)."""
        self.S1 = 0
        self.S2 = 0

    def enabled(self) -> int:
        """Retorna 1 si S1 y S2 están activos; 0 en caso contrario."""
        return 1 if (self.S1 & self.S2) else 0

    # ────────────────────────────────────────────────
    # Flags de la ALU
    # ────────────────────────────────────────────────
    def update_alu(self, n: int, z: int, c: int, v: int):
        """Actualiza los flags NZCV desde bits individuales."""
        self.N = n & 1
        self.Z = z & 1
        self.C = c & 1
        self.V = v & 1

    def clear_alu(self):
        """Limpia los flags NZCV."""
        self.N = self.Z = self.C = self.V = 0

    # ────────────────────────────────────────────────
    # Debug / Visualización
    # ────────────────────────────────────────────────
    def visualize(self) -> dict:
        """Devuelve el estado completo de todos los flags."""
        return {
            "N": self.N, "Z": self.Z, "C": self.C, "V": self.V,
            "S1": self.S1, "S2": self.S2, "L": self.L
        }
