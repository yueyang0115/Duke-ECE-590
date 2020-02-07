"""
Math 590
Project 4
Fall 2019

Partner 1: Yue Yang (yy258)
Partner 2: Qingyang Xu (qx37)
Date: 12/05/2019
"""

# Import math, itertools, and time.
import math
import itertools
import time

# Import the Priority Queue.
from p4priorityQueue import *

################################################################################

"""
Prim's Algorithm

INPUTS
adjList: the adjacency list for the map (a list of Vertex objects)
adjMat: the adjacency matrix for the map

OUTPUTS
None

"""


def prim(adjList, adjMat):
    # Initialize all costs to ∞ and prev to null
    for v in adjList:
        v.visited = False
        v.prev = None
        v.cost = math.inf

    # Pick a start vertex and set cost to 0
    start = adjList[0]
    start.cost = 0

    # Make the priority queue using cost for sorting
    pq = PriorityQueue()
    for v in adjList:
        pq.insert(v)

    while not pq.isEmpty():
        # Get the next unvisited vertex and visit it
        curr = pq.deleteMin()
        curr.visited = True

        # For each edge out of v
        for neigh in curr.neigh:
            # If the edge leads out, update
            if not neigh.visited:
                if neigh.cost > adjMat[curr.rank][neigh.rank]:
                    neigh.cost = adjMat[curr.rank][neigh.rank]
                    neigh.prev = curr

    return


################################################################################

"""
Kruskal's Algorithm
Note: the edgeList is ALREADY SORTED!
Note: Use the isEqual method of the Vertex class when comparing vertices.

INPUTS
adjList: the adjacency list for the map (a list of Vertex objects)
edgeList: the list of Edge objects for the map

OUTPUTS
X: the list of Edge objects in MST

"""


def kruskal(adjList, edgeList):
    # Initialize all singleton sets for each vertex
    for v in adjList:
        makeset(v)

    # Initialize the empty MST
    X = []

    # Loop through the sorted edges in increasing order.
    for e in edgeList:
        # If the min edge crosses a cut, add it to our MST
        u, v = e.vertices
        if not find(u).isEqual(find(v)):
            X.append(e)
            union(u, v)

    return X


################################################################################

"""
Disjoint Set Functions:
    makeset
    find
    union

These functions will operate directly on the input vertex objects.
"""

"""
makeset: this function will create a singleton set with root v.
"""


def makeset(v):
    v.pi = v
    v.height = 0
    return


"""
find: this function will return the root of the set that contains v.
Note: we will use path compression here.

"""


def find(v):
    if v != v.pi:
        v.pi = find(v.pi)
    return v.pi


"""
union: this function will union the sets of vertices v and u.
"""


def union(u, v):
    # First, find the root of the tree for u # and the tree for v
    ru = find(u)
    rv = find(v)

    # If the sets are already the same, return
    if ru == rv:
        return

    # Make shorter set point to taller set
    if ru.height > rv.height:
        rv.pi = ru
    elif ru.height < rv.height:
        ru.pi = rv
    else:
        # Same height, break tie.
        ru.pi = rv

        # Tree got taller, increment rv.height
        rv.height += 1

    return


################################################################################

"""
TSP

INPUTS
adjList: the adjacency list for the map (a list of Vertex objects)
start: the start vertex

OUTPUTS
tour: the list of vertices for TSP

"""


def tsp(adjList, start):
    # Initialize tour to an empty list
    tour = []

    # Initialize all vertices as not visited
    for v in adjList:
        v.visited = False

    # A list works as a stack to track the next unvisited vertex
    st = []
    # Push the start vertex onto our stack
    st.append(start)

    # When stack is not empty
    while len(st) != 0:
        # Get the current vertex
        curr = st.pop()

        if curr.visited == False:  # Only visit if we have not visited before
            # Mark as visited
            curr.visited = True

            # Append the vertex to tour
            tour.append(curr.rank)

            for neigh in curr.mstN:
                # Push all neighbors onto the stack
                st.append(neigh)

    # Append the start vertex as the end of tour
    tour.append(start.rank)

    return tour


################################################################################

# Import the tests (since we have now defined prim and kruskal).
from p4tests import *

"""
Main function.
"""
if __name__ == "__main__":
    verb = False  # Set to true for more printed info.
    print('Testing Prim\n')
    print(testMaps(prim, verb))
    print('\nTesting Kruskal\n')
    print(testMaps(kruskal, verb))
