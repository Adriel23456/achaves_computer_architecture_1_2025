from datetime import datetime, timedelta

class AuthenticationProcess:
    def __init__(self):
        self.try_counter = 0
        self.bloqueado_desde = None
        self.block_states = bytearray([0b00000000])  # Registro de bloques validados, ESTO TAMBIEN SE TIENE QUE SACAR DEL EXCEL Y ACTUALIZARLO DE MANERA CONSTANTE
        self.S1 = 0
        self.S2 = 0
        self.sesion_activa_desde = None

        # >>>> TODO: IMPLEMENTAR CARGA DESDE EXCEL
        # cargar try_counter, bloqueado_desde y block_states

    def guardar_estado_local(self):
        # >>>> TODO: IMPLEMENTAR GUARDADO EN EXCEL
        pass

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
        self.block_states[0] |= (1 << bloque_index) #ni idea que hacer con esto si dejarlo asi o pasasrlo a bajo, esta tomando el valor actual de los bloques y le aplica una mascara para poner en 1 el bit que cambia

    def todos_los_bloques_verificados(self):
        return self.block_states[0] == 0b11111111 #esto tambien esta en funcion separada para preguntar si es el OR del proce lo que se desea aplicar aca

    def login_proceso(self, LogininBlockE: bytearray, ComSE: bytearray,
                      ALUFlagsOut: bytearray, LogOutE: bytearray):

        now = datetime.now()
        print(f"[AUTH_DEBUG] LoginBlockE={LogininBlockE[0]:08b}, bloque_idx={LogininBlockE[0] & 0b00000111}")

        #tiempo?
        if self.try_counter >= 15:
            if self.bloqueado_desde is None:
                self.bloqueado_desde = now
                self.guardar_estado_local()
                print("Acceso bloqueado por exceso de intentos. Temporizador iniciado.")
                return self.S1, self.S2

            if now - self.bloqueado_desde < timedelta(minutes=10):
                print(f"Aún bloqueado. Intenta más tarde.")
                return self.S1, self.S2
            else:
                print("Bloqueo expirado. Reiniciando.")
                self.try_reset()
                self.bloqueado_desde = None
                self.block_states = bytearray([0b00000000])
                self.guardar_estado_local()#HAY QUE HACER AQUI LO DEL EXCEL

        #Logout?
        if LogOutE[0] == 1:
            self.full_reset()
            return self.S1, self.S2

        #Verificar ComSE
        if ComSE[0] != 1:
            print("ComSE no activo")
            return self.S1, self.S2

        #Verificación máxima de intentos
        if self.try_counter >= 15:
            self.bloqueado_desde = now
            self.guardar_estado_local()
            print("Máximo de intentos alcanzado. Bloqueo.")
            return self.S1, self.S2

        #Mux (3 bits LSB) ******************************************************************
        bloque_index = LogininBlockE[0] & 0b00000111 #ESTE AND DE ACA PUEDE APLICARSE CON LAS FUNCIONES DEL PROCE A REALIZAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(f"Intento de login en bloque {bloque_index}")

        #flag ZERO?
        flag_zero = (ALUFlagsOut[0] & 0b0100) != 0 #ACA TAMBIEN SE PUEDE HACER A PUNTA DE FUNCIONES DEL PRCE
        if not flag_zero:
            self.try_counter += 1
            self.guardar_estado_local()
            print("Flag ZERO no está activa. Fallo de verificación.")
            return self.S1, self.S2

        #Actualizar estado del bloque
        print(f"Verificación exitosa en bloque {bloque_index}")
        self.actualizar_estado_bloque(bloque_index)
        self.guardar_estado_local()

        #todos los bloques?
        if self.todos_los_bloques_verificados():
            print(" Todos los bloques han sido validados exitosamente.")
            # >>>> TODO: FUNCIONALIDAD POST LOGIN COMPLETO, INCLUYE EL TIMER DE 30MINS
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
    
    def set_attempts(self, attempts: int):
        """Establece el contador de intentos."""
        self.try_counter = attempts & 0xF
        print(f"[SET] Intentos establecidos: {self.try_counter}")

    def get_attempts(self) -> int:
        """Obtiene el contador de intentos actual."""
        return self.try_counter

#sf = SeguridadFlags()
#for i in range(8):
#        print(f"\ PRUEBA {i + 1}/8")
#
#        # Parámetros de entrada modificables
#        LogininBlockE = bytearray([i])      # Los 3 LSB indican el bloque: 000, 001, ..., 111
#        ComSE         = bytearray([1])      # Señal de comparación activa (1 = sí, 0 = no)
#        ALUFlagsOut   = bytearray([0b0100]) # Solo el bit ZERO en 1: NEG ZERO CARRY OVERFLOW => 0 1 0 0
#        LogOutE       = bytearray([0])      # Logout desactivado
#
#        # Ejecución
#        S1, S2 = sf.login_proceso(LogininBlockE, ComSE, ALUFlagsOut, LogOutE)
#
#        # Resultados y estado del sistema
#        print(f" Entradas:")
#        print(f"    ➤ LogininBlockE = {bin(LogininBlockE[0])[2:].zfill(8)}")
#        print(f"    ➤ ComSE         = {ComSE[0]}")
#        print(f"    ➤ ALUFlagsOut   = {bin(ALUFlagsOut[0])[2:].zfill(8)}")
#        print(f"    ➤ LogOutE       = {LogOutE[0]}")
#
#        print(f"\n Salidas:")
#        print(f"    ➤ S1 = {S1}")
#        print(f"    ➤ S2 = {S2}")
#
#        print(f"\n Estado interno:")
#        print(f"    ➤ Estado de bloques (block_states): {bin(sf.block_states[0])[2:].zfill(8)}")
#        print(f"    ➤ Intentos (try_counter): {sf.try_counter}")