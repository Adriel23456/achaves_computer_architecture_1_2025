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
	CMPS R1, P1
	CMPS R2, P2
	CMPS R3, P3
	CMPS R4, P4
	CMPS R5, P5
	CMPS R6, P6
	CMPS R7, P7
	CMPS R8, P8
	NOP
	NOP
	NOP
	NOP
.set_up_cript_key:
	STRK k0.0 #0xDEADBEEF
	STRK k0.1 #0xDEADBEEF
	STRK k0.2 #0xDEADBEEF
	STRK k0.3 #0xDEADBEEF
	NOP
	NOP
	NOP
	NOP
.tdea_decrypt_buf:
	MOV w3, R0
	NOP
	NOP
	NOP
	NOP
.Lblock_Loop:
	LDR w4, D[w3, #0]
	LDR w5, D[w3, #4]
	MOVI w6, #0xC6EF3720
	MOVI w7, #32
	NOP
	NOP
.Lloop:
	LSLI w8, w4, #4
	NOP
	NOP
	NOP
	NOP
	ADDS w8, w8, k0.2
	ADD w9, w4, w6
	NOP
	NOP
	NOP
	NOP
	EOR w8, w8, w9
	LSRI w9, w4, #5
	NOP
	NOP
	NOP
	NOP
	ADDS w9, w9, k0.3
	NOP
	NOP
	NOP
	NOP
	EOR w8, w8, w9
	NOP
	NOP
	NOP
	NOP
	SUB w5, w5, w8
	NOP
	NOP
	NOP
	NOP
	LSLI w8, w5, #4
	NOP
	NOP
	NOP
	NOP
	ADDS w8, w8, k0.0
	ADD w9, w5, w6
	NOP
	NOP
	NOP
	NOP
	EOR w8, w8, w9
	LSRI w9, w5, #5
	NOP
	NOP
	NOP
	NOP
	ADDS w9, w9, k0.1
	NOP
	NOP
	NOP
	NOP
	EOR w8, w8, w9
	NOP
	NOP
	NOP
	NOP
	SUB w4, w4, w8
	SUB w6, w6, d0
	SUBI w7, w7, #1
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
	NOP
	NOP
	NOP
	NOP
	SWI