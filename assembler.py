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
                    #print("----> ORG")
                    address = process_number_string(tokens[1])
                    # print("-----------> ", hex(address))
                if (tokens[0] == "LDA_I"):
                    address = address + 2
                if (tokens[0] == "INC"):
                    address = address + 1
                if (tokens[0] == "DEC"):
                    addres = address + 1
                if (tokens[0] == "OUT"):
                    address = address + 1
                if (tokens[0] == "JMP"):
                    address = address + 3
                if (tokens[0][-1] == ":"):
                    # print("---------------------------> LABEL")
                    labels[tokens[0][:-1]] = hex(address)

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
                # LDA_I Op Code
                if (tokens[0] == "LDA_I"):
                    print("----> LAD_I")
                    output.append(prepend_and_inc_address(1))
                    output.append(prepend_and_inc_address(process_number_string(tokens[1])))
                # INC Op Code
                if (tokens[0] == "INC"):
                    print("----> INC")
                    output.append(prepend_and_inc_address(6))
                # DEC Op Code
                if (tokens[0] == "DEC"):
                    print("----> DEC")
                    output.append(prepend_and_inc_address(7))
                # OUT Op Code
                if (tokens[0] == "OUT"):
                    print("----> OUT")
                    output.append(prepend_and_inc_address(9))
                # JMP Op Code
                if (tokens[0] == "JMP"):
                    print("----> JMP")
                    output.append(prepend_and_inc_address(10))
                    addr = process_number_string(labels[tokens[1]])
                    print("------> Jump Address:", addr)
                    output.append(prepend_and_inc_address(addr // 256))
                    output.append(prepend_and_inc_address(addr % 256))

if __name__ == "__main__":
    print('Microsim Assembler 2 - v0.1')
    parse_asm_file()
    print("LABELS")
    print(labels)
    print("OUTPUT")
    print(output)
