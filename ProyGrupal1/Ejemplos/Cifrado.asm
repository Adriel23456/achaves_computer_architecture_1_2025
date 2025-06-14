.login:
	MOVI R1, #1
	MOVI R2, #2
	MOVI R3, #3
	MOVI R4, #4
	MOVI R5, #5
	MOVI R6, #6
	MOVI R7, #7
	MOVI R8, #8
	NOP
	NOP
	NOP
	NOP
	AUTHCMP
	NOP
	NOP
	NOP
	NOP

.set_up_cript_key:
	STRK k0.0 #0xDEADBEEF
	STRK k0.1 #0xDEADBEEF
	STRK k0.2 #0xDEADBEEF
	STRK k0.3 #0xDEADBEEF

.tea_crypt_buf:
	MOV w3, R0
	NOP
	NOP
	NOP
	NOP
.Lblock_Loop:
	LDR w4, D[w3, #0]
	LDR w5, D[w3, #4]
	NOP
	NOP
	NOP
	NOP
	TEA #0, #0x0
.Lloop:
	TEAENC #1, k0
	TEAENC #2
	TEAENC #3, k0
	TEAENC #4, k0
	TEAENC #5
	TEAENC #6, k0
	TEAENC #7
	BNE .Lloop
	NOP
	NOP
	NOP
	NOP
	STR w4, D[w3, #0]
	STR w5, D[w3, #4]
	ADDI w3, w3, #8
	SUBI w2, w2, #1
	BNE .Lblock_Loop
	NOP
	NOP
	NOP
	NOP
.Ldone:
	SWI