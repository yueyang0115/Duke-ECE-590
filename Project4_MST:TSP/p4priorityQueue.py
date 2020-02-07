"""
Math 590
Project 4
PriorityQueue Class
Fall 2019
"""

"""
PriorityQueue Class
"""


class PriorityQueue:
    """
    Class attributes:
    array # The array storing the values in the queue.
          # Note: the values must have comparison operations.
    """

    """
    __init__ function to initialize the edge.

    INPUTS:
    array: the input array to be inserted into the queue.
    """

    def __init__(self, array=[]):
        self.array = array.copy()
        return

    """
    __repr__ function to print an edge.
    """

    def __repr__(self):
        return repr(self.array)

    """
    isEmpty: check if the queue is empty.
    """

    def isEmpty(self):
        if len(self.array) == 0:
            return True
        else:
            return False

    """
    insert: insert an object into the queue.
    """

    def insert(self, val):
        self.array.append(val)

    """
    deleteMin: returns the min element and removes it from the queue.
    """

    def deleteMin(self):
        # Check if empty.
        if len(self.array) == 0:
            raise Exception('Cannot delete min from an empty queue.')

        # Start by considering the first element.
        minVal = self.array[0]
        minInd = 0

        # Loop to find the min element.
        for ind in range(1, len(self.array)):
            if self.array[ind] < minVal:
                minVal = self.array[ind]
                minInd = ind

        # Remove the min and return it.
        self.array.pop(minInd)
        return minVal