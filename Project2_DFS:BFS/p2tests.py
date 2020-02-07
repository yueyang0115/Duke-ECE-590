"""
Math 590
Project 2
Fall 2019

p2tests.py
"""

# Import math and other p2 files.
import math
from p2stack import *
from p2queue import *
from p2maze import *

"""
testMazes function will test all of the mazes.
"""
def testMazes(verbosity=False):
    m = Maze(0,verbosity)
    print('Testing Maze 0, DFS')
    m.solve('DFS',verbosity,False)
    print('Testing Maze 0, BFS')
    m.solve('BFS',verbosity,False)
    m = Maze(1,verbosity)
    print('Testing Maze 1, DFS')
    m.solve('DFS',verbosity,False)
    print('Testing Maze 1, BFS')
    m.solve('BFS',verbosity,False)
    m = Maze(2,verbosity)
    print('Testing Maze 2, DFS')
    m.solve('DFS',verbosity,False)
    print('Testing Maze 2, BFS')
    m.solve('BFS',verbosity,False)
    m = Maze(3,verbosity)
    print('Testing Maze 3, DFS')
    m.solve('DFS',verbosity,False)
    print('Testing Maze 3, BFS')
    m.solve('BFS',verbosity,False)
    plt.show()
    return

################################################################################