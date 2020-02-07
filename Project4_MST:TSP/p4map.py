"""
Math 590
Project 4
Graph Classes
Fall 2019
"""

# Import math, prim, kruskal, and tsp.
import math
from project4 import prim, kruskal, tsp

"""
Vertex Class
"""


class Vertex:
    """
    Class attributes:

    rank    # The rank of this node.
    neigh   # The list of neighbors IN THE ORIGINAL GRAPH.
    mstN    # The list of neighbors IN THE MST.
    visited # A flag for whether the vertex has been visited.
    cost    # The cost of the edge out of the tree.
    prev    # The previous vertex in the path.
    pi      # The parent vertex in the disjoint set.
    height  # The height of this vertex in the disjoint set.
    city    # The name of the associated city.
    """

    """
    __init__ function to initialize the vertex.
    """

    def __init__(self, rank):
        self.rank = rank  # Set the rank of this vertex.
        self.neigh = []  # Set the input neighbors.
        self.mstN = []  # Set the mst neighbors.
        self.visited = False  # Not yet visited.
        self.cost = math.inf  # Infinite cost initially.
        self.prev = None  # No previous node on path yet.
        self.pi = None  # No parent vertex yet.
        self.height = 0  # 0 height initially.
        self.city = ''  # No city initially.
        return

    """
    __repr__ function to print a vertex.
    Note: only prints the city!
    """

    def __repr__(self):
        return '%s' % self.city

    """
    isEqual function compares this Vertex to an input Vertex object.
    Note: only needs to compare the rank!
    """

    def isEqual(self, vertex):
        return self.rank == vertex.rank

    """
    Overloaded comparison operators for priority queue.
    Sorted by cost.
    """

    def __lt__(self, other):
        return self.cost < other.cost


################################################################################

"""
Edge Class
"""


class Edge:
    """
    Class attributes:

    vertices # The list of vertices for this edge.
    weight   # The weight of this edge.
    """

    """
    __init__ function to initialize the edge.

    INPUTS:
    vertex1 and vertex2: the vertices for the edge
    weight: the weight of the edge
    """

    def __init__(self, vertex1=None, vertex2=None, weight=math.inf):
        self.vertices = [vertex1] + [vertex2]
        self.weight = weight
        return

    """
    __repr__ function to print an edge.
    """

    def __repr__(self):
        return '(%s,%s): %f' % (self.vertices[0].city, \
                                self.vertices[1].city, \
                                self.weight)

    """
    Overloaded comparison operators for sorting by weight...
    """

    def __lt__(self, other):
        return self.weight < other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __ne__(self, other):
        return self.weight != other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __ge__(self, other):
        return self.weight >= other.weight


################################################################################

"""
Map Class
"""


class Map:
    """
    Class attributes:
    adjMat   # The adjacency matrix storing edge weights.
    cities   # The list of city names.
    adjList  # The adjacency list of vertices.
    edgeList # The list of edges (edge objects).
    start    # The starting vertex of the tour.
    MSTalg   # Either prim or kruskal.
    mst      # The edges in the MST.
    tour     # The TSP tour (list of vertex ranks).
    optTour  # A string displaying the optimal tour.
    """

    """
    __init__ function to initialize the map.

    INPUTS:
    mapNum: The number of the map to use.
    MSTalg: The function for which alg to use: prim or kruskal.
    """

    def __init__(self, mapNum=0, MSTalg=prim):
        # Get the adjMat, cities, and optTour using mapNum.
        self.adjMat, self.cities, self.optTour = getMap(mapNum)

        # Create the adjList of vertices
        self.adjList = []
        for rank in range(0, len(self.cities)):
            v = Vertex(rank)
            self.adjList.append(v)

        # Create the list of edges and fill the vertex.neigh values.
        # Fill in the cities while we are at it.
        self.edgeList = []
        for r1 in range(0, len(self.adjMat)):
            v1 = self.adjList[r1]
            v1.city = self.cities[r1]
            for r2 in range(r1 + 1, len(self.adjMat[r1])):
                if self.adjMat[r1][r2] != 0:
                    v2 = self.adjList[r2]
                    v1.neigh.append(v2)
                    v2.neigh.append(v1)
                    e = Edge(v1, v2, self.adjMat[r1][r2])
                    self.edgeList.append(e)

        # Sort the edges.
        self.edgeList.sort()

        # Set start to the 0 ranked vertex (the first city).
        self.start = self.adjList[0]

        # Set the MSTalg.
        self.MSTalg = MSTalg

        # Empty MST initially.
        self.mst = []

        # Empty tour initially.
        self.tour = []
        return

    """
    __repr__ function to print a map.
    """

    def __repr__(self):
        # First the MST edges.
        s = ''
        s += '\nMST Edges:\n'
        w = 0
        for e in self.mst:
            s += repr(e) + '\n'
            w += e.weight
        s += '\nMST Weight:\n%f\n' % w

        # Now the tour.
        s += '\nTSP Approx. Tour:\n'
        w = 0
        if len(self.tour) > 0:
            for r in range(0, len(self.tour) - 1):
                s += self.cities[self.tour[r]] + '\n'
                w += self.adjMat[self.tour[r]][self.tour[r + 1]]
            s += self.cities[self.tour[0]] + '\n'
        else:
            w = math.inf
        s += '\nTSP Approx. Tour Weight:\n%f\n' % w

        # Now the optimal tour.
        s += self.optTour

        # Return the repr string.
        return s

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
    Note: for the larger matrices, this will still likely be hard to read.
    """

    def printMat(self):
        for row in self.adjMat:
            print(row)
        return

    """
    printEdges function prints the edge list of the Map.
    """

    def printEdges(self):
        s = 'Edge List:\n'
        for e in self.edgeList:
            s += repr(e) + '\n'
        print(s)
        return

    """
    getMST: uses MSTalg to get the MST and fill in the edges
    """

    def getMST(self):
        if self.MSTalg == prim:
            # Call Prim's on the adjList and adjMat.
            # This should update all of the vertices' prev values.
            prim(self.adjList, self.adjMat)

            # Now that we've set all of the prev values, go through each vertex
            # and update its mstN list.
            for v in self.adjList:
                if not v.prev is None:
                    v.mstN.append(v.prev)
                    v.prev.mstN.append(v)

            # Loop through the vertices and add the MST edges.
            for rank in range(0, len(self.adjList)):
                v = self.adjList[rank]
                for neighbor in v.mstN:
                    if neighbor.rank > rank:
                        e = Edge(v, neighbor, self.adjMat[rank][neighbor.rank])
                        self.mst.append(e)
            return

        elif self.MSTalg == kruskal:
            # Call Kruskal's on the adjList and edgeList.
            # This will return the mst edges.
            self.mst = kruskal(self.adjList, self.edgeList)

            # Now that the MST is set, loop through the edges and update the
            # mstN values for the vertices.
            for e in self.mst:
                u = e.vertices[0]
                v = e.vertices[1]
                u.mstN.append(v)
                v.mstN.append(u)
            return
        else:
            raise Exception('Not a valid MST alg.')

    """
    getTSP: uses the MST to find the approximate solution to TSP.
    """

    def getTSP(self):
        if len(self.mst) > 0:
            self.tour = tsp(self.adjList, self.start)
        else:
            raise Exception('No MST set!')
        return

    """
    clearMap: this function will reset the MST and tour for the map, along with
              all vertex info.
    """

    def clearMap(self):
        # Create the adjList of vertices
        self.adjList = []
        for rank in range(0, len(self.cities)):
            v = Vertex(rank)
            self.adjList.append(v)

        # Create the list of edges and fill the vertex.neigh values.
        # Fill in the cities while we are at it.
        self.edgeList = []
        for r1 in range(0, len(self.adjMat)):
            v1 = self.adjList[r1]
            v1.city = self.cities[r1]
            for r2 in range(r1 + 1, len(self.adjMat[r1])):
                if self.adjMat[r1][r2] != 0:
                    v2 = self.adjList[r2]
                    v1.neigh.append(v2)
                    v2.neigh.append(v1)
                    e = Edge(v1, v2, self.adjMat[r1][r2])
                    self.edgeList.append(e)

        # Sort the edges.
        self.edgeList.sort()

        # Set start to the 0 ranked vertex (the first city).
        self.start = self.adjList[0]

        # Empty MST initially.
        self.mst = []

        # Empty tour initially.
        self.tour = []


################################################################################

"""
getMap

This function will return the adjacency matrix and city names for the map.

INPUTS
mapNum: the number of which map to select.

OUTPUTS
adjMat:   the adjacency matrix.
cityList: the list of the cities.
"""


def getMap(mapNum=0):
    if mapNum == 0:
        cityList = ['a', 'b', 'c', 'd']
        adjMat = [[0, 2, 8, 5], \
                  [2, 0, 7, 4], \
                  [8, 7, 0, 6], \
                  [5, 4, 6, 0]]
        optTour = '\nOptimal Tour:' + \
                  '\na\nb\nc\nd\na\n\nWeight of Optimal Tour:\n20'
        return adjMat, cityList, optTour

    elif mapNum == 1:
        cityList = ['a', 'b', 'c', 'd']
        adjMat = [[0, 2, 2, 3], \
                  [2, 0, 3, 2], \
                  [2, 3, 0, 2], \
                  [3, 2, 2, 0]]
        optTour = '\nOptimal Tour:' + \
                  '\na\nb\nd\nc\na\n\nWeight of Optimal Tour:\n8'
        return adjMat, cityList, optTour


    elif mapNum == 2:
        cityList = ['NYC', 'Urbandale', 'Chicago', 'Durham', 'LA', 'Seattle', \
                    'Washington DC']
        lats = [40.71, 41.63, 41.88, 35.99, 34.05, 47.61, 38.91]
        longs = [74.01, 93.71, 87.63, 78.90, 118.24, 122.33, 77.04]
        optTour = '\nOptimal Tour:\nNYC\nChicago\nUrbandale\nSeattle\nLA' + \
                  '\nDurham\nWashington DC\nNYC\n\nWeight of Optimal ' + \
                  'Tour:\n9796'

    elif mapNum == 3:
        cityList = ['London', 'Paris', 'Madrid', 'Rome', 'Berlin', 'Istanbul', \
                    'Moscow', 'Athens', 'Copenhagen']
        lats = [51.51, 48.86, 40.42, 41.90, 52.52, 41.01, 55.76, 37.98, 55.68]
        longs = [0.13, -2.35, 3.70, -12.50, -13.41, -28.98, -37.62, -23.73, -12.57]
        optTour = '\nOptimal Tour:\nLondon\nBerlin\nCopenhagen\nMoscow\n' + \
                  'Istanbul\nAthens\nRome\nMadrid\nParis\nLondon\n\nWeight ' + \
                  'of Optimal Tour:\n8978'

    elif mapNum == 4:
        cityList = ['NYC', 'Urbandale', 'Chicago', 'Durham', 'LA', 'Seattle', \
                    'Washington DC', 'Houston', 'Phoenix', 'Denver', \
                    'San Francisco', 'Honolulu', 'Boston', 'Cleveland']
        lats = [40.71, 41.63, 41.88, 35.99, 34.05, 47.61, 38.91, \
                29.76, 33.45, 39.74, 37.77, 21.31, 42.36, 41.50]
        longs = [74.01, 93.71, 87.63, 78.90, 118.24, 122.33, 77.04, \
                 95.37, 112.07, 104.99, 122.42, 157.86, 71.06, 81.69]
        optTour = '\nOptimal Tour: ?'

    elif mapNum == 5:
        cityList = ['London', 'Paris', 'Madrid', 'Rome', 'Berlin', 'Istanbul', \
                    'Moscow', 'Athens', 'Copenhagen', 'Dublin', 'Warsaw', \
                    'Kiev']
        lats = [51.51, 48.86, 40.42, 41.90, 52.52, 41.01, 55.76, 37.98, 55.68, \
                53.35, 52.23, 50.45]

        longs = [0.13, -2.35, 3.70, -12.50, -13.41, -28.98, -37.62, -23.73, -12.57, \
                 6.26, -21.01, -30.52]
        optTour = '\nOptimal Tour:\nLondon\nParis\nMadrid\nRome\nAthens\n' + \
                  'Istanbul\nKiev\nMoscow\nWarsaw\nBerlin\nCopenhagen\n' + \
                  'Dublin\nLondon\n\nWeight of Optimal Tour:\n9911'

    elif mapNum == 6:
        cityList = ['London', 'Paris', 'Madrid', 'Rome', 'Berlin', 'Istanbul', \
                    'Moscow', 'Athens', 'Copenhagen', 'Dublin', 'Warsaw', \
                    'Kiev', 'St. Petersburg', 'Stockholm']
        lats = [51.51, 48.86, 40.42, 41.90, 52.52, 41.01, 55.76, 37.98, 55.68, \
                53.35, 52.23, 50.45, 59.93, 59.33]
        longs = [0.13, -2.35, 3.70, -12.50, -13.41, -28.98, -37.62, -23.73, -12.57, \
                 6.26, -21.01, -30.52, -30.34, -18.07]
        optTour = '\nOptimal Tour: ?'

    elif mapNum == 7:
        N = 75
        cityList = []
        lats = []
        longs = []
        lab = 0
        for ind in range(0, N + 1):
            cityList.append(str(lab))
            lats.append(ind * 180 / N - 90)
            longs.append(-10)
            lab += 1
        for ind in range(1, N - 1):
            cityList.append(str(lab))
            lats.append(90 - ind * 180 / N)
            longs.append(170)
            lab += 1
        antiPolar = -(lats[0] + lats[-1]) / 2
        lats.append(antiPolar)
        longs.append(-10)
        cityList.append(str(lab))
        optTour = '\nOptimal Tour: 40030.173592'

    elif mapNum == 8:
        N = 75
        cityList = []
        lats = []
        longs = []
        lab = 0
        for ind in range(0, N + 1):
            cityList.append(str(lab))
            lats.append(ind * 180 / N - 90)
            longs.append(-10)
            lab += 1
        for ind in range(1, N - 1):
            cityList.append(str(lab))
            lats.append(90 - ind * 180 / N)
            longs.append(170)
            lab += 1
        antiPolar = -(lats[0] + lats[-1]) / 2
        lats.insert(0, antiPolar)
        longs.insert(0, -10)
        cityList.insert(0, str(lab))
        optTour = '\nOptimal Tour: 40030.173592'

    else:
        raise Exception('Not a valid map number.')

    # Get the distances and insert into the adjacency matrix.
    adjMat = [[0 for x in range(0, len(cityList))] \
              for x in range(0, len(cityList))]
    for r in range(0, len(adjMat)):
        for c in range(r + 1, len(adjMat[r])):
            adjMat[r][c] = getDist(lats[r], longs[r], lats[c], longs[c])
            adjMat[c][r] = adjMat[r][c]
        adjMat[r][r] = 0

    return adjMat, cityList, optTour


################################################################################

"""
getDist

This function takes in two coordinates and returns the distance between them
(in kilometers).

INPUTS
lat1, long1: the latitude and longitude of the first city.
lat2, long2: the latitude and longitude of the second city.

OUTPUTS
dist: the distance between the two cities (km).
"""


def getDist(lat1, long1, lat2, long2):
    # Convert to radians.
    lat1 = lat1 * math.pi / 180
    long1 = long1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    long2 = long2 * math.pi / 180

    # Calculate the change in lat and long.
    dLat = lat2 - lat1
    dLong = long2 - long1

    # Set the radius of the Earth.
    R = 6371  # km

    # Calculate the distance using the formula for distance on a great circle.
    a = math.sin(dLat / 2) ** 2 \
        + \
        ( \
                    math.cos(lat1) * math.cos(lat2) \
                    * \
                    math.sin(dLong / 2) ** 2 \
            )
    if abs(a) < 1e-15: a = 0
    if abs(1 - a) < 1e-15: a = 1
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist = R * c
    return dist  # km