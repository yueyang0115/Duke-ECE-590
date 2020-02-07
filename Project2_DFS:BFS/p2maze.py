"""
Math 590
Project 2
Fall 2019

p2Maze.py
"""

# Import math, other p2 files, and plotting.
import math
from project2 import bdfs
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np

"""
Vertex Class
"""


class Vertex:
    """
    Class attributes:

    rank    # The rank of this node.
    neigh   # The list of neighbors.
    dist    # The distance from start.
    visited # Flag whether vertex has been visited.
    prev    # The previous vertex in the path.
    """

    """
    __init__ function to initialize the vertex.
    """

    def __init__(self, rank):
        self.rank = rank  # Set the rank of this vertex.
        self.neigh = []  # Set the input neighbors.
        self.dist = math.inf  # Infinite dist initially.
        self.visited = False  # Nothing visited at initialization.
        self.prev = None  # No previous node on path yet.
        return

    """
    __repr__ function to print a vertex.
    Note: only prints the rank!
    """

    def __repr__(self):
        return '%d' % self.rank

    """
    isEqual function compares this Vertex to an input Vertex object.
    Note: only needs to compare the rank!
    """

    def isEqual(self, vertex):
        return self.rank == vertex.rank


################################################################################

"""
Maze Class
"""


class Maze:
    """
    Class attributes:

    maze    # The 2D list representing the maze.
    adjList # The adjacency list of Vertex objects.
    adjMat  # The adjacency matrix, 2D list.
    start   # The start Vertex object.
    exit    # The exit Vertex object.
    path    # The path from start to exit, list of ranks.
    verb    # A flag to control printing. False prints less.
    """

    """
    __init__ function to initialize the maze.
    """

    def __init__(self, mazeNum=0, verbosity=False):

        # Select the maze to use.
        self.maze = getMaze(mazeNum)

        # Create an adjacency list of empty vertices.
        self.adjList = [Vertex(r) for r in \
                        range(0, len(self.maze) * len(self.maze[0]))]

        # Initialize the adjacency matrix to have no edges yet.
        self.adjMat = [[0 for x in self.adjList] for y in self.adjList]

        # Now loop through the maze and update adjacencies.
        # In this loop, maze[r][c] will correspond to vertex rank:
        #     r*len(maze[0])+c
        # Note: we skip the first and last row/col.
        for r in range(1, len(self.maze) - 1):
            for c in range(1, len(self.maze[r]) - 1):
                # Note that maze[r][c] will now be a 0 or a 1.
                # If it is 0, then open space and needs adjacency.
                # If it is 1, then wall and no adjacency.
                if self.maze[r][c] == 0:
                    # If up is open, it is a neighbor.
                    if self.maze[r - 1][c] == 0:
                        # Append the neighbor to the neigh list.
                        self.adjList[r * len(self.maze[0]) + c].neigh.append( \
                            self.adjList[(r - 1) * len(self.maze[0]) + c])

                        # Update the correct entry in the adjMat.
                        self.adjMat[r * len(self.maze[0]) + c] \
                            [(r - 1) * len(self.maze[0]) + c] = 1

                    # If down is open, it is a neighbor.
                    if self.maze[r + 1][c] == 0:
                        # Append the neighbor to the neigh list.
                        self.adjList[r * len(self.maze[0]) + c].neigh.append( \
                            self.adjList[(r + 1) * len(self.maze[0]) + c])

                        # Update the correct entry in the adjMat.
                        self.adjMat[r * len(self.maze[0]) + c] \
                            [(r + 1) * len(self.maze[0]) + c] = 1

                    # If left is open, it is a neighbor.
                    if self.maze[r][c - 1] == 0:
                        # Append the neighbor to the neigh list.
                        self.adjList[r * len(self.maze[0]) + c].neigh.append( \
                            self.adjList[r * len(self.maze[0]) + c - 1])

                        # Update the correct entry in the adjMat.
                        self.adjMat[r * len(self.maze[0]) + c] \
                            [r * len(self.maze[0]) + c - 1] = 1

                    # If right is open, it is a neighbor.
                    if self.maze[r][c + 1] == 0:
                        # Append the neighbor to the neigh list.
                        self.adjList[r * len(self.maze[0]) + c].neigh.append( \
                            self.adjList[r * len(self.maze[0]) + c + 1])

                        # Update the correct entry in the adjMat.
                        self.adjMat[r * len(self.maze[0]) + c] \
                            [r * len(self.maze[0]) + c + 1] = 1

        # Find the start in the top row and exit in the bottom row.
        # Update their info in the adjList and adjMat.
        # Note: start's only neighbor is down and exit's is up.
        for ind in range(0, len(self.maze[0])):
            if self.maze[0][ind] == 0:
                self.start = self.adjList[ind]
                self.start.neigh = [self.adjList[ind + len(self.maze[0])]]
                self.adjMat[ind][ind + len(self.maze[0])] = 1
                break
        for ind in range(0, len(self.maze[len(self.maze) - 1])):
            if self.maze[len(self.maze) - 1][ind] == 0:
                self.exit = \
                    self.adjList[ind + (len(self.maze) - 1) * len(self.maze[0])]
                self.exit.neigh = [self.adjList[ind + \
                                                (len(self.maze) - 2) * len(self.maze[0])]]
                self.adjMat[self.exit.rank] \
                    [self.exit.rank - len(self.maze[0])] = 1
                break

        # Set the path to be empty.
        self.path = []

        # Set verbosity.
        self.verb = verbosity
        return

    """
    __repr function to print the maze.
    """

    def __repr__(self):
        # Loop through the rows and cols of the maze and fill in 'X' for a wall
        # and ' ' for an open space. Put line breaks between rows.
        mp = ''
        for r in range(0, len(self.maze)):
            for c in range(0, len(self.maze)):
                if self.maze[r][c] == 0:
                    mp += ' '
                else:
                    mp += 'X'
            mp += '\n'

        # Mark the start with 's' and the end with 'e'.
        # Note the shift due to the line break symbols.
        # Note that each line break '\n' counts as 1 char...
        mp = mp[0:self.start.rank] + 's' + \
             mp[self.start.rank + 1:self.exit.rank + len(self.maze) - 1] + \
             'e' + mp[self.exit.rank + len(self.maze):]

        # If the path is not empty, fill it in.
        # Check to make sure it is a correct and valid path.
        if len(self.path) > 0:

            # Not an invalid path yet...
            invalid = False

            # Needs to start at start and end at end.
            if self.path[0] != self.start.rank:
                print('Path does not begin at start!')
                invalid = True
                mp = mp[0:self.start.rank + self.start.rank // len(self.maze[0])] + \
                     '!' + \
                     mp[self.start.rank + self.start.rank // len(self.maze[0]) + 1:]
            if self.path[len(self.path) - 1] != self.exit.rank:
                print('Path does not exit the maze!')
                invalid = True
                mp = mp[0:self.exit.rank + self.exit.rank // len(self.maze[0])] + \
                     '!' + \
                     mp[self.exit.rank + self.exit.rank // len(self.maze[0]) + 1:]

            # Loop through the path and fill it in.
            # Check for invalid ghosts and repeats.
            for vertex in self.path:
                # Skip the start and end.
                if (vertex != self.start.rank) and (vertex != self.exit.rank):
                    # Check if it is a wall or opening. Fill if open.
                    # Also check if already visited.
                    if mp[vertex + vertex // len(self.maze[0])] == 'X':
                        print('No ghosts! Do not walk through walls!')
                        invalid = True
                        mp = mp[0:vertex + vertex // len(self.maze[0])] + 'G' + \
                             mp[vertex + vertex // len(self.maze[0]) + 1:]
                    elif mp[vertex + vertex // len(self.maze[0])] == 'o':
                        print('You have already been to this vertex...')
                        invalid = True
                        mp = mp[0:vertex + vertex // len(self.maze[0])] + 'R' + \
                             mp[vertex + vertex // len(self.maze[0]) + 1:]
                    elif mp[vertex + vertex // len(self.maze[0])] == 'G':
                        print('Repeated ghosts!')
                    elif mp[vertex + vertex // len(self.maze[0])] == 'R':
                        print('Repeating again!')

                    else:
                        mp = mp[0:vertex + vertex // len(self.maze[0])] + 'o' + \
                             mp[vertex + vertex // len(self.maze[0]) + 1:]

            # Loop through the path to make sure that each neighbor is actually
            # a neighbor...
            for vInd in range(0, len(self.path) - 1):
                if (self.adjMat[self.path[vInd]][self.path[vInd + 1]] != 1) \
                        and (self.path[vInd] != self.path[vInd + 1]):
                    print('Not a neighbor! You cannot teleport!')
                    invalid = True

            # If we had an invalid path, print that fact.
            if invalid:
                print('')
                print('Path is invalid!')
                print('')
            else:
                print('')
                print('MAZE SOLVED!!!')
                print('')

        # Return the string for printing.
        if self.verb:
            return mp
        else:
            return ''

    """
    printList function for cleanly printing the adjaceny list.
    Note: skips vertices with no neighbors.
    """

    def printList(self):
        for vertex in self.adjList:
            if len(vertex.neigh) > 0:
                print('Rank: %d' % vertex.rank)
                print('Neighbors:')
                print(vertex.neigh)
                print('')
        return

    """
    printMat function for cleanly printing the adjaceny matrix.
    Note: for the larger mazes, this will still likely be hard to read.
    """

    def printMat(self):
        for row in self.adjMat:
            print(row)
        return

    """
    plot_maze_solution function for cleanly plotting your final path.
    Note: set plotting to False to supress figure generation.
    """

    def plot_maze_solution(self, plotting=True):
        if self.verb == False:
            return
        mp = self.__repr__()
        np_mz = []
        row_mz = []
        possible_value = ['X', ' ', 'o', 's', 'e', 'G', 'R']
        for i in mp:
            if i == '\n':
                np_mz += [row_mz]
                row_mz = []
                continue
            if i == '!':
                i = 'e'
            row_mz += [possible_value.index(i) / 6.]
        viridis = cm.get_cmap('viridis', 6)
        newcolors = viridis(np.linspace(0, 1, 6))
        newcolors[0, :] = np.array([0, 0, 1, 1])
        newcolors[1, :] = np.array([1, 1, 1, 1])
        newcolors[3, :] = np.array([0.7, 0.7, 0.7, 1])
        newcolors[4, :] = np.array([0, 1, 0, 1])
        newcolors[5, :] = np.array([1, 0, 0, 1])
        newcmp = ListedColormap(newcolors)
        plt.figure(figsize=(4, 4))
        fig = plt.imshow(np_mz, cmap=newcmp)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        if plotting:
            plt.show()

    """
    solve function calls implemented bdfs using the input alg.
    Note: set verbosity to False to supress printing out the resulting maze/path.
    Note: set plotting to False to supress figure generation.
    """

    def solve(self, alg, verbosity=True, plotting=True):
        self.path = bdfs(self, alg)
        if len(self.path) == 0:
            print('Maze not solved!\n')
        self.verb = verbosity
        print(self)
        self.plot_maze_solution(plotting)
        return


################################################################################

"""
getMaze function will provide the 2D array representing the maze to the Maze
class's __init__ function.

INPUTS
mazeNum: which maze to select

OUTPUTS
maze: a 2D list representing the maze
"""


def getMaze(mazeNum=0):
    # Select the maze to use.
    if mazeNum == 0:
        maze = [[1, 1, 0, 1, 1], \
                [1, 0, 0, 0, 1], \
                [1, 0, 0, 0, 1], \
                [1, 0, 0, 0, 1], \
                [1, 1, 0, 1, 1], ]
    elif mazeNum == 1:
        maze = [[1, 1, 0, 1, 1], \
                [1, 0, 0, 0, 1], \
                [1, 0, 1, 1, 1], \
                [1, 0, 0, 0, 1], \
                [1, 1, 0, 1, 1], ]
    elif mazeNum == 2:
        maze = [[1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1], \
                [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1], \
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], \
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1], \
                [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1], \
                [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1], \
                [1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1], \
                [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], \
                [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1], \
                [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1], \
                [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1], \
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1], \
                [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1], \
                [1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], \
                [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], \
                [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1], \
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1], \
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1], \
                [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    elif mazeNum == 3:
        maze = [[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], \
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], \
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    else:
        raise Exception('Input mazeNum not valid!')

    return maze