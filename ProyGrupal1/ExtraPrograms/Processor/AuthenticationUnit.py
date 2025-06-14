from datetime import datetime, timedelta

class AuthenticationProcess:
    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthenticationProcess, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.try_counter = 0
        self.block_states = bytearray([0b00000000])  # Estado de bloques validados
        self.S1 = 0
        self.S2 = 0
        self.sesion_activa_desde = None  # hora de bloqueo si aplica

    def set_block_states(self, value: int):
        self.block_states = bytearray([value])
        print(f"[SET] Estado de bloques actualizado: {bin(value)}")

    def get_block_states(self) -> int:
        return self.block_states[0]

    def set_sesion_activa_desde(self, hora: datetime):
        self.sesion_activa_desde = hora
        print(f"[SET] Hora de sesión activa desde: {hora}")

    def get_sesion_activa_desde(self) -> datetime:
        return self.sesion_activa_desde


    def try_reset(self):
        self.try_counter = 0
        print("try_counter reiniciado a 0")

    def full_reset(self):
        self.S1 = 0
        self.S2 = 0
        self.try_counter = 0
        print("full_reset aplicado: S1, S2, try_counter en 0")

    def reset_flags(self):
        self.S1 = 0
        self.S2 = 0
        print("Logout detectado: Flags S1 y S2 en 0")

    def actualizar_estado_bloque(self, bloque_index):
        self.block_states[0] |= (1 << bloque_index)

    def todos_los_bloques_verificados(self):
        return self.block_states[0] == 0b11111111

    def login_proceso(self, LogininBlockE: bytearray, ComSE: bytearray,
                      ALUFlagsOut: bytearray, LogOutE: bytearray):
        now = datetime.now()
        print(f"[AUTH_DEBUG] LoginBlockE={LogininBlockE[0]:08b}, bloque_idx={LogininBlockE[0] & 0b00000111}")

        if self.try_counter >= 15:
            if self.get_sesion_activa_desde() is None:
                self.set_sesion_activa_desde(now)
                print("Acceso bloqueado por exceso de intentos. Temporizador iniciado.")
                return self.S1, self.S2

            if now - self.get_sesion_activa_desde() < timedelta(minutes=10):
                print("Aún bloqueado. Intenta más tarde.")
                return self.S1, self.S2
            else:
                print("Bloqueo expirado. Reiniciando.")
                self.try_reset()
                self.set_sesion_activa_desde(None)
                self.set_block_states(0b00000000)

        if LogOutE[0] == 1:
            self.full_reset()
            return self.S1, self.S2

        if ComSE[0] != 1:
            print("ComSE no activo")
            return self.S1, self.S2

        if self.try_counter >= 15:
            self.set_sesion_activa_desde(now)
            print("Máximo de intentos alcanzado. Bloqueo.")
            return self.S1, self.S2

        bloque_index = LogininBlockE[0] & 0b00000111
        print(f"Intento de login en bloque {bloque_index}")

        flag_zero = (ALUFlagsOut[0] & 0b0100) != 0
        if not flag_zero:
            self.try_counter += 1
            print("Flag ZERO no está activa. Fallo de verificación.")
            return self.S1, self.S2

        print(f"Verificación exitosa en bloque {bloque_index}")
        self.actualizar_estado_bloque(bloque_index)

        if self.todos_los_bloques_verificados():
            print("Todos los bloques han sido validados exitosamente.")
            self.S1 = 1
            self.S2 = 1

        # Cuando se validan todos los bloques:
        if self.todos_los_bloques_verificados():
            print("Todos los bloques han sido validados exitosamente.")
            self.S1 = 1
            self.S2 = 1
            print(f"[AUTH] Login completo: S1={self.S1}, S2={self.S2}")
            print(f"[AUTH] Block states final: {self.block_states[0]:08b}")
        
        return self.S1, self.S2
