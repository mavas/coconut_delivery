"""
Here are the segments (jet streams AND the unassisted paths) that are flown with their segment costs:
0->5 10
*5->6 50
6->11 20
*11->14 150
14->17 8
*17->19 100
19->24 14
"""


import unittest, sys


class SwanTest(unittest.TestCase):
    """A test case for the problem.  Not used anymore."""
    def setUp(s):
        with open('sample_paths.txt', 'r') as f:
            c = f.read()
        s.sample = c
        with open('flight_paths.txt', 'r') as f:
            c = f.read()
        s.real = c
    def test_sample(s):
        e, j = find_shortest_path(s.sample)
        s.assertEqual(e, 352)
        s.assertEqual(j, [(0,5), (6,11), (14,17), (19,24)])
    @unittest.skip('')
    def test_real(s):
        e, j = find_shortest_path(s.real)


class JetStream:
    """
    Just a helper class to hold info about a particular JetStream.
    """
    def __init__(self, start, end, energy):
        self.__start = start
        self.__end = end
        self.__energy = energy
        self.predecessor = None
        self.path_energy = sys.maxsize
    def getStart(self): return self.__start
    def getEnd(self): return  self.__end
    def getEnergy(self): return self.__energy
    def __str__(self):
        return (self.__start, self.__end, self.__energy, self.path_energy).__str__()
    def __repr__(self):
        return (self.__start, self.__end, self.__energy, self.path_energy).__str__()


def dijkstra_swan(first_jet_streams, jet_stream_list, adj_list, last_mile, default_path_cost):
    """
    Implementation of Dijkstra's algorithm using a sorted list of nodes
    to compute a shortest path between a pair of nodes

    Returns the energy used, and the optimal path
    """
    # Choose a source
    source = first_jet_streams[0]
    # Create our priority queue of pathLength
    jet_stream_list.sort(key=lambda x: x.path_energy, reverse=True)
    while len(jet_stream_list) > 0:
        node = jet_stream_list.pop()
        i = node.getEnd()
        nodeEnergy = node.path_energy
        # Increment the energy cost until we encounter another jetstream
        while i not in adj_list and i < last_mile:
            i += 1
            nodeEnergy += default_path_cost
        # Check and see if we've reached the goal
        if i == last_mile:
            minPath = []
            while node:
                minPath.insert(0, (node.getStart(), node.getEnd()))
                node = node.predecessor
            minEnergy = nodeEnergy;
            return (minEnergy, minPath)
        for childNode in adj_list[i]:
            newLength = nodeEnergy + childNode.getEnergy()
            # If the computed path energy is smaller, store it and store
            # the new predecessor
            if newLength < childNode.path_energy:
                childNode.path_energy = newLength
                childNode.predecessor = node
        # Keep our priority queue sorted
        jet_stream_list.sort(key=lambda x: x.path_energy, reverse=True)


def parse_input_file():
    """
    Parses the input file, and returns a tuple of information.
    """
    min_start = sys.maxsize
    adj_list = dict()
    last_mile = 0
    jet_stream_list = list()
    with open(sys.argv[1]) as f:
        ln = 0
        for l in f:
            data = l.split(' ')
            if ln == 0:
                if len(data) > 0:
                    default_path_cost = int(data[0])
            elif len(data) >= 3:
                # Subsequent lines should have 3 integers, the start
                # mile, end mile, and energy to traverse that distance
                start = int(data[0])
                end = int(data[1])
                energy = int(data[2])
                jet_stream = JetStream(start, end, energy)
                # default the path energy to the maximum it could be
                jet_stream.path_energy = start * default_path_cost + energy
                # Add the JetStream to an adjacency list
                # representation by start mile
                if start not in adj_list:
                    adj_list[start] = []
                adj_list[start].append(jet_stream)
                # Store the last mile marker
                last_mile = max(last_mile, end)
                # Add it to a full list of jetStreams
                jet_stream_list.append(jet_stream)
                # Store the first jet streams we have to have a proper
                # starting point
                if start < min_start:
                    first_jet_streams = []
                    first_jet_streams.append(jet_stream)
                    min_start = start
                elif start <= min_start:
                    first_jet_streams.append(jet_stream)
            ln += 1
    return (default_path_cost, jet_stream_list, first_jet_streams, adj_list, last_mile)


def find_shortest_path():
    """
    Computes the shortest path for the swan.

    Returns the energy consumed, and the sequence of jet streams used.
    """
    default_path_cost, jet_stream_list, first_jet_streams, adj_list, last_mile = parse_input_file()
    e, j = dijkstra_swan(first_jet_streams, jet_stream_list, adj_list, last_mile, default_path_cost)
    return (e, j)


if __name__ == '__main__':
    e, j = find_shortest_path()
    print(e)
    print(j)
    #unittest.main()
