from __future__ import annotations
"""AuthenticationUnit – versión compatiblemente extendida
=========================================================
Incluye:
• Lógica de bloqueo 15 × 15 min
• Auto‑logout tras 15 min de sesión segura
• Métodos *compatibilidad* (set/get_block_states, etc.) para que el resto
  del sistema que aún invoque la API antigua no rompa.
• Protegido con *threading.Lock* para seguridad en entorno multihilo.
"""

from datetime import datetime, timedelta
from threading import Lock
from typing import Optional, Tuple


class AuthenticationProcess:
    # ──────────── parámetros de diseño ────────────
    ATTEMPT_LIMIT: int = 15       # intentos fallidos permitidos
    LOCKOUT_MINUTES: int = 15     # minutos de bloqueo tras exceso de fallos
    SESSION_MINUTES: int = 15     # vigencia de S1/S2 tras login completo

    # ─────── singleton thread‑safe ───────
    _instance: "Optional[AuthenticationProcess]" = None
    _inst_lock: Lock = Lock()

    def __new__(cls):
        with cls._inst_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        #  —— estado principal ——
        self.try_counter: int = 0          # fallos consecutivos
        self.block_states: int = 0x00      # bitmap de 8 bits
        self.S1: int = 0
        self.S2: int = 0

        #  —— timestamps ——
        self.lockout_start: Optional[datetime] = None  # inicio del bloqueo
        self.session_start: Optional[datetime] = None  # inicio de sesión segura

        self._initialized = True
        self._print("Instancia creada")

    # ------------------------------------------------------------------
    #  utilidades internas
    # ------------------------------------------------------------------
    def _print(self, msg: str) -> None:
        print(f"[AUTH] {msg}")

    def _reset_try_counter(self) -> None:
        self.try_counter = 0
        self._print("try_counter = 0")

    def _reset_session(self) -> None:
        """Apaga S1/S2 y limpia bloques."""
        self.S1 = self.S2 = 0
        self.block_states = 0x00
        self.session_start = None
        self._print("Sesión segura reiniciada")

    # ------------------------------------------------------------------
    #  API *compatibilidad* (para código heredado) –––––––––––––––––––––––
    # ------------------------------------------------------------------
    def set_block_states(self, value: int):
        self.block_states = value & 0xFF
        self._print(f"block_states <- {self.block_states:08b}")

    def get_block_states(self) -> int:
        return self.block_states & 0xFF

    # alias Legacy: sesión activa desde (solo para bloqueo, no para session)
    def set_sesion_activa_desde(self, hora: Optional[datetime]):
        self.lockout_start = hora
        self._print(f"lockout_start <- {hora}")

    def get_sesion_activa_desde(self) -> Optional[datetime]:
        return self.lockout_start

    # alias Legacy: reset simples
    def try_reset(self):
        self._reset_try_counter()

    def reset_flags(self):  # logout explícito
        self._reset_session()

    def full_reset(self):
        self._reset_try_counter()
        self._reset_session()
        self.lockout_start = None
        self._print("full_reset() ejecutado")

    # ------------------------------------------------------------------
    #  lógica principal de autenticación
    # ------------------------------------------------------------------
    def login_proceso(
        self,
        LogininBlockE: bytearray,
        ComSE: bytearray,
        ALUFlagsOut: bytearray,
        LogOutE: bytearray,
    ) -> Tuple[int, int]:
        """Un ciclo de evaluación de la unidad de autenticación.

        Se mantiene la firma original para compatibilidad con el datapath.
        """
        now = datetime.now()

        # 0) Logout inmediato ------------------------------------------------
        if LogOutE[0] == 1:
            self._print("LogOutE detectado → full_reset")
            self.full_reset()
            return self.S1, self.S2

        # 1) Auto‑logout tras vencimiento de la sesión ----------------------
        if self.S1 and self.S2 and self.session_start is not None:
            if now - self.session_start >= timedelta(minutes=self.SESSION_MINUTES):
                self._print("Sesión segura expirada – auto‑logout")
                self._reset_session()

        # 2) Ventana de bloqueo por fallos ----------------------------------
        if self.try_counter >= self.ATTEMPT_LIMIT:
            if self.lockout_start is None:
                self.lockout_start = now
                self._print("Límite de intentos alcanzado – bloqueo iniciado")
                return self.S1, self.S2

            if now - self.lockout_start < timedelta(minutes=self.LOCKOUT_MINUTES):
                self._print("En periodo de bloqueo – intento ignorado")
                return self.S1, self.S2

            # bloqueo caducó
            self._print("Bloqueo expirado – se restauran intentos")
            self.lockout_start = None
            self._reset_try_counter()
            self.block_states = 0x00

        # 3) Si no estamos en una instrucción CMPS, salir -------------------
        if ComSE[0] != 1:
            return self.S1, self.S2

        # 4) Procesar comparación -------------------------------------------
        bloque_idx: int = LogininBlockE[0] & 0b00000111  # 0‑7
        flag_zero: bool = bool(ALUFlagsOut[0] & 0b0100)  # NZCV bit 2 (Z)

        if not flag_zero:
            # fallo de autenticación
            self.try_counter += 1
            self._print(
                f"Fallo en bloque {bloque_idx} → try_counter={self.try_counter}/{self.ATTEMPT_LIMIT}"
            )
            return self.S1, self.S2

        # 5) Éxito en este bloque
        self.block_states |= 1 << bloque_idx
        self.try_counter = 0  # opcional: resetea tras éxito
        self._print(f"Bloque {bloque_idx} verificado ✔  block_states={self.block_states:08b}")

        # 6) ¿Se completaron los 8 bloques?
        if self.block_states == 0xFF:
            self.S1 = self.S2 = 1
            self.session_start = now
            self._print("Todos los bloques correctos – sesión segura activada")

        return self.S1, self.S2
