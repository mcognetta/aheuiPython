# -*- coding: utf-8 -*-

"""Interpreter for the Aheui (아희) programming language.

This module implements a Python interpreter for the Aheui programming language,
an esoteric programming language based on Befunge and written with the Korean
alphabet (힌글 or hangul).

The language has a fairly simple specification which can be found at:
    https://aheui.github.io/

Examples:
    An example execution of the interpreter is:

        > python aheui.py hello_world.aheui

    To enter debug mode you can use the flag '-d' or '--debug':

        > python aheui.py hello_world.aheui -d

    You can also interpret arbitrary aheui code via the eval method:

        > import aheui
        > aheui.eval('밤밣따빠밣밟따맣희')
"""

import sys
import codecs
import time
import argparse
import hangul

values = {'':0, 'ㄱ':2, 'ㄲ':4, 'ㄳ':4, 'ㄴ':2, 'ㄵ':5, 'ㄶ':5, 'ㄷ':3, 'ㄸ':6,
          'ㄹ':5, 'ㄺ':7, 'ㄻ':9, 'ㄼ':9, 'ㄽ':7, 'ㄾ':9, 'ㄿ':9, 'ㅀ':8, 'ㅁ':4,
          'ㅂ':4, 'ㅃ':8, 'ㅄ':6, 'ㅅ':2, 'ㅆ':4, 'ㅈ':3, 'ㅉ':6, 'ㅊ':4, 'ㅋ':3,
          'ㅌ':4, 'ㅍ':4}

class Stack(object):
    """Stack class for the interpreter.

    Contains the code that implements our stack. In the interpreter we only
    need to be able to push, pop, peek, and check the size of the stack. We
    also include a __str__ method for the debugging mode.
    """

    def __init__(self):
        self._list = []

    def push(self, data):
        self._list.append(data)

    def pop(self):
        if len(self._list) > 0:
            return self._list.pop()

    def peek(self):
        return self._list[-1]

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return str(self._list)

class Queue(Stack):
    """Queue class for the interpreter.

    Contains the code that implements our queue. This contains all the same
    functionality as the stack except for the push command so basically
    everything is overwritten.
    """

    def __init__(self):
        Stack.__init__(self)

    def push(self, data):
        self._list.insert(0, data)

    def swap(self):
        self._list[-1], self._list[-2] = self._list[-2], self._list[-1]

class Interpreter(object):
    """Main Interpreter class

    Contains the code to set up and execute the interpretation of aheui code.

    Attributes:
        storage: A map mapping 받침 consonants to their respective storage
                 data structures
        storage_pos: Unicode char corresponding to the current storage being
                     used
        pos: a 2 element list representing the current position of the cursor
             in the code
        momentum: a 2 element tuple represeting the current momentum of the cursor
        grid: a list populated by the lines of code in the source file
        go: a boolean that allows us to know when the program should terminate
            in case of an error or when hitting a ㅎ initial consonant
        debug: a boolean to toggle debugging mode on or off
    """

    def __init__(self, source='', debug=False, eval_code=''):
        self.storage = {}
        self.storage_pos = ''
        self.pos = [0, 0]
        self.momentum = (1, 0)    #(y,x)
        self.grid = []
        self.go = True
        self.debug = debug

        self.storage[''] = Stack()    # '' is not included in hangul.FINALS
        for c in hangul.FINALS:    #list of final consonants
            if c == 'ㅇ':
                self.storage[c] = Queue()
            elif c == 'ㅎ':
                self.storage[c] = Queue()    #protocol is still not well defined
            else:
                self.storage[c] = Stack()

        if eval_code != '':
            self.grid = [line for line in eval_code.split('\n')]

        elif source != '':
            with codecs.open(sys.argv[1], 'r', encoding='utf-8') as f:
                code = f.read().split('\n')
            for line in code:
                self.grid.append(line)

    def set_momentum(self, v):
        """Given the current vowel and momentum, determines the momentum for the
           cursor"""

        if v == 'ㅏ':
            self.momentum = (0, 1)
        elif v == 'ㅑ':
            self.momentum = (0, 2)
        elif v == 'ㅓ':
            self.momentum = (0, -1)
        elif v == 'ㅕ':
            self.momentum = (0, -2)
        elif v == 'ㅗ':
            self.momentum = (-1, 0)
        elif v == 'ㅛ':
            self.momentum = (-2, 0)
        elif v == 'ㅜ':
            self.momentum = (1, 0)
        elif v == 'ㅠ':
            self.momentum = (2, 0)
        elif v == 'ㅣ':
            self.momentum = (self.momentum[0], -self.momentum[1])
        elif v == 'ㅡ':
            self.momentum = (-self.momentum[0], self.momentum[1])
        elif v == 'ㅢ':
            self.momentum = (-self.momentum[0], -self.momentum[1])

    def reverse_momentum(self, v):
        """Given the current vowel, determines the momentum for the cursor in
           the case that it is reflected (due to bad stack pop, etc)"""

        if v == 'ㅏ':
            self.momentum = (0, -1)
        elif v == 'ㅑ':
            self.momentum = (0, -2)
        elif v == 'ㅓ':
            self.momentum = (0, 1)
        elif v == 'ㅕ':
            self.momentum = (0, 2)
        elif v == 'ㅗ':
            self.momentum = (1, 0)
        elif v == 'ㅛ':
            self.momentum = (2, 0)
        elif v == 'ㅜ':
            self.momentum = (-1, 0)
        elif v == 'ㅠ':
            self.momentum = (-2, 0)
        elif v == 'ㅣ':
            self.momentum = (self.momentum[0], self.momentum[1])
        elif v == 'ㅡ':
            self.momentum = (self.momentum[0], self.momentum[1])
        elif v == 'ㅢ':
            self.momentum = (self.momentum[0], self.momentum[1])

    def step(self):
        """Performs one step of the interpretation, getting the character,
           executing the associated instruction(s), updating the position,
           stack position, and momentum"""

        if self.debug:
            print("pos: ", self.pos)
            print("dir: ", self.momentum)
            print("char: ", self.grid[self.pos[0]][self.pos[1]])
            print("storage: ", self.storage[self.storage_pos])
            if self.storage_pos == '':
                print("storage_pos: \'\'")
            else:
                print("storage_pos: ", self.storage_pos)
            print()

        char = self.grid[self.pos[0]][self.pos[1]]

        if hangul.is_hangul(char):

            c, v, f = hangul.split_char(char)

            if c == 'ㅇ':
                self.set_momentum(v)

            elif c == 'ㅎ':
                self.go = False

            elif c == 'ㄷ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(x+y)
                    self.set_momentum(v)
                else:
                    self.reverse_momentum(v)

            elif c == 'ㄸ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(x*y)
                    self.set_momentum(v)
                else:
                    self.reverse_momentum(v)

            elif c == 'ㄴ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(y//x)
                    self.set_momentum(v)
                else:
                    self.reverse_momentum(v)

            elif c == 'ㅌ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(y-x)
                    self.set_momentum(v)
                else:
                    self.reverse_momentum(v)

            elif c == 'ㄹ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(y%x)
                    self.set_momentum(v)
                else:
                    self.reverse_momentum(v)

            elif c == 'ㅁ':
                if len(self.storage[self.storage_pos]) >= 1:
                    temp = self.storage[self.storage_pos].pop()
                    self.set_momentum(v)
                    if f == 'ㅇ':
                        if temp != None:
                            print(temp, end='')
                            if self.debug:
                                print()
                    elif f == 'ㅎ':
                        if temp != None:
                            print(chr(temp), end='')
                            if self.debug:
                                print()
                else:
                    self.reverse_momentum(v)

            elif c == 'ㅂ':
                self.set_momentum(v)
                if f == 'ㅇ':
                    self.storage[self.storage_pos].push(int(input()))
                elif f == 'ㅎ':
                    self.storage[self.storage_pos].push(ord(input()))
                else:
                    self.storage[self.storage_pos].push(values[f])

            elif c == 'ㅃ':
                self.set_momentum(v)
                if len(self.storage[self.storage_pos]) >= 1:
                    self.storage[self.storage_pos].push(self.storage[self.storage_pos].peek())
                else:
                    self.reverse_momentum(v)

            elif c == 'ㅍ':
                if len(self.storage[self.storage_pos]) >= 2:
                    self.set_momentum(v)
                    if self.storage_pos == 'ㅎ': #queue
                        self.storage[self.storage_pos].swap()
                    else:
                        x = self.storage[self.storage_pos].pop()
                        y = self.storage[self.storage_pos].pop()
                        self.storage[self.storage_pos].push(x)
                        self.storage[self.storage_pos].push(y)
                else:
                    self.reverse_momentum(v)

            elif c == 'ㅅ':
                self.storage_pos = f
                self.set_momentum(v)

            elif c == 'ㅆ':
                if len(self.storage[self.storage_pos]) >= 1:
                    self.set_momentum(v)
                    self.storage[f].push(self.storage[self.storage_pos].pop())
                else:
                    self.reverse_momentum(v)

            elif c == 'ㅈ':
                if len(self.storage[self.storage_pos]) >= 2:
                    self.set_momentum(v)
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    if y >= x:
                        self.storage[self.storage_pos].push(1)
                    else:
                        self.storage[self.storage_pos].push(0)
                else:
                    self.reverse_momentum(v)

            elif c == 'ㅊ':
                if len(self.storage[self.storage_pos]) >= 1:
                    if self.storage[self.storage_pos].pop() != 0:
                        self.set_momentum(v)
                    else:
                        self.reverse_momentum(v)
                else:
                    self.reverse_momentum(v)

        #if character is not 한글 it skips to here

        if self.momentum[0] != 0:
            counter = 0
            new_row = self.pos[0]
            while True:
                if self.momentum[0] > 0:
                    new_row = (new_row+1) % len(self.grid)
                else:
                    new_row = (new_row-1) % len(self.grid)

                if self.pos[1] <= len(self.grid[new_row])-1:
                    counter += 1
                    if counter == abs(self.momentum[0]):
                        break
            self.pos[0] = new_row

        else:
            self.pos[1] = (self.pos[1]+self.momentum[1]) % len(self.grid[self.pos[0]])

    def interpret(self):
        """Begins the interpretation of the aheui program"""

        while self.go:
            self.step()

def eval(code, debug=False):
    """Interprets Aheui code passed as a string parameter"""

    Interpreter(debug=debug, eval_code=code).interpret()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str,
                        help='source file for the aheui code')

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        dest='debug', help='debug mode for the interpreter')

    '''
    parser.add_argument('--log', action='store_true', default=False,
                        dest='logging', help='logging mode for the interpreter,\
                        writes to log.txt in cwd')
    '''

    args = parser.parse_args()
    Interpreter(source=args.source, debug=args.debug).interpret()
