import argparse

from interpreter import Interpreter


def main(args):
    inter = Interpreter()
    if args.program:
        with open(args.program, "r") as fd:
            prog = fd.read()
    else:
        prog = input()
    if not inter.load_program(prog):
        print("Error, check your program")
        return
    inter.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program", nargs="?", help="The file containing the program")
    main(parser.parse_args())
