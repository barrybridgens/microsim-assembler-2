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

def parse_asm_file():
    with open("/home/barry/software/projects/microsim-assembler-2/test.asm") as file:
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
                    output.append(1)
                    output.append(process_number_string(tokens[1]))
                # INC Op Code
                if (tokens[0] == "INC"):
                    print("----> INC")
                    output.append(6)
                # DEC Op Code
                if (tokens[0] == "DEC"):
                    print("----> DEC")
                    output.append(7)
                # OUT Op Code
                if (tokens[0] == "OUT"):
                    print("----> OUT")
                    output.append(9)

if __name__ == "__main__":
    print('Microsim Assembler 2 - v0.1')
    parse_asm_file()
    print("OUTPUT")
    print(output)
