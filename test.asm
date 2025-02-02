	# Test file for microsim-assembler

	ORG 0x200
var1:
	
	ORG 0x210

start:	
	LDA_I	27

	ORG 0x220

	LDA_M	var1
	INC
	DEC
	OUT
	STA	var1

	LDA_I	4
	DEC
	BRNZ	0xFFFF

	JMP	start

