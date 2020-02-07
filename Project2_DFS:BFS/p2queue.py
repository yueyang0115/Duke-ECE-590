"""
Math 590
Project 2
Fall 2019

p2queue.py

Partner 1:
Partner 2:
Date:
"""

"""
Queue Class
"""
class Queue:

    """
    Class attributes:
    queue    # The array for the queue.
    front    # The index of the front of the queue.
    rear     # The index ONE PAST the rear of the queue.
    numElems # The number of elements in the queue.
    """

    """
    __init__ function to initialize the Queue.
    Note: intially the size of the queue defaults to 100.
    Note: the queue is initally filled with None values.
    """
    def __init__(self, size=3):
        self.queue = [None for x in range(0,size)]
        self.front = 0
        self.rear = 0
        self.numElems = 0
        return

    """
    __repr__ function to print the stack.
    """
    def __repr__(self):
        print(self.queue)
        print('Front: %d' % self.front)
        print('Rear: %d' % self.rear)
        return ('numElems: %d' % self.numElems)

    """
    isFull function to check if the queue is full.
    """
    def isFull(self):
        if self.numElems == len(self.queue):
            return 1
        else:
            return 0

    """
    isEmpty function to check if the queue is empty.
    """
    def isEmpty(self):
        if self.numElems == 0:
            return 1
        else:
            return 0

    """
    resize function to resize the queue by doubling its size.
    Note: we also reset the front to index 0.
    """
    def resize(self):
        if (self.rear<=self.front):
            self.queue = self.queue[self.front:] + self.queue[:self.rear]
        self.front = 0
        self.rear = self.numElems
        self.queue = self.queue + [None for x in self.queue]
        return

    """
    push function to push a value into the rear of the queue.
    """
    def push(self, val):
        if self.isFull():
            self.resize()
        self.queue[self.rear] = val

        if(self.rear==len(self.queue)-1):
            self.rear=0
        else:
            self.rear = self.rear + 1

        self.numElems = self.numElems + 1
        return

    """
    pop function to pop the value from the front of the queue.
    """
    def pop(self):
        temp = self.queue[self.front]
        self.queue[self.front] = None

        if (self.front == len(self.queue)-1):
            self.front = 0
        else:
            self.front = self.front+1

        self.numElems = self.numElems - 1
        return temp
        #return None