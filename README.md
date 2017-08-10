# aheuiPython - an Aheui Interpreter in Python

## Introduction
Aheui is an esoteric programming language based on the Korean writing system.
[The complete specification can be found here.](https://aheui.github.io/) This
repo contains an interpreter for the language written in Python3.

## Usage
After installing aheuiPython (for example, via pip), you can interpret Aheui
files using the command `python aheui.py <inputfile>.aheui`.

There is also a debug command so that you can view the current cursor location
as well as the contents of the current data structure. This can be done using
the `-d` flag as in `python aheui.py <inputfile>.aheui -d`

Below is a sample of the output from the debug mode:

```
>>> aheui.eval('밤밣망하', debug=True)
pos:  [0, 0]
momentum:  (0, 1)
char:  밤
storage_pos: ''
storage:  [4]

pos:  [0, 1]
momentum:  (0, 1)
char:  밣
storage_pos: ''
storage:  [4, 8]

8
pos:  [0, 2]
momentum:  (0, 1)
char:  망
storage_pos: ''
storage:  [4]

pos:  [0, 3]
momentum:  (0, 1)
char:  하
storage_pos: ''
storage:  [4]
```

As you may notice, each step of the code will print the position in the grid,
the current momentum, the current character, the current storage location, and
the contents of the current storage. If the current symbol outputs something,
the output will be displayed before the debug block for that step (be aware that
the output may be whitespace and will just show up as a blank line).

Note that if the current storage is a stack, when displayed, the right most
symbol is the top. If if is a queue, the left most symbol is the back of the
queue while the right most symbol is the front (meaning we push to the left and
pop from the right).

## Examples
There are several examples from the "official" Aheui test suite included in the
examples directory.
