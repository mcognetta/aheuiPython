# -*- coding: utf-8 -*-

import sys, codecs, time, argparse
#import aheui.hangul as hangul
import hangul

consonants = ('ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ',
              'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ',
              'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

initial = ('ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ',
           'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

vowel = ('ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ',
         'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ')

final = ('ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㄲ',
         'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ', 'ㅆ', 'ㅇ',
         'ㅎ')

values = {'':0, 'ㄱ':2, 'ㄲ':4, 'ㄳ':4, 'ㄴ':2, 'ㄵ':5, 'ㄶ':5, 'ㄷ':3, 'ㄸ':6,
          'ㄹ':5, 'ㄺ':7, 'ㄻ':9, 'ㄼ':9, 'ㄽ':7, 'ㄾ':9, 'ㄿ':9, 'ㅀ':8, 'ㅁ':4,
          'ㅂ':4, 'ㅃ':8, 'ㅄ':6, 'ㅅ':2, 'ㅆ':4, 'ㅈ':3, 'ㅉ':6, 'ㅊ':4, 'ㅋ':3,
          'ㅌ':4, 'ㅍ':4}

class Stack:
    def __init__(self):
        self._list = []

    def push(self, data):
        self._list.append(data)

    def pop(self):
        if len(self._list) > 0:
            return self._list.pop()
    
    def peek(self):
        return self._list[-1]

    def size(self):
        return len(self._list)

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return str(self._list)

class Queue(Stack):
    def __init__(self):
        self._list = []

    def push(self, data):
        self._list.insert(0, data)

class Interpreter:
    """Main Interpreter class

    Contains the code to set up and execute the interpretation of aheui code.

    Attributes:
        storage: A map mapping 받침 consonants to their respective storage
                 data structures
        storage_pos: Unicode char corresponding to the current storage being
                     used
        pos: a 2 element list representing the current position of the cursor
             in the code
        dir: a 2 element tuple represeting the current momentum of the cursor
        grid: a list populated by the lines of code in the source file
        go: a boolean that allows us to know when the program should terminate
            in case of an error or when hitting a ㅎ initial consonant
        debug: a boolean to toggle debugging mode on or off
    """

    def __init__(self, source='', debug=False):
        self.storage = {}
        self.storage_pos = ''
        self.pos = [0, 0]
        self.dir = (1, 0) #(y,x)
        self.grid = []
        self.go = True
        self.debug = debug

        self.storage[''] = Stack()
        for c in final:
            if c == 'ㅇ':
                self.storage[c] = Queue()
            elif c == 'ㅎ':
                pass #protocol?
            else:
                self.storage[c] = Stack()

        if source != '':
            with codecs.open(sys.argv[1], 'r', encoding='utf-8') as f:
                code = f.read().split('\n')
            for line in code:
                self.grid.append(line)

    def set_dir(self, v):
        """Given the current vowel and momentum, determines the momentum for the
           cursor"""

        if v == 'ㅏ':
            self.dir = (0, 1)
        elif v == 'ㅑ':
            self.dir = (0, 2)
        elif v == 'ㅓ':
            self.dir = (0, -1)
        elif v == 'ㅕ':
            self.dir = (0, -2)
        elif v == 'ㅗ':
            self.dir = (-1, 0)
        elif v == 'ㅛ':
            self.dir = (-2, 0)
        elif v == 'ㅜ':
            self.dir = (1, 0)
        elif v == 'ㅠ':
            self.dir = (2, 0)
        elif v == 'ㅣ':
            self.dir = (self.dir[0], -self.dir[1])
        elif v == 'ㅡ':
            self.dir = (-self.dir[0], self.dir[1])
        elif v == 'ㅢ':
            self.dir = (-self.dir[0], -self.dir[1])

    def reverse_vowel(self, v):
        """Given the current vowel, determines the momentum for the cursor in
           the case that it is reflected (due to bad stack pop, etc)"""

        if v == 'ㅏ':
            self.dir = (0, -1)
        elif v == 'ㅑ':
            self.dir = (0, -2)
        elif v == 'ㅓ':
            self.dir = (0, 1)
        elif v == 'ㅕ':
            self.dir = (0, 2)
        elif v == 'ㅗ':
            self.dir = (1, 0)
        elif v == 'ㅛ':
            self.dir = (2, 0)
        elif v == 'ㅜ':
            self.dir = (-1, 0)
        elif v == 'ㅠ':
            self.dir = (-2, 0)
        elif v == 'ㅣ':
            self.dir = (-self.dir[0], self.dir[1])
        elif v == 'ㅡ':
            self.dir = (self.dir[0], -self.dir[1])
        elif v == 'ㅢ':
            self.dir = (self.dir[0], self.dir[1])

    def step(self):
        """Performs one step of the interpretation, getting the character,
           executing the associated instruction(s), updating the position,
           stack position, and momentum"""

        if self.debug:
            print("pos: ", self.pos)
            print("dir: ", self.dir)
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
                self.set_dir(v)

            elif c == 'ㅎ':
                self.go = False

            elif c == 'ㄷ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(x+y)
                    self.set_dir(v)
                else:
                    self.reverse_vowel(v)

            elif c == 'ㄸ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(x*y)
                    self.set_dir(v)
                else:
                    self.reverse_vowel(v)

            elif c == 'ㄴ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(y//x)
                    self.set_dir(v)
                else:
                    self.reverse_vowel(v)

            elif c == 'ㅌ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(y-x)
                    self.set_dir(v)
                else:
                    self.reverse_vowel(v)

            elif c == 'ㄹ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(y%x)
                    self.set_dir(v)
                else:
                    self.reverse_vowel(v)

            elif c == 'ㅁ':
                temp = self.storage[self.storage_pos].pop()
                self.set_dir(v)
                if f == 'ㅇ':
                    if temp != None:
                        print(temp, end='')
                        if self.debug:
                            print()
                elif f == 'ㅎ':
                    if temp != None:
                        print(chr(temp), end='') #here
                        if self.debug:
                            print()

            elif c == 'ㅂ':
                self.set_dir(v)
                if f == 'ㅇ':
                    self.storage[self.storage_pos].push(int(input()))
                elif f == 'ㅎ':
                    self.storage[self.storage_pos].push(ord(input()))
                else:
                    self.storage[self.storage_pos].push(values[f])

            elif c == 'ㅃ':
                self.set_dir(v)
                if len(self.storage[self.storage_pos]) >= 1:
                    self.storage[self.storage_pos].push(self.storage[self.storage_pos].peek())

            elif c == 'ㅍ':
                self.set_dir(v)
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    self.storage[self.storage_pos].push(x)
                    self.storage[self.storage_pos].push(y)

            elif c == 'ㅅ':
                self.storage_pos = f
                self.set_dir(v)

            elif c == 'ㅆ':
                if len(self.storage[self.storage_pos]) >= 1:
                    self.storage[f].push(self.storage[self.storage_pos].pop())
                self.set_dir(v)

            elif c == 'ㅈ':
                if len(self.storage[self.storage_pos]) >= 2:
                    x = self.storage[self.storage_pos].pop()
                    y = self.storage[self.storage_pos].pop()
                    if y >= x:
                        self.storage[self.storage_pos].push(1)
                    else:
                        self.storage[self.storage_pos].push(0)
                self.set_dir(v)

            elif c == 'ㅊ':
                if len(self.storage[self.storage_pos]) >= 1:
                    if self.storage[self.storage_pos].pop() > 0:
                        self.set_dir(v)
                    else:
                        self.reverse_vowel(v)

        if self.dir[0] > 0 and self.pos[0]+self.dir[0] >= len(self.grid):
            self.pos[0] = 0

        elif self.dir[0] < 0 and self.pos[0]+self.dir[0] < 0:
            self.pos[0] = len(self.grid)-1
        
        elif self.dir[1] > 0 and self.pos[1]+self.dir[1] >= len(self.grid[self.pos[0]]):
            self.pos[1] = 0

        elif self.dir[1] < 0 and self.pos[1]+self.dir[1] < 0:
            self.pos[1] = len(self.grid[self.pos[0]])-1

        else:
            self.pos[0] += self.dir[0]
            self.pos[1] += self.dir[1]


    def run(self):
        """Begins the interpretation of the aheui program"""

        while self.go:
            if self.debug:
                time.sleep(1)
            self.step()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str,
                        help='source file for the aheui code')

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        dest='debug', help='debug mode for the interpreter')
    args = parser.parse_args()
    #parser.add_argument('--log', action='store_true', default=False, dest='logging', help='logging mode for the interpreter, writes to log.txt in cwd')
    Interpreter(source=args.source, debug=args.debug).run()
    #Interpreter(debug=True).run()
