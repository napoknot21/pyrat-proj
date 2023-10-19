#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This program is an improvement of "TSP_2".
    It improves the number of branches that are cut by exploring neighbors in increasing distance to the current vertex of the search.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports
import numpy

# Previously developed functions
from tutorial import get_neighbors
from BFS import locations_to_actions
from TSP_1 import graph_to_metagraph, expand_route

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def tsp ( complete_graph: numpy.ndarray,
          source:         int
        ) ->              Tuple[List[int], int]:

    """
        Function to solve the TSP using an exhaustive search.
        The backtracking mechanism allows stopping exploration of some branches.
        Vertices are explored in increasing distance to quickly find a good solution and cut more branches.
        In:
            * complete_graph: Complete graph of the vertices of interest.
            * source:         Vertex used to start the search.
        Out:
            * best_route:  Best route found in the search.
            * best_length: Length of the best route found.
    """
    
    # We sort the neighbors in increasing distance
    sorted_neighbors = {}
    for vertex in range(complete_graph.shape[0]):
        neighbors = get_neighbors(vertex, complete_graph)
        neighbors_weights = [complete_graph[vertex, neighbor] for neighbor in neighbors]
        sorted_neighbors[vertex] = [neighbors[i] for i in numpy.argsort(neighbors_weights)]
    
    # Subfunction for recursive calls
    def _tsp (current_vertex, current_visited_vertices, current_route, current_length, current_best_route, current_best_length):
        
        # Backtracking
        if current_length >= current_best_length:
            return current_best_route, current_best_length
        
        # If we have a full path, we evaluate it
        if len(current_visited_vertices) == complete_graph.shape[0]:
            if current_length >= current_best_length:
                return current_best_route, current_best_length
            return current_route, current_length
        
        # Otherwise, we explore one more neighbor
        for vertex in sorted_neighbors[current_vertex]:
            if vertex not in current_visited_vertices:
                current_best_route, current_best_length = _tsp(vertex, current_visited_vertices + [vertex], current_route + [vertex], current_length + complete_graph[current_vertex, vertex], current_best_route, current_best_length)
        
        # We propagate the current best
        return current_best_route, current_best_length
    
    # Initialize the search from the source
    best_route, best_length = _tsp(source, [source], [source], 0, None, float("inf"))
    return best_route, best_length
    
#####################################################################################################################################################
##################################################### EXECUTED ONCE AT THE BEGINNING OF THE GAME ####################################################
#####################################################################################################################################################

def preprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                    maze_width:       int,
                    maze_height:      int,
                    name:             str,
                    teams:            Dict[str, List[str]],
                    player_locations: Dict[str, int],
                    cheese:           List[int],
                    possible_actions: List[str],
                    memory:           threading.local
                  ) ->                None:

    """
        This function is called once at the beginning of the game.
        It is typically given more time than the turn function, to perform complex computations.
        Store the results of these computations in the provided memory to reuse them later during turns.
        To do so, you can crete entries in the memory dictionary as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """

    # Build a graph of locations of interest, i.e., initial location and those of pieces of cheese
    locations_of_interest = [player_locations[name]] + cheese
    complete_graph, routing_tables = graph_to_metagraph(maze, locations_of_interest)
    
    # Solve the TSP on that graph
    route, _ = tsp(complete_graph, 0)
    
    # Convert the route in the complete graph into a route in the maze
    maze_route = expand_route(route, routing_tables, locations_of_interest)
    memory.actions_to_perform = locations_to_actions(maze_route, maze_width)

#####################################################################################################################################################
######################################################### EXECUTED AT EACH TURN OF THE GAME #########################################################
#####################################################################################################################################################

def turn ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
           maze_width:       int,
           maze_height:      int,
           name:             str,
           teams:            Dict[str, List[str]],
           player_locations: Dict[str, int],
           player_scores:    Dict[str, float],
           player_muds:      Dict[str, Dict[str, Union[None, int]]],
           cheese:           List[int],
           possible_actions: List[str],
           memory:           threading.local
         ) ->                str:

    """
        This function is called at every turn of the game and should return an action within the set of possible actions.
        You can access the memory you stored during the preprocessing function by doing memory.my_key.
        You can also update the existing memory with new information, or create new entries as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * action: One of the possible actions, as given in possible_actions.
    """

    # Apply actions in order
    action = memory.actions_to_perform.pop(0)
    return action

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Map the functions to the character
    players = [{"name": "TSP exh 3", "preprocessing_function": preprocessing, "turn_function": turn}]

    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "nb_cheese": 10,
              "trace_length": 1000}

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################