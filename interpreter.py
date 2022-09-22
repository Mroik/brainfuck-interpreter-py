import argparse
import tty
import termios
from sys import stdin


def get_char():
    fd = stdin.fileno()
    oldy = termios.tcgetattr(fd)
    try:
        tty.setraw(fd, termios.TCSADRAIN)
        ch = stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, oldy)
    return ch


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

    def load_program(self, program: str) -> None:
        for instruction in program:
            match instruction:
                case ('>' | '<' | '+' | '-' | '.' | ',' | '[' | ']'):
                    self.program.append(str(instruction))
        if len(self.program) == 0:
            raise ValueError("No program was present in the string")
        self.ready = True

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
        print(chr(self.memory[self.data_pointer]), end="", flush=True)

    def _scan_data(self) -> None:
        """
        Instruction ','
        """
        char_read = ord(get_char())
        if char_read > 255 or char_read < 0:
            raise ValueError("Can read only ASCII characters")
        self.memory[self.data_pointer] = char_read

    def _left_conditional(self) -> None:
        """
        Instruction '['
        """
        if self.memory[self.data_pointer] == 0:
            while self.program[self.program_pointer] != ']':
                self.program_pointer += 1
                if self.program_pointer >= len(self.program):
                    raise RuntimeError("The program is not correctly written")

    def _right_conditional(self) -> None:
        """
        Instruction ']'
        """
        if self.memory[self.data_pointer] != 0:
            counter = 0
            self.program_pointer -= 1

            while True:
                if self.program[self.program_pointer] == '[':
                    if counter == 0:
                        break
                    counter -= 1
                elif self.program[self.program_pointer] == ']':
                    counter += 1
                self.program_pointer -= 1
                if self.program_pointer <= 0:
                    raise RuntimeError("The program is not correctly written")

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


def main(args):
    inter = Interpreter()
    if args.program:
        with open(args.program, "r") as fd:
            prog = fd.read()
    else:
        print("You need to pass a file to read from")
        return
    inter.load_program(prog)
    inter.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program", nargs="?", help="The file containing the program")
    main(parser.parse_args())
