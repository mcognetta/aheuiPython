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
pos:  [23, 16]
dir:  (1, 0)
char:  뿌
storage:  [99]
storage_pos: ''

pos:  [24, 16]
dir:  (1, 0)
char:  숨
storage:  [99, 99]
storage_pos: ''

pos:  [25, 16]
dir:  (1, 0)
char:  빠
storage:  [97]
storage_pos:  ㅁ

pos:  [25, 17]
dir:  (0, 1)
char:  본
storage:  [97, 97]
storage_pos:  ㅁ
```

## Examples
There are several examples from the "official" Aheui test suite included in the
examples directory.
