section .data
    buffer: times 44 db 0      ; Space for 11 values (11*4=44 bytes)
    hex_chars: db "0123456789abcdef"
    out_buf: times 3 db 0      ; 2 hex digits + newline

section .text
global _start
_start:
    ; Set up buffer address
    mov rdi, buffer
    
    ; Load seed value (0x53)
    mov al, 0x53
    
    ; Store seed as first value
    mov [rdi], al
    
    ; Print initial seed
    call print_hex_byte
    
    ; Initialize counter and move to next position
    mov rcx, 10         ; Counter for 10 values
    add rdi, 4          ; Next position
    
generate_loop:
    ; Extract bit 1 from right
    mov r8b, al
    shr r8b, 1
    and r8b, 1
    
    ; Extract bit 2 from right
    mov r9b, al
    shr r9b, 2
    and r9b, 1
    
    ; XOR for feedback
    xor r9b, r8b
    
    ; Shift right and insert feedback bit
    shr al, 1
    shl r9b, 7
    or al, r9b
    
    ; Keep only 8 bits (already handled by using AL)
    
    ; Store value and print it
    mov [rdi], al
    call print_hex_byte
    
    ; Advance to next position
    add rdi, 4
    
    ; Decrement counter and loop
    dec rcx
    jnz generate_loop
    
    ; Exit program
    mov rax, 60         ; syscall: exit
    xor rdi, rdi        ; status: 0
    syscall

; Function to print hex byte in AL
print_hex_byte:
    push rax            ; Save registers
    push rcx
    push rdx
    push rdi
    push rsi
    
    ; Set up out_buf
    mov rdi, out_buf
    mov rsi, hex_chars
    
    ; First hex digit (high nibble)
    mov rdx, rax
    shr rdx, 4          ; High nibble
    and rdx, 0xF
    mov dl, [rsi + rdx] ; Get hex character
    mov [rdi], dl       ; Store to output buffer
    
    ; Second hex digit (low nibble)
    mov rdx, rax
    and rdx, 0xF        ; Low nibble
    mov dl, [rsi + rdx] ; Get hex character
    mov [rdi + 1], dl   ; Store to output buffer
    
    ; Add newline
    mov byte [rdi + 2], 10 ; Newline character
    
    ; Write to stdout
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; file: stdout
    mov rsi, out_buf    ; buffer
    mov rdx, 3          ; size: 3 bytes
    syscall
    
    pop rsi             ; Restore registers
    pop rdi
    pop rdx
    pop rcx
    pop rax
    ret
