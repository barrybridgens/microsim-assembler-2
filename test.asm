	# Test file for microsim-assembler

	ORG 0x200
var1:
	
	ORG 0x210

start:	
	LDA_I	27

	ORG 0x220

	LDA_M	var1
	INC
	ADD_I	0x05
	ADD_M	var1
	STA	var1
	DEC
	OUT
	STA	var1

	LDA_I	4
loop:	
	DEC
	BRNZ	loop

	HALT

