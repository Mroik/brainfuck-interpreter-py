import sys
import tty
import termios

def get_char():
    fd = sys.stdin.fileno()
    sett = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, sett)
    return ch


if len(sys.argv) > 1:
    fd = open(sys.argv[1])
else:
    fd = sys.stdin
instr = fd.read()
fd.close()

data = [0]
pos = 0
skip = False
i_instr = 0
loops = []

while(True):
    char = instr[i_instr]
    if char == '>':
        if pos == len(data)-1:
            data.append(0)
        pos += 1
    elif char == '<':
        if pos == 0:
            data.insert(0, 0)
        else:
            pos -= 1
    elif char == '+':
        data[pos] += 1
        if data[pos] == 256:
            data[pos] = 0
    elif char == '-':
        data[pos] -= 1
        if data[pos] == -1:
            data[pos] = 255
    elif char == '.':
        print(chr(data[pos]), end="")
    elif char == ',':
        data[pos] = ord(get_char())
        if data[pos] > 255:
            raise ValueError("Brainfuck only stores byte sized data. Limit yourself to ASCII")
    elif char == '[':
        if data[pos] != 0:
            loops.append(i_instr)
        else:
            inside = 0
            while(True):
                i_instr += 1
                char = instr[i_instr]
                if char == '[':
                    inside += 1
                elif char == ']':
                    if inside != 0:
                        inside -= 1
                    else:
                        break
    elif char == ']':
        if data[pos] != 0:
            i_instr = loops.pop() - 1
    i_instr += 1
    if len(instr)-1 == i_instr:
        break
