class Interpreter:
    def __init__(self):
        self.memory = list()
        self.memory.append(0)
        self.program = list()
        self.ready = False
        self.data_pointer = 0
        self.program_pointer = 0
        self._instructions = {
            ">": self._increment_pointer,
            "<": self._decrement_pointer,
            "+": self._increment_value,
            "-": self._decrement_value,
            ".": self._print_data,
            ",": self._scan_data,
            "[": self._left_conditional,
            "]": self._right_conditional,
        }

    def load_program(self, program: str) -> bool:
        for instruction in program:
            match instruction:
                case ('>' | '<' | '+' | '-' | '.' | '|' | '[' | ']'):
                    self.program.append(str(instruction))
        self.ready = True
        return True

    def _increment_pointer(self) -> None:
        """
        Instruction '>'
        """
        self.data_pointer += 1
        if self.data_pointer == 30000:
            raise IndexError("Brainfuck traditionally only has 30.000 bytes of memory")
        while len(self.memory) <= self.data_pointer:
            self.memory.append(0)

    def _decrement_pointer(self) -> None:
        """
        Instruction '<'
        """
        self.data_pointer -= 1
        if self.data_pointer < 0:
            raise IndexError("Can't point to a cell left to the 0-th")

    def _increment_value(self) -> None:
        """
        Instruction '+'
        """
        self.memory[self.data_pointer] += 1
        if self.memory[self.data_pointer] > 255:
            self.memory[self.data_pointer] = 0

    def _decrement_value(self) -> None:
        """
        Instruction '-'
        """
        self.memory[self.data_pointer] -= 1
        if self.memory[self.data_pointer] < 0:
            self.memory[self.data_pointer] = 255

    def _print_data(self) -> None:
        """
        Instruction '.'
        """
        print(chr(self.memory[self.data_pointer]), end="")

    def _scan_data(self) -> None:
        """
        Instruction ','
        """
        char_read = ord(input()[0])
        if char_read > 255 or char_read < 0:
            raise ValueError("Can read only ASCII characters")
        self.memory[self.data_pointer] = char_read

    def _left_conditional(self) -> None:
        """
        Instruction '['
        """
        if self.memory[self.data_pointer] == 0:
            while True:
                self.program_pointer += 1
                if self.program_pointer >= len(self.program):
                    raise RuntimeError("The program is not correctly written")
                if self.program[self.program_pointer] == ']':
                    break

    def _right_conditional(self) -> None:
        """
        Instruction ']'
        """
        if self.memory[self.data_pointer] != 0:
            while True:
                self.program_pointer -= 1
                if self.program_pointer <= 0:
                    raise RuntimeError("The program is not correctly written")
                if self.program[self.program_pointer] == '[':
                    break

    def _fetch_execute(self) -> bool:
        self._instructions[self.program[self.program_pointer]]()
        self.program_pointer += 1
        return self.program_pointer == len(self.program)

    def start(self) -> bool:
        if not self.ready:
            return False
        self.ready = False
        while not self._fetch_execute():
            pass
        return True

    def debug(self):
        print("Memory:")
        for x in self.memory:
            print(f"\t{x}")
        print("Program:")
        for x in self.program:
            print(f"\t{x}")
        print(f"Program pointer: {self.program_pointer}")
