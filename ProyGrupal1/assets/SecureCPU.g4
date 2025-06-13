**Documentación del ISA desarrollado desde cero**

**1. Descripción General**
Este conjunto de instrucciones (ISA) está diseñado para arquitecturas de 64 bits con longitud fija de instrucción de 64 bits (8 bytes), empleando codificación en big-endian. Utiliza un formato limpio y consistentemente matricial que facilita la implementación de un ensamblador de dos pasadas y un pipeline de ejecución eficiente.

**2. Características Principales**

* **Longitud fija**: Todas las instrucciones ocupan exactamente 64 bits, simplificando el fetch y alineación de instrucciones.
* **Formato binario**: Cada instrucción consta de:

  * 8 bits de opcode (bits 63–56)
  * 4 bits de campo SPECIAL (bits 55–52)
  * 4 bits para Rd (bits 51–48)
  * 4 bits para Rn (bits 47–44)
  * 4 bits para Rm (bits 43–40)
  * 32 bits para inmediato o offset (bits 39–8)
  * 8 bits de campo extra (bits 7–0)
* **Sistema de registros**:

  * Registros de propósito general R0–R15 (4 bits)
  * Registros "wide" W1–W9 codificados como R0–R8 internamente (4 bits)
  * Registro especial D0 (alias de W10 → 9 decimal → 1001)
  * Claves criptográficas Kx.y codificadas en 4 bits (2 bits para clave, 2 bits para palabra)
  * Pasword registers Px (4 bits)
* **Campo SPECIAL**: Bits que indican si Rd/Rn/Rm son registros "wide" o de otro tipo, y codifican modos especiales para instrucciones de memoria e I/O.
* **Dos pasadas de ensamblador**:

  1. Primera pasada: recolecta etiquetas y calcula direcciones de instrucción.
  2. Segunda pasada: valida sintaxis, expande pseudoinstrucciones, codifica ramas usando offsets relativos, genera cadenas binarias.

**3. Categorías de Operaciones**

1. **Aritméticas (REG, REG, REG)**:

   * ADD, ADDS (con k-word), SUB, ADC, SBC, MUL, DIV, AND, ORR, EOR, BIC, LSL, LSR, ASR, ROR

2. **Inmediatos (REG, REG, IMM)**:

   * ADDI, SUBI, ADCI, SBCI, MULI, DIVI, ANDI, ORRI, EORI, BICI, LSLI, LSRI, ASRI, RORI

3. **Movimiento de datos**:

   * **Reg a reg**: MOV, MVN
   * **Inmediato**: MOVI, MVNI

4. **Comparaciones**:

   * **Registro vs registro**: CMP, CMN, TST, TEQ
   * **Registro vs inmediato**: CMPI, CMNI, TSTI, TEQI
   * **Comparación de contraseña**: CMPS (usa PASS register y genera campo inmediato cero)

5. **Bifurcaciones**:

   * B, BEQ, BNE, BLT, BGT (offset de instrucciones calculado \* 8 bytes)

6. **Especiales**:

   * SWI (software interrupt), NOP, CLEAR, LOGOUT

7. **Memoria**:

   * Carga/almacena en memoria global o datos:

     * LDR, LDRB  (destino en Rd)
     * STR, STRB  (fuente en Rm)
   * Modo de direccionamiento: G\[D/V/P]\[Registro, #offset]

8. **Entrada/Salida**:

   * PRINTI, PRINTS, PRINTB (imprime datos de memoria)

9. **Seguridad/Cifrado**:

   * STRK (almacena clave y valor inmediato)
   * STRPASS (almacena palabra de contraseña en PASS register)

10. **Pseudoinstrucciones**:

    * AUTHCMP → expande a 8 CMPS consecutivas
    * TEA (prepara registros W6 y W7)
    * TEAENC #n, kx → secuencia de NOPs y operaciones ADD/EOR/LSL/LSR según ronda n
    * TEAD #n, kx → mezcla de NOPs, LSL/EOR/Sub ADD según ronda n

**4. Flujo de Compilación**

1. **Lexer**: tokeniza etiquetas, opcodes, registros, memoria, inmadiatos, comas.
2. **Parser**: valida secuencia de tipos contra patrones predefinidos para cada instrucción (incluye variantes para pseudoinstrucciones).
3. **Encoder**: convierte tokens en cadenas de bits de 64 bits:

   * Determina opcode y campo special.
   * Codifica registros e inmediato.
   * Expande pseudoinstrucciones recursivamente.
4. **Generación de binario**:

   * Convierte cada cadena de bits a entero y a 8 bytes big-endian.
   * Guarda resultado en `Assets/instruction_mem.bin`.

**5. Ventajas y Aplicaciones**

* Alta consistencia y predictibilidad en longitud de instrucción.
* Soporte nativo para cifrado y autenticación (STRK, STRPASS, AUTHCMP).
* Pseudoinstrucciones para facilitar rutinas complejas (TEA, TEAENC, TEAD).
* Diseño modular: lexer, parser, encoder separados para facilidad de mantenimiento.
* Adecuado para sistemas embebidos o CPUs educativas con pipeline y memoria de instrucciones simple.

**6. Conclusión**
Este ISA combina la simplicidad de un formato fijo con potentes extensiones para cifrado y autenticación, soporte de direccionamiento de memoria flexible e instrucciones de I/O dedicadas, ofreciendo una base sólida para implementaciones de CPU didácticas o prototipos de arquitecturas de 64 bits.