import sys


class Interpreter:
    def __init__(self):
        self.code = ""
        self.go_text = "package main\n\nimport \"fmt\"\n\nfunc main() {\n" \
                       "\tmemorySize := uint16(30000)\n" \
                       "\tmemory := make([]byte, memorySize)\n" \
                       "\tptr := int16(0)\n" \
                       "\tvar response string\n\n"
        self.indent = 1
        self.code_ptr = 0
        self.storage = 0

    def get_code(self, code: str):
        self.code = code

    # Appends code to the Go text and resets storage when desired
    def push(self, string: str, reset_storage=False):
        self.go_text += "\t" * self.indent + string + "\n"
        if reset_storage:
            self.storage = 0

    def current(self) -> str:
        return self.code[self.code_ptr]

    # Compare to current() above - the extra code here prevents over-indexing self.code
    def next(self) -> str:
        if self.code_ptr + 1 < len(self.code):
            return self.code[self.code_ptr + 1]
        return "ERR"

    """
    Evaluates current character AND the next character.
    This, along with self.storage, compacts code repetition; i.e.
        memory[ptr] += 1
        memory[ptr] += 1
        memory[ptr] += 1
    becomes
        memory[ptr] += 3
    """
    def current_is(self, inp: str) -> bool:
        if self.current() == inp:
            if self.next() == inp:
                self.storage += 1
                return False
            return True
        return False

    def interpret(self):
        while self.code_ptr < len(self.code):
            if self.current_is("+"):
                self.push("memory[ptr] += " + str(self.storage + 1), True)
            elif self.current_is("-"):
                self.push("memory[ptr] -= " + str(self.storage + 1), True)
            elif self.current_is(">"):
                self.push("ptr = (ptr + " + str(self.storage + 1) + ") % int16(memorySize)", True)
            elif self.current_is("<"):
                self.push("ptr -= " + str(self.storage + 1), True)
                self.push("if ptr < 0 {ptr = int16(memorySize - 1)}")
            elif self.current() == ".":
                self.push("fmt.Print(string(memory[ptr]))")
            elif self.current() == ",":
                self.push("_, err := fmt.Scanln(&response)")
                self.push("if err != nil {panic(err)}")
                self.push("memory[ptr] = response[0]")
            elif self.current() == "[":
                self.push("for memory[ptr] != 0 {")
                self.indent += 1
            elif self.current() == "]":
                self.indent -= 1
                if self.indent < 1:
                    sys.exit("Syntax error: cannot have a \"]\" before a \"[\"")
                self.push("}")

            self.code_ptr += 1

        if self.indent != 1:
            sys.exit("Syntax error: missing \"]\"")

        # Pushes end-of-file code
        self.push("response = \"\"")
        self.push("fmt.Print(response)")
        self.indent = 0
        self.push("}")


if __name__ == '__main__':
    # Gets CLI file path
    file_path = sys.argv[1]

    # Strips path down to .bf file name and replaces .bf with .go
    go_name = file_path.split("/")[-1].replace(".bf", "") + ".go"
    interpreter = Interpreter()

    # Populates interpreter with .bf source code
    with open(file_path, "r") as file:
        interpreter.get_code(file.read())

    interpreter.interpret()

    # Creates Go file
    with open(go_name, "w") as go_file:
        go_file.write(interpreter.go_text)
