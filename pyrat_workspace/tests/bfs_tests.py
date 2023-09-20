#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This program contains all the unit tests for the functions developed in the program "bfs.py".
    Let's consider the following maze for our tests:
    #############################################################
    # (0)       # (1)      # (2)       ⵗ (3)       # (4)        #
    #           #          #           ⵗ           #            #
    #           #          #           ⵗ           #            #
    #⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅############⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅##########################
    # (5)       ⵗ (6)       ⵗ (7)       ⵘ (8)       ⵘ (9)       #
    #           ⵗ           ⵗ           6           9            #
    #           ⵗ           ⵗ           ⵘ           ⵘ           #
    #⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#ⴾⴾⴾⴾⴾⴾ8ⴾⴾⴾⴾⴾⴾ############⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#############
    # (10)      ⵗ (11)      # (12)      # (13)      # (14)      #
    #           ⵗ           #           #           #           #
    #           ⵗ           #           #           #           #
    #ⴾⴾⴾⴾⴾⴾ9ⴾⴾⴾⴾⴾⴾ#⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#############ⴾⴾⴾⴾⴾⴾ6ⴾⴾⴾⴾⴾⴾ#⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#
    # (15)      ⵘ (16)      ⵗ (17)      ⵘ (18)      ⵗ (19)      #
    #           4           ⵗ           5           ⵗ            #
    #           ⵘ           ⵗ           ⵘ           ⵗ           #
    #⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅#
    # (20)      # (21)      ⵗ (22)      # (23)      # (24)      #
    #           #           ⵗ           #           #           #
    #           #           ⵗ           #           #           #
    #############################################################
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports
import unittest
import numpy
import sys
import os

# Previously developed functions
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "programs"))
from bfs import *

#####################################################################################################################################################
############################################################### UNIT TESTS DEFINITION ###############################################################
#####################################################################################################################################################

class TestsTutorial (unittest.TestCase):

    """
        Here we choose to use the unittest module to perform unit tests.
        This module is very simple to use and allows to easily check if the code is working as expected.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any,
                 ) ->        Self:

        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments of the parent constructor.
                * kwargs: Keyword arguments of the parent constructor.
            Out:
                * self: Reference to the current object.
        """

        # Inherit from parent class
        super(TestsTutorial, self).__init__(*args, **kwargs)

        # We need to store the width of the maze
        self.maze_width = 5

        # We define the graph structures that will be used for the tests
        self.graph_dictionary = {0: {5: 1},
                                 2: {3: 1, 7: 1},
                                 3: {2: 1},
                                 5: {0: 1, 6: 1, 10: 1},
                                 6: {5: 1, 7: 1, 11: 8},
                                 7: {2: 1, 3: 1, 6: 1, 8: 6},
                                 8: {7: 6, 9: 9, 13: 1},
                                 9: {8: 9},
                                 10: {5: 1, 11: 1, 15: 9},
                                 11: {6: 8, 10: 1, 16: 1},
                                 13: {8: 1, 18: 6},
                                 14: {19: 1},
                                 15: {10: 9, 16: 4, 20: 1},
                                 16: {11: 1, 15: 4, 17: 1, 21: 1},
                                 17: {16: 1, 18: 5, 22: 1},
                                 18: {13: 6, 17: 5, 19: 1, 23: 1},
                                 19: {14: 1, 18: 1, 24: 1},
                                 20: {15: 1},
                                 21: {16: 1, 22: 1},
                                 22: {17: 1, 21: 1},
                                 23: {18: 1},
                                 24: {19: 1}}
        
        # Here is the same graph represented as an adjacency matrix
        self.graph_matrix = numpy.array([[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 1, 0, 0, 0, 1, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 6, 0, 9, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 0, 1, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 5, 0, 1, 0, 0, 0, 1, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]])
        
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def test_bfs ( self : Self
                 ) -> None :
        
        """
            Tests the "bfs" function from the "bfs.py" module. 
            This test ensures that the "bfs" function correctly computes the distances from a source vertex to all other vertices in the graph.
            The function is tested against both adjacency list (dictionary) and adjacency matrix representations of the graph.

            Parameters:
                * self: Reference to the current test case instance.

            Returns:
                * None.
        """

        for graph in [self.graph_dictionary, self.graph_matrix] :
            
            distances, routing_table = bfs(0, graph)
        
            # We check the distance from the source (vertex 0) to some other vertices
            self.assertEqual(distances[7], 3)
            self.assertEqual(distances[11], 3)
            self.assertEqual(distances[24], 8)

        # Testing with an invalid source vertex
        self.assertRaises(Exception, bfs, -1, self.graph_dictionary) # Negative vertex
        self.assertRaises(Exception, bfs, 1000, self.graph_dictionary) # Out of range vertex

        # Testing with an invalid graph type
        self.assertRaises(Exception, bfs, 0, [1, 2, 3])  # A list is not a valid graph representation

    #############################################################################################################################################

    def test_find_route(self):
        """
        Tests the "find_route" function to ensure it correctly computes a route from source to target using the provided routing table.

        Parameters:
            * self: Reference to the current test case instance.

        Returns:
            * None.
        """

        # We need a routing table to test the function, so let's get one using BFS
        for graph in [self.graph_dictionary, self.graph_matrix]:
            distances, routing_table = bfs(0, graph) 

            # Test with a valid route
            route1 = find_route(routing_table, 0, 7)
            # Ensure the route starts at the source and ends at the target
            self.assertEqual(route1[0], 0) and self.assertEqual(route1[-1], 7)
            # Ensure the entire route is ok
            self.assertEqual(route1, [0, 5, 6, 7])

            route2 = find_route(routing_table, 0, 22)
            # Ensure the route starts at the source and ends at the target
            self.assertEqual(route2[0], 0) and self.assertEqual(route2[-1], 22)
            # Ensure the entire route is ok
            self.assertEqual(route2, [0, 5, 6, 11, 16, 17, 22])

        # Test for an invalid route
        # For this, we need to simulate a missing route in the routing table
        # Assuming that there's no direct path from 0 to 99 in your test graph
        # Modify the number 99 to a valid vertex in your graph but without a direct path from 0
        incomplete_routing_table = routing_table.copy()
        incomplete_routing_table[99] = None 

        with self.assertRaises(ValueError):
            find_route(incomplete_routing_table, 0, 99)


    #############################################################################################################################################

    def test_locations_to_actions  ( self  :  Self  
                                   ) -> None :
        
        """
            This function tests the function "locations_to_action" of the file "bfs.py".
            It checks that the function returns the correct action.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # We check that the function returns the correct action for standard cases
        self.assertEqual(locations_to_actions([16, 11], self.maze_width), ["north"])
        self.assertEqual(locations_to_actions([16, 15], self.maze_width), ["west"])
        self.assertEqual(locations_to_actions([16, 17], self.maze_width), ["east"])
        self.assertEqual(locations_to_actions([16, 21], self.maze_width), ["south"])
        self.assertEqual(locations_to_actions([16, 16], self.maze_width), ["nothing"])

        # The function should raise an exception if the locations are not adjacent
        self.assertRaises(Exception, locations_to_actions, [16, 20], self.maze_width)


#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Run all unit tests
    unittest.main(verbosity=2)

#####################################################################################################################################################
#####################################################################################################################################################

