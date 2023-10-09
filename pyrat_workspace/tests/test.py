# Import PyRat
from pyrat import *

# External imports
import unittest
import numpy
import sys
import os

# Previously developed functions
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "programs"))
from tsp_1 import *


class TestYourProgram(unittest.TestCase):
    def setUp(self):
        # Define test data
        self.maze = numpy.array([[0, 1, 0, 0],
                              [1, 0, 1, 0],
                              [0, 1, 0, 1],
                              [0, 0, 1, 0]])
        self.vertices = [0, 1, 2, 3]

    def test_graph_to_metagraph(self):
        # Test the graph_to_metagraph function
        complete_graph, routing_tables = graph_to_metagraph(self.maze, self.vertices)

        # Assert that complete_graph is a dictionary
        self.assertIsInstance(complete_graph, dict)
        
        # Assert that routing_tables is a dictionary
        self.assertIsInstance(routing_tables, dict)

        # Add more specific assertions based on your expected output

    def test_tsp(self):
        # Test the tsp function
        complete_graph = {0: {1: 1, 2: 2, 3: 3},
                         1: {0: 1, 2: 1, 3: 2},
                         2: {0: 2, 1: 1, 3: 1},
                         3: {0: 3, 1: 2, 2: 1}}
        source = 0

        best_route, best_length = tsp(complete_graph, source, 0, [], threading.local())

        # Add assertions to check if the best_route and best_length are as expected

    def test_expand_route(self):
        # Test the expand_route function
        route_in_complete_graph = [0, 1, 2, 3]
        routing_tables = {0: {1: [0, 1], 2: [0, 2], 3: [0, 2, 3]},
                          1: {0: [1, 0], 2: [1, 2], 3: [1, 2, 3]},
                          2: {0: [2, 0], 1: [2, 1], 3: [2, 3]},
                          3: {0: [3, 2, 0], 1: [3, 2, 1], 2: [3, 2]}}
        
        expanded_route = expand_route(route_in_complete_graph, routing_tables)

        # Add assertions to check if the expanded_route is as expected

if __name__ == '__main__':
    unittest.main()