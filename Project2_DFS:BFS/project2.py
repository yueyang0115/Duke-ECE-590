"""
Math 590
Project 2
Fall 2019

project2.py

Partner 1:
Partner 2:
Date:
"""

# Import math and other p2 files.
import math
from p2tests import *

################################################################################
"""
DFS function
INPUTS
A maze object
maze: A Maze object representing the maze.
USAGE
Call dfs(maze), you will get a path
OUTPUS
path: A path from start vertex to target vertex, which is a list,
      which shortest path from maze.start to maze.exit.
"""
def dfs(maze):
    for v in maze.adjList:
        v.visited = False                   # No vertex visited yet
        v.prev = None

    st = Stack()                            # Push the start vertex onto our stack
    st.push(maze.start)

    while not st.isEmpty():
        curr = st.pop()                     # Get the current room
        if curr.isEqual(maze.exit):         # Found exit
            break

        if curr.visited == False:           # Only visit if we have not visited before
            curr.visited = True             # Mark as visited
            for neigh in curr.neigh:        # Push all neighbors onto the stack
                st.push(neigh)
                if neigh.visited == False:
                    neigh.prev = curr       # Then record where we came from

    path = [None for x in maze.adjList]     # Write down the path in reversed way
    curr = maze.exit
    index = 0
    while curr != None:
        path[index] = curr.rank
        index = index + 1
        curr = curr.prev

    # reverse path
    maze.path = [path[i] for i in range((len(path) - 1), -1, -1) if path[i] != None]
    print(maze.path)
    return maze.path    # return path to the exit


"""
BFS function
INPUTS
A maze object
maze: A Maze object representing the maze.
USAGE
Call bfs(maze), you will get a path
OUTPUS
path: A path from start vertex to target vertex, which is a list,
      which shortest path from maze.start to maze.exit.
"""
def bfs(maze):
    for v in maze.adjList:
        v.prev = None
        v.dist = math.inf                   # Set all vertices to an infinite distance
        v.visited = False

    queue = Queue()
    queue.push(maze.start)                  # Push the start vertex into the queue
    maze.start.dist = 0                     # set start.dist = 0.

    while not queue.isEmpty():              # Get the current vertex
        curr = queue.pop()
        if curr.isEqual(maze.exit):         # Found exit
            break

        for neigh in curr.neigh:            # Look at all of its neighbors
            if neigh.dist == math.inf:      # If the neighbor’s dist not updated
                queue.push(neigh)           # Push the neighbor into the queue
                neigh.dist = curr.dist+1    # Update its distance
                neigh.prev = curr           # track path
                neigh.visited = True

    path = [None for x in maze.adjList]  # Write down the path in reversed way
    curr = maze.exit
    index = 0
    while curr != None:
        path[index] = curr.rank
        index = index + 1
        curr = curr.prev

    maze.path = [i for i in reversed(path) if i != None]
    return maze.path  # return path to the exit

################################################################################


"""
BFS/DFS function

INPUTS
maze: A Maze object representing the maze.
alg:  A string that is either 'BFS' or 'DFS'.

OUTPUTS
path: The shortest path from maze.start to maze.exit.
"""
def bdfs(maze, alg):
    # If the alg is not BFS or DFS, raise exception.
    if (alg != 'BFS') and (alg != 'DFS'):
        raise Exception('Incorrect alg! Need BFS or DFS!')

    ##### Your implementation goes here. #####
    if alg == 'BFS':
        return bfs(maze)
    else:
        return dfs(maze)

"""
Main function.
"""
if __name__ == "__main__":
    testMazes(False)