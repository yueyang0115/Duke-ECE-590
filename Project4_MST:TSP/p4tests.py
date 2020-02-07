"""
Math 590
Project 4
Testing Code
Fall 2019
"""

# Import the Map Class.
from p4map import *

"""
testMaps

This function will test your code on the various maps using the input alg.

INPUTS
alg: prim or kruskal
verb: verbosity flag, if True will print info on solutions

OUTPUTS
s: a string indicating number of tests passed.
"""


def testMaps(alg, verb=False):
    Mpass = 0
    Tpass = 0
    MSTfailed = False
    TSPfailed = False
    t = 9
    tol = 1e-6

    if alg == prim:
        sAlg = 'Prim'
    else:
        sAlg = 'Kruskal'

    # Test maps.
    MSTws = [12, 6, 5999.977279, 6909.105275, 11810.893206, 7724.194671, \
             8813.919553, 39763.305768, 39763.305768]
    for ind in range(0, t):
        if verb:
            print('##########################')
        MSTw = MSTws[ind]
        m = Map(ind, alg)
        m.getMST()
        if len(m.mst) < len(m.cities) - 1:
            print('Test %d: Not enough edges in MST.' % ind)
            MSTfailed = True
        if len(m.mst) > len(m.cities) - 1:
            print('Test %d: Too many edges in MST.' % ind)
            MSTfailed = True
        w = 0
        for e in m.mst:
            w += e.weight
        if w < MSTw - tol:
            print('Test %d: MST weight too low.' % ind)
            MSTfailed = True
        if w > MSTw + tol:
            print('Test %d: MST weight too high.' % ind)
            MSTfailed = True
        if not MSTfailed:
            m.getTSP()
            w = 0
            if len(m.tour) > 0:
                for r in range(0, len(m.tour) - 1):
                    w += m.adjMat[m.tour[r]][m.tour[r + 1]]
            else:
                w = math.inf
            if len(m.tour) != len(m.cities) + 1:
                print('Test %d: TSP should be length %d.' % (ind, len(m.cities) + 1))
                TSPfailed = True
            if w == math.inf:
                print('Test %d: No TSP reported.' % ind)
                TSPfailed = True
            else:
                if w > 2 * MSTw + 2 * tol:
                    print('Test %d: TSP too large.' % ind)
                    TSPfailed = True
                if w <= MSTw - tol:
                    print('Test %d: TSP too small.' % ind)
                    TSPfailed = True
            if m.tour[0] != m.tour[-1]:
                print('Test %d: TSP start != end.' % ind)
                TSPfailed = True
            for c in range(1, len(m.tour)):
                city = m.tour[c]
                if city in m.tour[c + 1:]:
                    print('Test %d: Repeated City in TSP.' % ind)
                    TSPfailed = True
            if ind == 7:
                ans = 40030.173592
                if (w < ans - tol) or (w > ans + tol):
                    print('Test %d: Wrong TSP!' % ind)
                    TSPfailed = True
            if ind == 8:
                ans = 79526.611536
                if (w < ans - tol) or (w > ans + tol):
                    print('Test %d: Wrong TSP!' % ind)
                    TSPfailed = True
        else:
            TSPfailed = True
        if not MSTfailed:
            Mpass += 1
        if not TSPfailed:
            Tpass += 1

        if verb:
            print()
            print('Testing map %d with %s' % (ind, sAlg))
            print(m)
            print()

    if verb:
        print('##########################')
        print()
    s = 'Passed %d/%d MST Tests and %d/%d TSP Tests for %s.' \
        % (Mpass, t, Tpass, t, sAlg)
    return s