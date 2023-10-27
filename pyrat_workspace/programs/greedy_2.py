#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This program is an empty PyRat program file.
    It serves as a template for your own programs.
    Some [TODO] comments below are here to help you keep your code organized.
    Note that all PyRat programs must have a "turn" function.
    Functions "preprocessing" and "postprocessing" are optional.
    Please check the documentation of these functions for more info on their purpose.
    Also, the PyRat website gives more detailed explanation on how a PyRat game works.
    https://formations.imt-atlantique.fr/pyrat
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports 
import random, heapq

# Previously developed functions
from tutorial import get_neighbors, locations_to_action
from dijkstra import dijkstra, locations_to_actions, find_route, traversal

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def give_score ( graph:          Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                 current_vertex: int,
                 targets:        List[int]
               ) ->              Tuple[List[float], Dict[int, Union[None, int]]]:
    """
        Function that associates a score to each target.
        In:
            * graph:          Graph containing the vertices.
            * current_vertex: Current location of the player in the maze.
            
        Out:
            * scores:        Scores given to the targets.
            * routing_table: Routing table obtained from the current vertex.
    """

    # Call Dijkstra's algorithm to get distances and predecessors from the current vertex.
    distances, routing_tables = dijkstra(current_vertex, graph)
    
    # Score for a target is its shortest distance from the current vertex.
    scores = {target: distances[target] for target in targets}
    
    # Return the scores and the routing table.
    return scores, routing_tables

#####################################################################################################################################################

def greedy ( graph:          Union[numpy.ndarray, Dict[int, Dict[int, int]]],
             initial_vertex: int,
             vertices:       List[int]
           ) ->              List[int]:
    """
        Greedy algorithm that goes to the score maximizer in a loop.
        In:
            * graph:          Graph containing the vertices.
            * initial_vertex: Initial location of the player in the maze.
            * vertices:       Vertices to visit with the greedy heuristic.
        Out:
            * route: Route to follow to perform the path through all vertices.
    """
    # Start with the target node (end point of the desired path)
    current = target

    # Initialize the path with just the target node for now
    path = [current]

    # Loop back through the path using the routing table (came_from dictionary)
    # until we reach the start node
    while current != start:
        
        # Update the current node to its predecessor in the path
        current = routing_table[current]

        # Insert the current node at the beginning of the path
        # This is because we're reconstructing the path from end to start
        path.insert(0, current)
    
    # Return the reconstructed path
    return path

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

    source = player_locations[name]

    route, cheese_goal = greedy (maze, source, cheese)
    
    memory.route = route
    memory.goal = cheese_goal
    
    memory.actions = locations_to_actions(memory.route, maze_width)
    
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
    
    if (memory.route != [] and memory.goal in cheese):
        
        action = memory.actions.pop(0)
    
    else:
    
        route_new, cheese_goal_new = greedy (maze, player_locations[name], cheese)
        memory.route = route_new
        memory.goal = cheese_goal_new
        memory.actions = locations_to_actions(memory.route, maze_width)
        action = memory.actions.pop(0)

    return action

#####################################################################################################################################################
######################################################## EXECUTED ONCE AT THE END OF THE GAME #######################################################
#####################################################################################################################################################

def postprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                     maze_width:       int,
                     maze_height:      int,
                     name:             str,
                     teams:            Dict[str, List[str]],
                     player_locations: Dict[str, int],
                     player_scores:    Dict[str, float],
                     player_muds:      Dict[str, Dict[str, Union[None, int]]],
                     cheese:           List[int],
                     possible_actions: List[str],
                     memory:           threading.local,
                     stats:            Dict[str, Any],
                   ) ->                None:

    """
        This function is called once at the end of the game.
        It is not timed, and can be used to make some cleanup, analyses of the completed game, model training, etc.
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
            * None.
    """

    # [TODO] Write your postprocessing code here
    pass
    
#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Map the functions to the character
    players = [{"name": "greedy 2", "preprocessing_function": preprocessing, "turn_function": turn}]
    
    # Customize the game elements
    config = {"maze_width": 31,
              "maze_height": 29,
              "mud_percentage": 50.0,
              "nb_cheese": 21,
              "trace_length": 1000}
    
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    
    # Show statistics
    print(stats)

#################################################################################################################
#################################################################################################################