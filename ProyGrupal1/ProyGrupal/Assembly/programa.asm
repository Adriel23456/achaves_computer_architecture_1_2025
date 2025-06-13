; Archivo de prueba para verificar codificación de instrucciones
; Cada sección prueba un grupo de instrucciones con diferentes operandos

; ==============================================
; INSTRUCCIONES ARITMÉTICAS (REG, REG, REG)
; ==============================================
ADD R1, R2, R3          ; Suma básica
ADD R0, R1, R2          ; Con registro 0
ADD R7, R6, R5          ; Registros altos

ADDS R1, R2, k1.0         ; Suma con clave
ADDS R0, R3, k2.0         ; Suma con otra clave

SUB R4, R5, R6          ; Resta
SUB R0, R0, R1          ; Resta con mismo registro destino

ADC R2, R3, R4          ; Suma con carry
SBC R5, R6, R7          ; Resta con borrow

MUL R1, R2, R3          ; Multiplicación
MUL R0, R4, R5          ; Multiplicación variante

DIV R6, R7, R1          ; División
DIV R2, R3, R4          ; División variante

; ==============================================
; OPERACIONES LÓGICAS (REG, REG, REG)
; ==============================================
AND R1, R2, R3          ; AND lógico
AND R0, R1, R2          ; AND con R0

ORR R4, R5, R6          ; OR lógico
ORR R7, R0, R1          ; OR variante

EOR R2, R3, R4          ; XOR exclusivo
EOR R5, R6, R7          ; XOR variante

BIC R1, R2, R3          ; Bit clear
BIC R0, R4, R5          ; Bit clear variante

; ==============================================
; OPERACIONES DE DESPLAZAMIENTO (REG, REG, REG)
; ==============================================
LSL R1, R2, R3          ; Shift izquierda lógico
LSL R0, R1, R2          ; LSL variante

LSR R4, R5, R6          ; Shift derecha lógico
LSR R7, R0, R1          ; LSR variante

ASR R2, R3, R4          ; Shift derecha aritmético
ASR R5, R6, R7          ; ASR variante

ROR R1, R2, R3          ; Rotación derecha
ROR R0, R4, R5          ; ROR variante

; ==============================================
; INSTRUCCIONES INMEDIATAS (REG, REG, IMM)
; ==============================================
ADDI R1, R2, #10        ; Suma inmediata
ADDI R0, R1, #255       ; Suma inmediata máxima
ADDI R3, R4, #0         ; Suma con cero

SUBI R2, R3, #5         ; Resta inmediata
SUBI R5, R6, #100       ; Resta inmediata mayor

ADCI R1, R2, #8         ; Suma con carry inmediata
SBCI R3, R4, #12        ; Resta con borrow inmediata

MULI R0, R1, #2         ; Multiplicación inmediata
MULI R2, R3, #16        ; Multiplicación por potencia de 2

DIVI R4, R5, #4         ; División inmediata
DIVI R6, R7, #8         ; División variante

ANDI R1, R2, #15        ; AND inmediato (máscara)
ANDI R0, R3, #255       ; AND inmediato completo

ORRI R2, R3, #128       ; OR inmediato
ORRI R4, R5, #7         ; OR inmediato pequeño

EORI R1, R2, #85        ; XOR inmediato
EORI R3, R4, #170       ; XOR inmediato patrón

BICI R5, R6, #31        ; Bit clear inmediato
BICI R0, R1, #240       ; Bit clear variante

LSLI R2, R3, #1         ; Shift izquierda inmediato
LSLI R4, R5, #8         ; Shift izquierda byte

LSRI R1, R2, #2         ; Shift derecha inmediato
LSRI R6, R7, #4         ; Shift derecha variante

ASRI R3, R4, #3         ; Shift aritmético inmediato
ASRI R0, R1, #7         ; Shift aritmético variante

RORI R5, R6, #1         ; Rotación inmediata
RORI R2, R3, #16        ; Rotación media

; ==============================================
; MOVIMIENTO DE DATOS
; ==============================================
MOV R1, R2              ; Movimiento básico
MOV R0, R7              ; Mover a R0
MOV R3, R0              ; Mover desde R0

MVN R4, R5              ; Movimiento negado
MVN R6, R1              ; MVN variante

MOVI R1, #42            ; Mover inmediato
MOVI R0, #0             ; Mover cero
MOVI R7, #255           ; Mover máximo

MVNI R2, #10            ; Mover inmediato negado
MVNI R3, #128           ; MVNI variante

; ==============================================
; INSTRUCCIONES DE COMPARACIÓN
; ==============================================
CMP R1, R2              ; Comparación básica
CMP R0, R3              ; Comparación con R0
CMP R7, R1              ; Comparación variante

CMPS R1, P1   ; Comparación con password
CMPS R2, P2     ; Comparación con otro password

CMN R3, R4              ; Comparación negativa
CMN R0, R5              ; CMN con R0

TST R1, R2              ; Test bits
TST R6, R7              ; Test variante

TEQ R2, R3              ; Test igualdad
TEQ R4, R5              ; TEQ variante

CMPI R1, #10            ; Comparar con inmediato
CMPI R0, #0             ; Comparar con cero
CMPI R7, #255           ; Comparar con máximo

CMNI R2, #5             ; Comparación negativa inmediata
CMNI R3, #20            ; CMNI variante

TSTI R4, #15            ; Test inmediato
TSTI R1, #128           ; Test bit alto

TEQI R5, #42            ; Test igualdad inmediato
TEQI R0, #1             ; TEQI variante

; ==============================================
; INSTRUCCIONES DE BIFURCACIÓN
; ==============================================
B .loop_start            ; Salto incondicional
B .end_program           ; Salto al final

BEQ .equal_label         ; Salto si igual
BNE .not_equal_label     ; Salto si no igual
BLT .less_than_label     ; Salto si menor
BGT .greater_than_label  ; Salto si mayor

; ==============================================
; OPERACIONES ESPECIALES
; ==============================================
SWI                     ; Interrupción software
NOP                     ; No operación
NOP                     ; Otra NOP para prueba

; ==============================================
; INSTRUCCIONES DE MEMORIA
; ==============================================

LDR R4, G[R5, #4]        ; Cargar con índice registro
LDR R7, D[R8, #5]       ; Cargar dirección

STR R4, G[R5, #4]        ; Almacenar con índice
STR R7, D[R8, #5]         ; Almacenar en variable

LDRB R3, D[R4, #1]       ; Cargar byte con offset
LDRB R5, G[R6, #1]

STRB R1, D[R2, #2]           ; Almacenar byte
STRB R5, G[R6, #2]       ; Almacenar byte con offset
; ==============================================
; INSTRUCCIONES ESPECIALES DEL SISTEMA
; ==============================================
PRINTI G[R6, #1]          ; Imprimir entero


PRINTS D[R6, #1]         ; Imprimir string


PRINTB G[R6, #1]           ; Imprimir binario


LOGOUT                  ; Cerrar sesión

STRK k0.1 #1             ; Almacenar clave 1
STRK k0.2 #2             ; Almacenar clave 2
STRK k0.3 #3             ; Almacenar clave 3

STRPASS P1 #1 ; Almacenar password 1
STRPASS P2 #2  ; Almacenar password 2
STRPASS P3 #3    ; Almacenar password 3

AUTHCMP                 ; Comparar autenticación

; ==============================================
; INSTRUCCIONES TEA
; ==============================================
TEA #10, #20            ; TEA con dos inmediatos
TEA #5, #15             ; TEA variante
TEA #0, #255            ; TEA casos extremos

; ==============================================
; ETIQUETAS PARA BIFURCACIONES
; ==============================================
.loop_start:
ADDI R1, R1, #1         ; Incrementar contador
CMPI R1, #10            ; Comparar con límite
BLT .loop_start          ; Repetir si menor

.equal_label:
MOVI R0, #1             ; Marcar como igual
B .end_program

.not_equal_label:
MOVI R0, #2             ; Marcar como no igual
B .end_program

.less_than_label:
MOVI R0, #3             ; Marcar como menor
B .end_program

.greater_than_label:
MOVI R0, #4             ; Marcar como mayor

.end_program:
SWI                     ; Terminar programa