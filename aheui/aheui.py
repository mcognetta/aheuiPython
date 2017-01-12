# -*- coding: utf-8 -*-

import sys
import codecs
#import aheui.hangul as hangul
import hangul
import time

consonants = ('ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄸ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅃ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ')
initial = ('ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ')
vowel = ('ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ')
final = ('ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㄲ','ㄳ','ㄵ','ㄶ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅄ','ㅆ','ㅇ','ㅎ')
values = {'':0,'ㄱ':2,'ㄲ':4,'ㄳ':4,'ㄴ':2,'ㄵ':5,'ㄶ':5,'ㄷ':3,'ㄸ':6,'ㄹ':5,'ㄺ':7,'ㄻ':9,'ㄼ':9,'ㄽ':7,'ㄾ':9,'ㄿ':9,'ㅀ':8,'ㅁ':4,'ㅂ':4,'ㅃ':8,'ㅄ':6,'ㅅ':2,'ㅆ':4,'ㅈ':3,'ㅉ':6,'ㅊ':4,'ㅋ':3,'ㅌ':4,'ㅍ':4}

class Stack:
    def __init__(self):
        self._list = []

    def push(self,data):
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

class Queue(Stack):
    def __init__(self):
        self._list = []

    def push(self,data):
        self._list.insert(0,data)

class Interpreter:
    def __init__(self):
        self.storage = {}
        self.storage_pos = ''
        self.pos = [-1,0]
        self.dir = (1,0) #(y,x)
        self.grid = []
        self.go = True
        self.debug = False

        self.storage[''] = Stack()
        for c in final:
            if c == 'ㅇ':
                self.storage[c] = Queue()
            elif c == 'ㅎ':
                pass #protocol?
            else:
                self.storage[c] = Stack()

        if sys.argv[1] != '':
            with codecs.open(sys.argv[1],'r',encoding='utf-8') as f:
                code = f.read().split('\n')
            for line in code:
                self.grid.append(line)

    def set_dir(self, v):
        if v == 'ㅏ':
            self.dir = (0,1)
        elif v == 'ㅑ':
            self.dir = (0,2)
        elif v == 'ㅓ':
            self.dir = (0,-1)
        elif v == 'ㅕ':
            self.dir = (0,-2)
        elif v == 'ㅗ':
            self.dir = (-1,0)
        elif v == 'ㅛ':
            self.dir = (-2,0)
        elif v == 'ㅜ':
            self.dir = (1,0)
        elif v == 'ㅠ':
            self.dir = (2,0)
        elif v == 'ㅣ':
            self.dir = (self.dir[0],-self.dir[1])
        elif v == 'ㅡ':
            self.dir = (-self.dir[0],self.dir[1])
        elif v == 'ㅢ':
            self.dir = (-self.dir[0],-self.dir[1])

    def reverse_vowel(self, v):
        if v == 'ㅏ':
            self.dir = (0,-1)
        elif v == 'ㅑ':
            self.dir = (0,-2)
        elif v == 'ㅓ':
            self.dir = (0,1)
        elif v == 'ㅕ':
            self.dir = (0,2)
        elif v == 'ㅗ':
            self.dir = (1,0)
        elif v == 'ㅛ':
            self.dir = (2,0)
        elif v == 'ㅜ':
            self.dir = (-1,0)
        elif v == 'ㅠ':
            self.dir = (-2,0)
        elif v == 'ㅣ':
            self.dir = (-self.dir[0],self.dir[1])
        elif v == 'ㅡ':
            self.dir = (self.dir[0],-self.dir[1])
        elif v == 'ㅢ':
            self.dir = (self.dir[0],self.dir[1])

    def step(self):

        if self.debug:
            print(self.pos)
            print(self.dir)
            print(self.grid[self.pos[0]][self.pos[1]])
        #update y then x but what if we exceed both grid edges at the same step
        if self.dir[0] > 0 and self.pos[0]+self.dir[0] >= len(self.grid):
            print('a')
            self.pos[0] = 0

        elif self.dir[0] < 0 and self.pos[0]+self.dir[0] < 0:
            print('b')
            self.pos[0] = len(self.grid)-1
        
        elif self.dir[1] > 0 and self.pos[1]+self.dir[1] >= len(self.grid[self.pos[0]]):
            print('c')
            self.pos[1] = 0

        elif self.dir[1] < 0 and self.pos[1]+self.dir[1] < 0:
            print('d')
            self.pos[1] = len(self.grid[self.pos[0]])-1

        else:
            self.pos[0] += self.dir[0]
            self.pos[1] += self.dir[1]

        char = self.grid[self.pos[0]][self.pos[1]]

        c,v,f = hangul.split_char(char) #return error if it fails

        if c == 'ㅇ':
            self.set_dir(v)
            return

        elif c == 'ㅎ':
            self.go = False
            return

        elif c == 'ㄷ':
            if len(self.storage[self.storage_pos]) >= 2:
                x,y = self.storage[self.storage_pos].pop(), self.storage[self.storage_pos].pop()
                self.storage[self.storage_pos].push(x+y)
                self.set_dir(v)
            else:
                self.reverse_vowel(v)
            return

        elif c == 'ㄸ':
            if len(self.storage[self.storage_pos]) >= 2:
                x,y = self.storage[self.storage_pos].pop(), self.storage[self.storage_pos].pop()
                self.storage[self.storage_pos].push(x*y)
                self.set_dir(v)
            else:
                self.reverse_vowel(v)
            return

        elif c == 'ㄴ':
            if len(self.storage[self.storage_pos]) >= 2:
                x,y = self.storage[self.storage_pos].pop(), self.storage[self.storage_pos].pop()
                self.storage[self.storage_pos].push(y//x)
                self.set_dir(v)
            else:
                self.reverse_vowel(v)
            return

        elif c == 'ㅌ':
            if len(self.storage[self.storage_pos]) >= 2:
                x,y = self.storage[self.storage_pos].pop(), self.storage[self.storage_pos].pop()
                self.storage[self.storage_pos].push(y-x)
                self.set_dir(v)
            else:
                self.reverse_vowel(v)
            return

        elif c == 'ㄹ':
            if len(self.storage[self.storage_pos]) >= 2:
                x,y = self.storage[self.storage_pos].pop(), self.storage[self.storage_pos].pop()
                self.storage[self.storage_pos].push(y%x)
                self.set_dir(v)
            else:
                self.reverse_vowel(v)
            return

        elif c == 'ㅁ':
            temp = self.storage[self.storage_pos].pop()
            self.set_dir(v)
            if f == 'ㅇ':
                if temp != None:
                    print(temp)
            elif f == 'ㅎ':
                if temp != None:
                    print(chr(temp)) #here
            return

        elif c == 'ㅂ':
            self.set_dir(v)
            if f == 'ㅇ':
                self.storage[self.storage_pos].push(int(input('enter a number:')))
            elif f == 'ㅎ':
                self.storage[self.storage_pos].push(ord(input('enter a char:')))
            else:
                self.storage[self.storage_pos].push(values[f])
            return

        elif c == 'ㅃ':
            self.set_dir(v)
            if len(self.storage[self.storage_pos]) >= 1:
                self.storage[self.storage_pos].push(self.storage[self.storage_pos].peek())
            return

        elif c == 'ㅍ':
            self.set_dir(v)
            if len(self.storage[self.storage_pos]) >= 2:
                x,y = self.storage[self.storage_pos].pop(), self.storage[self.storage_pos].pop()
                self.storage[self.storage_pos].push(y)
                self.storage[self.storage_pos].push(x)
            return

        elif c == 'ㅅ':
            self.storage_pos = f
            self.set_dir(v)
            return

        elif c == 'ㅆ':
            if len(self.storage[self.storage_pos]) >= 1:
                self.storage[f].push(self.storage[self.storage_pos])
            self.set_dir(v)
            return

        elif c == 'ㅈ':
            if len(self.storage[self.storage_pos]) >= 2:
                x,y = self.storage[self.storage_pos].pop(), self.storage[self.storage_pos].pop()
                if y >= x:
                    self.storage[self.storage_pos].push(1)
                else:
                    self.storage[self.storage_pos].push(0)
            self.set_dir(v)
            return

        elif c == 'ㅊ':
            if len(self.storage[self.storage_pos]) >= 1:
                if self.storage[self.storage_pos].pop() > 0:
                    self.set_dir(v)
                else:
                    self.reverse_vowel(v)
            return

        else:
            self.go = False
            return -1

    def run(self):
        while self.go:
            if self.debug:
                time.sleep(1)
            self.step()

if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.run()