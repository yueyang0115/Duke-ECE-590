"""
Math 590
Project 3
Fall 2019

Partner 1: Yue Yang (yy258)
Partner 2:
Date: 11/13/2019
"""

# Import math and p3tests.
import math
from p3tests import *

################################################################################

"""
detectArbitrage
"""


def detectArbitrage(currencies, tol=1e-15):
    # Set initial dist, visited and prev
    for v in currencies.adjList:
        v.prev = None
        v.dist = math.inf

    # set the dist of start vertex to 0
    currencies.adjList[0].dist = 0

    # do V-1 iteration
    for iter in range(0, len(currencies.adjList) - 1):
        # Look at each vertex
        for u in currencies.adjList:
            # Check each neighbor of u
            # Update predictions and previous vertex
            for neigh in u.neigh:
                # Only update if the new value is better
                if neigh.dist > u.dist + currencies.adjMat[u.rank][neigh.rank] + tol:
                    neigh.dist = u.dist + currencies.adjMat[u.rank][neigh.rank]
                    neigh.prev = u

    # do one more time iteration to detect negative circle
    circle_flag = 0
    global curr
    for u in currencies.adjList:
        for neigh in u.neigh:
            # if a vertex changes its dist, negative circle exists
            if neigh.dist > u.dist + currencies.adjMat[u.rank][neigh.rank] + tol:
                circle_flag = 1
                neigh.prev = u
                # vertex 'curr' changes dist but may not be in the circle
                curr = neigh
                break
        if circle_flag == 1:
            break

    # follow the changed vertex's path backwards, save vertex.rank in an array
    # if a vertex is saved twice, it is visited twice and is in negative circle
    array = [None for x in currencies.adjList]
    while array[curr.rank % len(array)] is None:
        array[curr.rank % len(array)] = 1
        curr = curr.prev
    firstnode = curr

    circle = []
    # if negative circle exists
    if circle_flag == 1:
        # track vertices, get a circle in reverse
        circle.append(firstnode.rank)
        curr = firstnode.prev
        while not curr.isEqual(firstnode):
            circle.append(curr.rank)
            curr = curr.prev
        circle.append(curr.rank)

        # reverse to get the original circle
        circle = [i for i in reversed(circle) if i is not None]

    return circle

################################################################################

"""
rates2mat
"""

def rates2mat(rates):
    return [[-math.log(R) for R in row] for row in rates]

"""
Main function.
"""
if __name__ == "__main__":
    testRates()
