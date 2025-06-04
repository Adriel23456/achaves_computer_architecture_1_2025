; Pruebas de operaciones aritméticas
ADD R1, R2, R3
SUB R4, R5, R6
ADDI R7, R8, #10

; Pruebas de movimiento
MOVI R9, #0xFF
STR R10, G[R1, #4]

; Pruebas de encriptación
TEA #0, #0x9E3779B9
STRK k0.0 #0x12345678
STRPASS 0 #0x87654321

; Pruebas especiales
NOP
LOGOUT

; Prueba de salto y etiqueta
.Linicio
B .Linicio

; Print literal
PRINTL #0x48  ; representa 'H'

; Línea inválida para ver el manejo de errores
INVALID R1, R2
