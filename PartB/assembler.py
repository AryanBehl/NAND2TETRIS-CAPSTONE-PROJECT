import sys


def clean_lines(filename):
    """Read an assembly file and remove comments and blank lines."""
    instructions = []

    with open(filename, "r") as file:
        for line in file:

            line = line.split("//")[0].strip()

            if line:
                instructions.append(line)

    return instructions



def first_pass(instructions):
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2,
        "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }

    for i in range(16):
        symbols["R" + str(i)] = i

    defined_labels = set()
    instruction_address = 0

    for instruction in instructions:
        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]

            if label in defined_labels:
                print("Warning: Duplicate label:", label)
            else:
                defined_labels.add(label)
                symbols[label] = instruction_address
        else:
            instruction_address += 1

    return symbols



def a_instruction(symbol, symbols, next_variable):
    if symbol.isdigit():
        address = int(symbol)
    elif symbol in symbols:
        address = symbols[symbol]
    else:
        address = next_variable
        symbols[symbol] = address
        next_variable += 1

    binary = format(address, "016b")
    return binary, next_variable


COMP_TABLE = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

DEST_TABLE = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

JUMP_TABLE = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}



def c_instruction(instruction):
    dest = ""
    jump = ""

    if "=" in instruction:
        dest, instruction = instruction.split("=", 1)

    if ";" in instruction:
        comp, jump = instruction.split(";", 1)
    else:
        comp = instruction

    # Normalize destination order
    dest = "".join(ch for ch in "AMD" if ch in dest)

    if comp not in COMP_TABLE:
        raise ValueError("Unknown computation: " + comp)

    if dest not in DEST_TABLE:
        raise ValueError("Unknown destination: " + dest)

    if jump not in JUMP_TABLE:
        raise ValueError("Unknown jump: " + jump)

    return "111" + COMP_TABLE[comp] + DEST_TABLE[dest] + JUMP_TABLE[jump]



def assemble(filename):
    instructions = clean_lines(filename)

    # Pass 1: Build symbol table
    symbols = first_pass(instructions)

    # Pass 2: Generate machine code
    next_variable = 16
    machine_code = []

    for instruction in instructions:

        # Ignore labels
        if instruction.startswith("(") and instruction.endswith(")"):
            continue

        # A-instruction
        elif instruction.startswith("@"):
            symbol = instruction[1:]
            binary, next_variable = a_instruction(
                symbol, symbols, next_variable
            )
            machine_code.append(binary)

        # C-instruction
        else:
            binary = c_instruction(instruction)
            machine_code.append(binary)

    # Create output filename
    output_file = filename.rsplit(".", 1)[0] + ".hack"

    with open(output_file, "w") as file:
        for code in machine_code:
            file.write(code + "\n")

    print("Assembly successful!")
    print("Output file:", output_file)
    print("Total instructions:", len(machine_code))



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
        sys.exit(1)

    assemble(sys.argv[1])
