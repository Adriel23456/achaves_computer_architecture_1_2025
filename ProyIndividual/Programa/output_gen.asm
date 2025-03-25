section .data
    ; File paths and error messages
    input_file_path: db "input.img", 0
    output_file_path: db "output.img", 0
    error_open: db "Error: No se pudo abrir el archivo input.img", 10, 0
    error_open_len: equ $ - error_open
    error_read: db "Error: No se pudieron leer datos del archivo input.img", 10, 0
    error_read_len: equ $ - error_read
    error_empty: db "Error: El archivo input.img está vacío", 10, 0
    error_empty_len: equ $ - error_empty
    error_create: db "Error: No se pudo crear el archivo output.img", 10, 0
    error_create_len: equ $ - error_create
    error_write: db "Error: No se pudieron escribir datos en el archivo output.img", 10, 0
    error_write_len: equ $ - error_write
    
    ; Buffers
    input_buffer: times 4 db 0   ; Buffer for 2x2 block (4 bytes)
    output_buffer: times 16 db 0  ; Buffer for 4x4 block (16 bytes)

section .bss
    input_fd: resq 1    ; File descriptor for input file
    output_fd: resq 1   ; File descriptor for output file
    bytes_read: resq 1  ; Number of bytes read

section .text
global _start

_start:
    ; Open input file
    mov rax, 2          ; syscall: open
    mov rdi, input_file_path
    mov rsi, 0          ; O_RDONLY
    mov rdx, 0644o      ; File mode (not used for O_RDONLY)
    syscall
    
    ; Check for error
    cmp rax, 0
    jl open_error
    
    ; Save input file descriptor
    mov [input_fd], rax
    
    ; Create output file
    mov rax, 2          ; syscall: open
    mov rdi, output_file_path
    mov rsi, 0x241      ; O_WRONLY | O_CREAT | O_TRUNC
    mov rdx, 0644o      ; File mode (rw-r--r--)
    syscall
    
    ; Check for error
    cmp rax, 0
    jl create_error
    
    ; Save output file descriptor
    mov [output_fd], rax
    
    ; Main processing loop
process_loop:
    ; Read 4 bytes from input file
    mov rax, 0          ; syscall: read
    mov rdi, [input_fd]
    mov rsi, input_buffer
    mov rdx, 4          ; Read 4 bytes
    syscall
    
    ; Check for error or end of file
    cmp rax, 0
    jl read_error
    je end_processing    ; End of file
    
    ; Store bytes read
    mov [bytes_read], rax
    
    ; Check if we have enough bytes for processing
    cmp qword [bytes_read], 4
    jl end_processing    ; Not enough data for a complete block
    
    ; Process the 2x2 block to create a 4x4 block
    call process_block
    
    ; Write the 4x4 block to output file
    mov rax, 1          ; syscall: write
    mov rdi, [output_fd]
    mov rsi, output_buffer
    mov rdx, 16         ; Write 16 bytes
    syscall
    
    ; Check for error
    cmp rax, 16
    jne write_error
    
    ; Continue with the next block
    jmp process_loop

end_processing:
    ; Close input file
    mov rax, 3          ; syscall: close
    mov rdi, [input_fd]
    syscall
    
    ; Close output file
    mov rax, 3          ; syscall: close
    mov rdi, [output_fd]
    syscall
    
    ; Exit program
    mov rax, 60         ; syscall: exit
    xor rdi, rdi        ; status: 0
    syscall

; Error handlers
open_error:
    mov rax, 1          ; syscall: write
    mov rdi, 2          ; file: stderr
    mov rsi, error_open
    mov rdx, error_open_len
    syscall
    jmp exit_error

read_error:
    mov rax, 1          ; syscall: write
    mov rdi, 2          ; file: stderr
    mov rsi, error_read
    mov rdx, error_read_len
    syscall
    jmp exit_error

create_error:
    mov rax, 1          ; syscall: write
    mov rdi, 2          ; file: stderr
    mov rsi, error_create
    mov rdx, error_create_len
    syscall
    jmp exit_error

write_error:
    mov rax, 1          ; syscall: write
    mov rdi, 2          ; file: stderr
    mov rsi, error_write
    mov rdx, error_write_len
    syscall
    jmp exit_error

exit_error:
    mov rax, 60         ; syscall: exit
    mov rdi, 1          ; status: 1
    syscall

; Process a 2x2 block to create a 4x4 block using bilinear interpolation
process_block:
    ; Load the 4 corner values (a, b, c, d) from input buffer
    movzx r8, byte [input_buffer]      ; a
    movzx r9, byte [input_buffer + 1]  ; b
    movzx r10, byte [input_buffer + 2] ; c
    movzx r11, byte [input_buffer + 3] ; d
    
    ; Set the original corner values in the output buffer
    mov [output_buffer], r8b      ; a
    mov [output_buffer + 3], r9b  ; b
    mov [output_buffer + 12], r10b ; c
    mov [output_buffer + 15], r11b ; d
    
    ; Calculate a1 = int((2/3)*a + (1/3)*b) = (2*a + b) / 3
    mov rax, r8
    imul rax, 2
    add rax, r9
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 1], al   ; Store a1
    
    ; Calculate b1 = int((1/3)*a + (2/3)*b) = (a + 2*b) / 3
    mov rax, r9
    imul rax, 2
    add rax, r8
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 2], al   ; Store b1
    
    ; Calculate c1 = int((2/3)*a + (1/3)*c) = (2*a + c) / 3
    mov rax, r8
    imul rax, 2
    add rax, r10
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 4], al   ; Store c1
    mov r12, rax                  ; Save c1 for later use
    
    ; Calculate g1 = int((1/3)*a + (2/3)*c) = (a + 2*c) / 3
    mov rax, r10
    imul rax, 2
    add rax, r8
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 8], al   ; Store g1
    mov r13, rax                  ; Save g1 for later use
    
    ; Calculate k1 = int((2/3)*c + (1/3)*d) = (2*c + d) / 3
    mov rax, r10
    imul rax, 2
    add rax, r11
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 13], al  ; Store k1
    
    ; Calculate l1 = int((1/3)*c + (2/3)*d) = (c + 2*d) / 3
    mov rax, r11
    imul rax, 2
    add rax, r10
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 14], al  ; Store l1
    
    ; Calculate f1 = int((2/3)*b + (1/3)*d) = (2*b + d) / 3
    mov rax, r9
    imul rax, 2
    add rax, r11
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 7], al   ; Store f1
    mov r14, rax                  ; Save f1 for later use
    
    ; Calculate j1 = int((1/3)*b + (2/3)*d) = (b + 2*d) / 3
    mov rax, r11
    imul rax, 2
    add rax, r9
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 11], al  ; Store j1
    mov r15, rax                  ; Save j1 for later use
    
    ; Calculate d1 = int((2/3)*c1 + (1/3)*f1) = (2*c1 + f1) / 3
    mov rax, r12                  ; c1
    imul rax, 2
    add rax, r14                  ; f1
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 5], al   ; Store d1
    
    ; Calculate e1 = int((1/3)*c1 + (2/3)*f1) = (c1 + 2*f1) / 3
    mov rax, r14                  ; f1
    imul rax, 2
    add rax, r12                  ; c1
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 6], al   ; Store e1
    
    ; Calculate h1 = int((2/3)*g1 + (1/3)*j1) = (2*g1 + j1) / 3
    mov rax, r13                  ; g1
    imul rax, 2
    add rax, r15                  ; j1
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 9], al   ; Store h1
    
    ; Calculate i1 = int((1/3)*g1 + (2/3)*j1) = (g1 + 2*j1) / 3
    mov rax, r15                  ; j1
    imul rax, 2
    add rax, r13                  ; g1
    mov rbx, 3
    xor rdx, rdx
    div rbx
    mov [output_buffer + 10], al  ; Store i1
    
    ret