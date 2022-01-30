# This is a brainfuck interpreter
To use it simply call it with the name of the file to read from as the 1st
argument. Otherwise you can pipe into the interpreter the program.
```sh
python interpreter.py program.txt
```
```sh
echo ",.>,.>,." | python interpreter.py
```
