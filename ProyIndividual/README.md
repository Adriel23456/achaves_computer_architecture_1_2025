# Interpolación Bilineal en Ensamblador x86-64

Autor: Adriel Sebastian Chaves Salazar

## Descripción del Proyecto

Este proyecto implementa un algoritmo de interpolación bilineal en lenguaje ensamblador x86-64. El sistema procesa imágenes en escala de grises, selecciona un cuadrante específico y aplica interpolación bilineal para aumentar su resolución, transformando bloques de 2×2 píxeles en bloques de 4×4 píxeles con valores interpolados.

## Tecnologías Utilizadas

- **Sistema Operativo**: Linux/Ubuntu
- **ISA**: x86-64 de 64 bits
- **Ensamblador**: NASM (Netwide Assembler)
- **Lenguaje de alto nivel**: Python 3 con bibliotecas:
  - Tkinter para la interfaz gráfica
  - PIL/Pillow para procesamiento de imágenes
  - NumPy para manipulación de matrices de píxeles
- **Estructura de datos**:
  - Entrada: Bloques de 2×2 píxeles en archivos binarios
  - Salida: Bloques de 4×4 píxeles interpolados

## Explicación del Código Ensamblador

El código ensamblador realiza la interpolación bilineal leyendo bloques de 2×2 píxeles desde un archivo binario, calculando los valores interpolados, y escribiendo bloques de 4×4 píxeles al archivo de salida.

### Secciones del Código

#### Sección de Datos (.data)

```assembly
section .data
    ; File paths and error messages
    input_file_path: db "input.img", 0
    output_file_path: db "output.img", 0
    ...
    ; Buffers
    input_buffer: times 4 db 0   ; Buffer for 2x2 block (4 bytes)
    output_buffer: times 16 db 0  ; Buffer for 4x4 block (16 bytes)
```

Esta sección define:
- Rutas de los archivos de entrada/salida terminados en null (0)
- Mensajes de error para distintas situaciones
- Dos buffers:
  - `input_buffer`: Almacena 4 bytes (un bloque de 2×2 píxeles)
  - `output_buffer`: Almacena 16 bytes (un bloque de 4×4 píxeles)

#### Sección BSS (.bss)

```assembly
section .bss
    input_fd: resq 1    ; File descriptor for input file
    output_fd: resq 1   ; File descriptor for output file
    bytes_read: resq 1  ; Number of bytes read
```

Esta sección reserva memoria para:
- Descriptores de archivo de entrada y salida (8 bytes cada uno con `resq 1`)
- Variable para almacenar la cantidad de bytes leídos

#### Punto de Entrada y Manejo de Archivos

```assembly
_start:
    ; Open input file
    mov rax, 2          ; syscall: open
    mov rdi, input_file_path
    mov rsi, 0          ; O_RDONLY
    mov rdx, 0644o      ; File mode (not used for O_RDONLY)
    syscall
```

Instrucciones clave:
- `mov rax, 2`: Prepara la llamada al sistema "open" (código 2)
- `mov rdi, input_file_path`: Primer parámetro - ruta del archivo
- `mov rsi, 0`: Segundo parámetro - modo de solo lectura (O_RDONLY)
- `syscall`: Ejecuta la llamada al sistema
- `cmp rax, 0` y `jl open_error`: Verificación de error (salta si es negativo)

El código utiliza las mismas instrucciones para crear el archivo de salida, pero con diferentes banderas (`0x241` = O_WRONLY | O_CREAT | O_TRUNC).

#### Bucle Principal de Procesamiento

```assembly
process_loop:
    ; Read 4 bytes from input file
    mov rax, 0          ; syscall: read
    mov rdi, [input_fd]
    mov rsi, input_buffer
    mov rdx, 4          ; Read 4 bytes
    syscall
```

Este bucle:
1. Lee 4 bytes (un bloque de 2×2 píxeles) del archivo de entrada
2. Verifica errores y fin de archivo
3. Llama a `process_block` para realizar la interpolación bilineal
4. Escribe 16 bytes (bloque de 4×4 píxeles) al archivo de salida
5. Vuelve al inicio para procesar el siguiente bloque

#### Algoritmo de Interpolación Bilineal

```assembly
process_block:
    ; Load the 4 corner values (a, b, c, d) from input buffer
    movzx r8, byte [input_buffer]      ; a
    movzx r9, byte [input_buffer + 1]  ; b
    movzx r10, byte [input_buffer + 2] ; c
    movzx r11, byte [input_buffer + 3] ; d
```

Instrucciones clave de interpolación:

1. `movzx r8-r11, byte [input_buffer+offset]`: Carga los 4 valores de esquina con extensión de cero
2. `mov [output_buffer+offset], r8b-r11b`: Coloca los valores originales en las esquinas del buffer de salida
3. Para cada valor interpolado (a1, b1, c1, etc.):
   - `imul rax, 2`: Multiplica por 2 (para calcular el peso de 2/3)
   - `add rax, reg`: Suma el segundo valor (para la ponderación de 1/3)
   - `mov rbx, 3`: Prepara el divisor (3)
   - `xor rdx, rdx`: Limpia el registro rdx para la división
   - `div rbx`: Divide rax por 3, resultado en rax
   - `mov [output_buffer+offset], al`: Almacena el byte bajo (al) del resultado

La interpolación sigue la fórmula: `resultado = (2*valor1 + valor2)/3` o `resultado = (valor1 + 2*valor2)/3` dependiendo del píxel.

#### Gestión de Errores

```assembly
open_error:
    mov rax, 1          ; syscall: write
    mov rdi, 2          ; file: stderr
    mov rsi, error_open
    mov rdx, error_open_len
    syscall
    jmp exit_error
```

El código maneja cuatro tipos de errores:
- Error al abrir el archivo de entrada
- Error al leer datos
- Error al crear el archivo de salida
- Error al escribir datos

Cada manejador imprime un mensaje en stderr y termina con código de error.

## Detalles del Algoritmo de Interpolación

El algoritmo implementa el proceso de interpolación bilineal para transformar un bloque de 2×2 píxeles en un bloque de 4×4 siguiendo estos pasos:

1. Los valores originales (a, b, c, d) se colocan en las esquinas del bloque 4×4
2. Los bordes se calculan primero, usando interpolación lineal con pesos 2/3 y 1/3:
   - Borde superior: a1 = (2a+b)/3, b1 = (a+2b)/3
   - Borde izquierdo: c1 = (2a+c)/3, g1 = (a+2c)/3
   - Borde derecho: f1 = (2b+d)/3, j1 = (b+2d)/3
   - Borde inferior: k1 = (2c+d)/3, l1 = (c+2d)/3
3. Los píxeles centrales se calculan usando los bordes calculados en el paso 2:
   - d1 = (2c1+f1)/3, e1 = (c1+2f1)/3
   - h1 = (2g1+j1)/3, i1 = (g1+2j1)/3

Esta implementación usa ponderaciones de 2/3 y 1/3 para dar mayor peso a los píxeles más cercanos, creando una transición suave entre los valores originales.

## Ejecución del Sistema

El flujo de trabajo completo del sistema es:

1. El programa Python carga y redimensiona una imagen a 512×512 píxeles
2. El usuario selecciona uno de los 16 cuadrantes de 128×128 píxeles
3. Python escribe el cuadrante seleccionado en formato binario como `input.img`
4. Un script Bash compila y ejecuta el código ensamblador
5. El ensamblador lee `input.img`, aplica interpolación bilineal y genera `output.img`
6. Python lee `output.img` y muestra la imagen interpolada resultante (256×256 píxeles)

## Notas Adicionales

- El sistema está optimizado para imágenes de 512×512 píxeles, ya que este tamaño facilita la división en cuadrantes de 128×128 píxeles, que a su vez son adecuados para la interpolación a 256×256 píxeles.
- La organización por bloques (en lugar de organización lineal) simplifica significativamente el código ensamblador al evitar cálculos complejos de índices.