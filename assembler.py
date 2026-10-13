# Microsim Assembler 2

import sys

input_fn = "/home/barry/software/projects/microsim-assembler-2/test.asm"
obj_fn = "/home/barry/software/projects/microsim-assembler-2/test.obj"
lst_fn = "/home/barry/software/projects/microsim-assembler-2/test.lst"

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
    with open(obj_fn, "w") as obj_file:
        for addr in output:
            out = str(addr[0]) + "    " + str(addr[1])
            obj_file.write(out)
            obj_file.write("\n")

def write_to_file(file, line):
    file.write(line)
    file.write("\n")
    

def parse_asm_file():
    global address
    with open(input_fn) as asm_file:
        # Lables Pass
        for line in asm_file:
            # print("Lables Pass")
            # print(line.strip().split())
            # Skip blank lines
            if line.strip() == "":
                pass
            else:
                tokens = line.strip().split()
                # ORG Directive
                if (tokens[0] == "ORG"):
                    write_to_file(lst_file, "----> ORG")
                    address = process_number_string(tokens[1])
                    write_to_file(lst_file, "-----------> " + hex(address))
                if (tokens[0] == "VAR"):
                    write_to_file(lst_file, "----> VAR")
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
                    write_to_file(lst_file, "---------------------------> LABEL")
                    labels[tokens[0][:-1]] = hex(address)
                    write_to_file(lst_file, "---------------------------> " + hex(address))

        print(labels)    
            
        # Assembler Pass
        asm_file.seek(0)
        for line in asm_file:
            # write_to_file(lst_file, line.strip().split())
            # Skip blank lines
            if line.strip() == "":
                write_to_file(lst_file, "----> BLANK")
            else:
                tokens = line.strip().split()
                # ORG Directive
                if (tokens[0] == "ORG"):
                    write_to_file(lst_file, "----> ORG")
                    address = process_number_string(tokens[1])
                    # write_to_file(lst_file, "-----------> " + hex(address))
                # constant string directive
                if (tokens[0] == ".S"):
                    write_to_file(lst_file, "Tokens size = " + str(len(tokens)))
                    write_to_file(lst_file, "String = " + tokens[1])
                    for tok in tokens:
                        if (tok != ".S"):
                            for c in tok:
                                write_to_file(lst_file, c + " -> " + str(ord(c)))
                                output.append(prepend_and_inc_address(ord(c)))
                            output.append(prepend_and_inc_address(ord(' ')))
                    output.append(prepend_and_inc_address(0))
                # LDA_I Op Code
                if (tokens[0] == "LDA_I"):
                    write_to_file(lst_file, "----> LDA_I")
                    output.append(prepend_and_inc_address(1))
                    output.append(prepend_and_inc_address(process_number_string(tokens[1])))
                # LDA_M Op Code
                if (tokens[0] == "LDA_M"):
                    write_to_file(lst_file, "----> LDA_M")
                    output.append(prepend_and_inc_address(2))
                    addr = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Load Address:" + hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # STA Op Code
                if (tokens[0] == "STA"):
                    write_to_file(lst_file, "----> STA")
                    output.append(prepend_and_inc_address(3))
                    addr = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Store Address:" + hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # ADD_I Op Code
                if (tokens[0] == "ADD_I"):
                    write_to_file(lst_file, "----> ADD_I")
                    output.append(prepend_and_inc_address(4))
                    output.append(prepend_and_inc_address(process_number_string(tokens[1])))
                # ADD_M Op Code
                if (tokens[0] == "ADD_M"):
                    write_to_file(lst_file, "----> ADD_M")
                    output.append(prepend_and_inc_address(5))
                    addr = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Add Address:" + hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # INC Op Code
                if (tokens[0] == "INC"):
                    write_to_file(lst_file, "----> INC")
                    output.append(prepend_and_inc_address(6))
                # DEC Op Code
                if (tokens[0] == "DEC"):
                    write_to_file(lst_file, "----> DEC")
                    output.append(prepend_and_inc_address(7))
                # BRNZ Op Code
                if (tokens[0] == "BRNZ"):
                    write_to_file(lst_file, "----> BRNZ")
                    output.append(prepend_and_inc_address(8))
                    addr = process_number_string(labels[tokens[1]])
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # OUT Op Code
                if (tokens[0] == "OUT"):
                    write_to_file(lst_file, "----> OUT")
                    output.append(prepend_and_inc_address(9))
                # JMP Op Code
                if (tokens[0] == "JMP"):
                    write_to_file(lst_file, "----> JMP")
                    output.append(prepend_and_inc_address(10))
                    addr = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Jump Address:" + hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # JSR Op Code
                if (tokens[0] == "JSR"):
                    write_to_file(lst_file, "----> JSR")
                    output.append(prepend_and_inc_address(11))
                    addr = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Jump Subroutine Address:" + hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # RET Op Code
                if (tokens[0] == "RET"):
                    write_to_file(lst_file, "----> RET")
                    output.append(prepend_and_inc_address(12))
                # LDI_I Op Code
                if (tokens[0] == "LDI_I"):
                    write_to_file(lst_file, "----> LDI_I")
                    output.append(prepend_and_inc_address(13))
                    addr = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Index Address:" + hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # LDI_M Op Code
                if (tokens[0] == "LDI_M"):
                    write_to_file(lst_file, "----> LDI_M")
                    output.append(prepend_and_inc_address(14))
                    addr = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Index Address:" + hex(addr))
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))
                # INCI
                if (tokens[0] == "INCI"):
                    write_to_file(lst_file, "----> INCI")
                    output.append(prepend_and_inc_address(15))
                # DECI
                if (tokens[0] == "DECI"):
                    write_to_file(lst_file, "----> DECI")
                    output.append(prepend_and_inc_address(16))
                # LDAI
                if (tokens[0] == "LDAI"):
                    write_to_file(lst_file, "----> LDAI")
                    output.append(prepend_and_inc_address(17))
                # LDAIO
                if (tokens[0] == "LDAIO"):
                    write_to_file(lst_file, "----> LDAIO")
                    output.append(prepend_and_inc_address(18))
                    data = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Data:" + hex(addr))
                    output.append(prepend_and_inc_address(data))
                # STAI
                if (tokens[0] == "STAI"):
                    write_to_file(lst_file, "----> STAI")
                    output.append(prepend_and_inc_address(19))
                # STAIO
                if (tokens[0] == "STAIO"):
                    write_to_file(lst_file, "----> STAIO")
                    output.append(prepend_and_inc_address(18))
                    data = process_number_string(labels[tokens[1]])
                    write_to_file(lst_file, "------> Data:" + hex(addr))
                    output.append(prepend_and_inc_address(data))

                # HALT Op Code
                if (tokens[0] == "HALT"):
                    write_to_file(lst_file, "----> HALT")
                    output.append(prepend_and_inc_address(255))

if __name__ == "__main__":
    print('Microsim Assembler 2 - v0.1')
    # Get input filename from command line (if present)
    if len(sys.argv) > 1:
        input_fn = sys.argv[1]
        obj_fn = input_fn[:input_fn.index('.')] + '.obj'
        lst_fn = input_fn[:input_fn.index('.')] + '.lst'
    with open(lst_fn, "w") as lst_file:
        write_to_file(lst_file, "Input File Name: " + input_fn)
        write_to_file(lst_file, "\n")
        parse_asm_file()
        print("LABELS")
        print(labels)
        print("OUTPUT")
        print(output)
        write_obj_file()
