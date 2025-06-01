# Microsim Assembler 2

address = 0x100
labels = {}
output = []

def process_number_string(s):
    if (s[:2]) == "0x":
        n = int(s, 16)
    else:
        n = int(s)
    return(n)

def prepend_and_inc_address(d):
    global address
    ret = [address, d]
    address = address + 1
    return(ret)

def write_obj_file():
    global output
    with open("/home/barry/software/projects/microsim-assembler-2/test.obj", "w") as file:
        for addr in output:
            out = str(addr[0]) + "    " + str(addr[1])
            file.write(out)
            file.write("\n")

def parse_asm_file():
    global address
    with open("/home/barry/software/projects/microsim-assembler-2/test.asm") as file:
        # Lables Pass
        for line in file:
            # print("Lables Pass")
            # print(line.strip().split())
            # Skip blank lines
            if line.strip() == "":
                pass
            else:
                tokens = line.strip().split()
                # ORG Directive
                if (tokens[0] == "ORG"):
                    print("----> ORG")
                    address = process_number_string(tokens[1])
                    print("-----------> ", hex(address))
                if (tokens[0] == "VAR"):
                    print("----> VAR")
                    size = process_number_string(tokens[1])
                    address = address + size
                if (tokens[0] == "LDA_I"):
                    address = address + 2
                if (tokens[0] == "LDA_M"):
                    address = address + 3
                if (tokens[0] == "STA"):
                    address = address + 3
                if (tokens[0] == "ADD_I"):
                    address = address + 2
                if (tokens[0] == "ADD_M"):
                    address = address + 3
                if (tokens[0] == "INC"):
                    address = address + 1
                if (tokens[0] == "DEC"):
                    address = address + 1
                if (tokens[0] == "BRNZ"):
                    address = address + 3
                if (tokens[0] == "OUT"):
                    address = address + 1
                if (tokens[0] == "JMP"):
                    address = address + 3
                if (tokens[0] == "JSR"):
                    address = address + 3
                if (tokens[0] == "RET"):
                    address = address + 1
                if (tokens[0] == "LDI_I"):
                    address = address + 3
                if (tokens[0] == "LDI_M"):
                    address = address + 3
                if (tokens[0] == "INCI"):
                    address = address + 1
                if (tokens[0] == "DECI"):
                    address = address + 1
                if (tokens[0] == "LDAI"):
                    address = address + 1
                if (tokens[0] == "LDAIO"):
                    address = address + 2
                if (tokens[0] == "STAI"):
                    address = address + 1
                if (tokens[0] == "STAIO"):
                    address = address + 2
                if (tokens[0][-1] == ":"):
                    print("---------------------------> LABEL")
                    labels[tokens[0][:-1]] = hex(address)
                    print("---------------------------> ", hex(address))

        print(labels)    
            
        # Assembler Pass
        file.seek(0)
        for line in file:
            print(line.strip().split())
            # Skip blank lines
            if line.strip() == "":
                print("----> BLANK")
            else:
                tokens = line.strip().split()
                # ORG Directive
                if (tokens[0] == "ORG"):
                    print("----> ORG")
                    address = process_number_string(tokens[1])
                    # print("-----------> ", hex(address))
                # constant string directive
                if (tokens[0] == ".S"):
                    print("Tokens size = ", len(tokens))
                    print("String = ", tokens[1])
                    for tok in tokens:
                        if (tok != ".S"):
                            for c in tok:
                                print(c, " -> ", ord(c))
                                output.append(prepend_and_inc_address(ord(c)))
                            output.append(prepend_and_inc_address(ord(' ')))
                    output.append(prepend_and_inc_address(0))
                # LDA_I Op Code
                if (tokens[0] == "LDA_I"):
                    print("----> LDA_I")
                    output.append(prepend_and_inc_address(1))
                    output.append(prepend_and_inc_address(process_number_string(tokens[1])))
                # LDA_M Op Code
                if (tokens[0] == "LDA_M"):
                    print("----> LDA_M")
                    output.append(prepend_and_inc_address(2))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Load Address:", hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # STA Op Code
                if (tokens[0] == "STA"):
                    print("----> STA")
                    output.append(prepend_and_inc_address(3))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Store Address:", hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # ADD_I Op Code
                if (tokens[0] == "ADD_I"):
                    print("----> ADD_I")
                    output.append(prepend_and_inc_address(4))
                    output.append(prepend_and_inc_address(process_number_string(tokens[1])))
                # ADD_M Op Code
                if (tokens[0] == "ADD_M"):
                    print("----> ADD_M")
                    output.append(prepend_and_inc_address(5))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Add Address:", hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # INC Op Code
                if (tokens[0] == "INC"):
                    print("----> INC")
                    output.append(prepend_and_inc_address(6))
                # DEC Op Code
                if (tokens[0] == "DEC"):
                    print("----> DEC")
                    output.append(prepend_and_inc_address(7))
                # BRNZ Op Code
                if (tokens[0] == "BRNZ"):
                    print("----> BRNZ")
                    output.append(prepend_and_inc_address(8))
                    addr = process_number_string(labels[tokens[1]])
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # OUT Op Code
                if (tokens[0] == "OUT"):
                    print("----> OUT")
                    output.append(prepend_and_inc_address(9))
                # JMP Op Code
                if (tokens[0] == "JMP"):
                    print("----> JMP")
                    output.append(prepend_and_inc_address(10))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Jump Address:", hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # JSR Op Code
                if (tokens[0] == "JSR"):
                    print("----> JSR")
                    output.append(prepend_and_inc_address(11))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Jump Subroutine Address:", hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # RET Op Code
                if (tokens[0] == "RET"):
                    print("----> RET")
                    output.append(prepend_and_inc_address(12))
                # LDI_I Op Code
                if (tokens[0] == "LDI_I"):
                    print("----> LDI_I")
                    output.append(prepend_and_inc_address(13))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Index Address:", hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # LDI_M Op Code
                if (tokens[0] == "LDI_M"):
                    print("----> LDI_M")
                    output.append(prepend_and_inc_address(14))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Index Address:", hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # INCI
                if (tokens[0] == "INCI"):
                    print("----> INCI")
                    output.append(prepend_and_inc_address(15))
                # DECI
                if (tokens[0] == "DECI"):
                    print("----> DECI")
                    output.append(prepend_and_inc_address(16))
                # LDAI
                if (tokens[0] == "LDAI"):
                    print("----> LDAI")
                    output.append(prepend_and_inc_address(17))
                # LDAIO
                if (tokens[0] == "LDAIO"):
                    print("----> LDAIO")
                    output.append(prepend_and_inc_address(18))
                    data = process_number_string(labels[tokens[1]])
                    print("------> Data:", hex(addr))
                    output.append(prepend_and_inc_address(data))
                # STAI
                if (tokens[0] == "STAI"):
                    print("----> STAI")
                    output.append(prepend_and_inc_address(19))
                # STAIO
                if (tokens[0] == "STAIO"):
                    print("----> STAIO")
                    output.append(prepend_and_inc_address(18))
                    data = process_number_string(labels[tokens[1]])
                    print("------> Data:", hex(addr))
                    output.append(prepend_and_inc_address(data))

                # HALT Op Code
                if (tokens[0] == "HALT"):
                    print("----> HALT")
                    output.append(prepend_and_inc_address(255))

if __name__ == "__main__":
    print('Microsim Assembler 2 - v0.1')
    parse_asm_file()
    print("LABELS")
    print(labels)
    print("OUTPUT")
    print(output)
    write_obj_file()
