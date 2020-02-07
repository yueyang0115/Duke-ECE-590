"""
Math 590
Project 2
Fall 2019

p2stack.py

Partner 1:
Partner 2:
Date:
"""

"""
Stack Class
"""
class Stack:

    """
    Class attributes:
    stack    # The array for the stack.
    top      # The index of the top of the stack.
    numElems # The number of elements in the stack.
    """

    """
    __init__ function to initialize the Stack.
    Note: intially the size of the stack defaults to 100.
    Note: the stack is initally filled with None values.
    Note: since nothing is on the stack, top is -1.
    """
    def __init__(self, size=100):
        self.stack = [None for x in range(0,size)]
        self.top = -1
        self.numElems = 0
        return

    """
    __repr__ function to print the stack.
    """
    def __repr__(self):
        print(self.stack)
        print('Top: %d' % self.top)
        return ('numElems: %d' % self.numElems)

    """
    isFull function to check if the stack is full.
    """
    def isFull(self):
        if self.numElems == len(self.stack):
            return 1
        else:
            return 0

    """
    isEmpty function to check if the stack is empty.
    """
    def isEmpty(self):
        if self.numElems == 0:
            return 1
        else:
            return 0

    """
    resize function to resize the stack by doubling its size.
    """
    def resize(self):
        self.stack = self.stack + [None for x in self.stack]
        return

    """
    push function to push a value onto the stack.
    """
    def push(self, val):
        if self.isFull():
            self.resize()

        self.top = self.top + 1
        self.stack[self.top] = val
        self.numElems = self.numElems + 1
        return

    """
    pop function to pop the value off the top of the stack.
    """
    def pop(self):
        temp = self.stack[self.top]
        self.stack[self.top] = None
        self.numElems = self.numElems - 1
        self.top = self.top - 1
        return temp
        #return None