	# Test file for microsim-assembler

	ORG 0x080
var1:
	VAR 1
	
	ORG 0x0100
start:	
	LDA_I	27

	LDA_M	var1
	INC
	ADD_I	0x05
	ADD_M	var1
	STA	var1
	DEC
	OUT
	STA	var1

	LDA_I	4

	LDI_I	hello

loop:	
	LDAI
	OUT
	INCI
	BRNZ	loop

	HALT
hello:
	.S Hello World
