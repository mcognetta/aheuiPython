import hangul

class Stack:
    def __init__(self):
        self._list = []

    def push(self,data):
        self._list.append(data)

    def pop(self,data):
        return self._list.pop()
    
    def peek(self):
        return self._list[-1]

    def size(self):
        return len(self._list)

class Queue:
    def __init__(self):
        self._list = []

    def push(self,data):
        self._list.insert(0,data)

    def pop(self,data):
        return self._list.pop()

    def peek(self,data):
        return self._list[-1]

    def size(self):
        return len(self._list)
