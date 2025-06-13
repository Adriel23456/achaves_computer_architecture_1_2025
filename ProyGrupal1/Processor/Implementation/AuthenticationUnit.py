# authentication_process.py
from datetime import datetime, timedelta
#TODO: ALGUIEN QUE HAGA ACÁ EL IMPORT DEL CPU_INFO_EXCEL A MI NO ME DEJA POR ALGÚN MOTIVO



class AuthenticationProcess:
    _instance = None  # clase interna para asegurar singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthenticationProcess, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # evita re-inicializar
        self._initialized = True
        self.try_counter = 0
        self.block_states = bytearray([0b00000000])
        self.S1 = 0
        self.S2 = 0
        self.sesion_activa_desde = None

        # TODO: Cargar estado desde Excel
        self.cargar_estado_local()


    def cargar_estado_local(self):
        value = cpu.table.read_immediate(121, 17)  # Lee R121
        try:
            valor = int(value)
            self.block_states = bytearray([valor])
            print(f"Estado cargado: {bin(valor)}")
        except Exception as e:
            print(f"Error al cargar estado local: {e}")
            self.block_states = bytearray([0b00000000])  # valor por defecto

    def guardar_estado_local(self):
        # block_states es un bytearray con 1 byte, convertimos a entero
        valor = self.block_states[0]
        # Guardamos el entero en el registro R121 (registro 121, posición 17)
        cpu.table.write(121, 17, valor)  # guardamos como el 0b del número entero

        cpu.table.execute_all() #CUIDADO CON ESTO NO SÉ SI ESTÁ PETANDO EL EXCEL

        print(f"Estado guardado: {bin(valor)}")

    def guardar_hora(self, hora):
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parametro = f"'{hora}'"
        cpu.table.write(121, 17, parametro) #ESCRIBE EN R120

        cpu.table.execute_all()  # CUIDADO CON ESTO NO SÉ SI ESTÁ PETANDO EL EXCEL

    def obtener_hora(self):
        string, value = cpu.table.read_immediate(121, 17)  # LEE R120
        return  datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

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

        if self.try_counter >= 15:
            if self.obtener_hora() is None:
                self.guardar_hora(now)
                self.guardar_estado_local()
                print("Acceso bloqueado por exceso de intentos. Temporizador iniciado.")
                return self.S1, self.S2

            if now - self.obtener_hora() < timedelta(minutes=10):
                print(f"Aún bloqueado. Intenta más tarde.")
                return self.S1, self.S2
            else:
                print("Bloqueo expirado. Reiniciando.")
                self.try_reset()
                self.guardar_hora(None)
                self.block_states = bytearray([0b00000000])
                self.guardar_estado_local()

        if LogOutE[0] == 1:
            self.full_reset()
            return self.S1, self.S2

        if ComSE[0] != 1:
            print("ComSE no activo")
            return self.S1, self.S2

        if self.try_counter >= 15:
            self.guardar_hora(now)
            self.guardar_estado_local()
            print("Máximo de intentos alcanzado. Bloqueo.")
            return self.S1, self.S2

        bloque_index = LogininBlockE[0] & 0b00000111
        print(f"Intento de login en bloque {bloque_index}")

        flag_zero = (ALUFlagsOut[0] & 0b0100) != 0
        if not flag_zero:
            self.try_counter += 1
            self.guardar_estado_local()
            print("Flag ZERO no está activa. Fallo de verificación.")
            return self.S1, self.S2

        print(f"Verificación exitosa en bloque {bloque_index}")
        self.actualizar_estado_bloque(bloque_index)
        self.guardar_estado_local()

        if self.todos_los_bloques_verificados():
            print(" Todos los bloques han sido validados exitosamente.")
            self.S1 = 1
            self.S2 = 1

        return self.S1, self.S2
