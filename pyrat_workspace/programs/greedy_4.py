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
from typing import Optional
# External imports 
import random, heapq

# Previously developed functions
from tutorial import get_neighbors, locations_to_action
from dijkstra import *
from a_star import *

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def nearby_cheese ( current_position: int,
                    cheeses: List[int],
                    max_distance: float = 5
                  ) -> Optional[int] :
    """
    Returns the nearest cheese if it's within the max_distance.

    In:
        * current_position:     Current position.
        * cheeses:              Location of the cheese to evaluate.
        * max_distance:         Maximal distance for searching.
        
    Out:
        * minimal_cheese:       The nearest cheese in a radius of 5 (or max_distance).
    """
    
    # Create a list comprehension to filter cheeses that are within the max_distance from the current position.
    nearby = [cheese for cheese in cheeses if abs(current_position - cheese) <= max_distance]
    
    # If there's at least one cheese that meets the criteria:
    if nearby:

        # Determine the closest cheese by minimizing the absolute difference from the current position.
        minimal_cheese = min(nearby, key=lambda cheese: abs(current_position - cheese))
        
        # Return the closest cheese.
        return minimal_cheese
    
    # If no cheeses are found within the max_distance, return None.
    return None

#####################################################################################################################################################

def cheese_density(maze: Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                           cheese_location: int, 
                           cheeses: List[int], 
                           maze_width: int, 
                           D: int) -> float:
    """
    Computes the sum of distances from a given cheese to the D closest cheeses.
    
    In:
        * maze:             Map of the maze.
        * cheese_location:  Location of the cheese to evaluate.
        * cheeses:          List of all available pieces of cheese in the maze.
        * maze_width:       Width of the maze in number of cells.
        * D:                Number of closest cheeses to consider.
        
    Out:
        * density_score:    Sum of distances to the D closest cheeses.
    """
    
    # List to store distances from the cheese_location to other pieces of cheese
    distances = []

    # Loop through each piece of cheese
    for fromage in cheeses:
        
        # We don't want to measure the distance from the cheese to itself
        if fromage != cheese_location:
            
            # Calculate the Manhattan distance from cheese_location to the current 'fromage'
            distance = manhattan_distance(cheese_location, fromage, maze_width)
            
            # If the calculated distance is within the limit (D), add it to the distances list
            if distance <= D:
                distances.append(distance)
    
    # Compute the "density score": sum of the inverses of the distances, incremented by 1
    # This gives a higher value for closer cheeses, representing higher "density"
    densite = sum(1 / (distance + 1) for distance in distances)
    
    return densite

#####################################################################################################################################################

def greedy ( graph: Union[numpy.ndarray, Dict[int, Dict[int, int]]],
             source :   int, 
             vertices : List[int],
             maze_width: int,
             lambda_coefficient: float = 0.5
           ) ->  int :
    """
    Determines the optimal vertex to target from a list of vertices based on A* search algorithm.
    
    This function computes the shortest path from a given source to all the vertices provided 
    in the list using A* search algorithm and a Manhattan distance heuristic. It returns the 
    optimal path and the associated target vertex.
    
    In:
        * graph : A representation of the maze in which the shortest path is to be found. 
        * source : The starting vertex from which the paths to the vertices are to be determined.
        * vertices : A list of target vertices to which the shortest path from the source is to be determined.
        * maze_width : Width of the maze in number of cells. Used for the Manhattan distance heuristic.
        * lambda_coefficient : A weight parameter to balance the influence of cheese density in the score calculation.
    
    Out:
        * route : The optimal path from the source to the best target vertex 
        * best_cheese : The optimal target vertex itself.
    """
    
    # Initialize variables to store the shortest distance found and the corresponding optimal cheese vertex
    best_score = float('inf')
    best_cheese = None
    route = None

    # Iterate over each cheese in the list of vertices
    for cheese in vertices:
        
        # Compute the density score of the cheese, representing its proximity to other cheeses
        density = cheese_density(graph, cheese, vertices, maze_width, D=5)
        
        # Calculate the shortest path from the source to the current cheese using A* algorithm
        player_path, distance_to_cheese = a_star(source, cheese, graph, manhattan_distance, maze_width)

        # Combine the calculated distance and density score into a single evaluation score
        # A lower score is better, indicating a closer and denser cheese
        score = distance_to_cheese + lambda_coefficient * (1 - density)

        # Update the best score, cheese, and route if the current cheese provides a better score
        if score < best_score:
            best_score = score
            best_cheese = cheese
            route = player_path

    # Return the optimal path and the best cheese vertex
    return route, best_cheese

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

    route, cheese_goal = greedy (maze, source, cheese, maze_width)
    
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
    
        route_new, cheese_goal_new = greedy (maze, player_locations[name], cheese, maze_width)
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
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage": 40.0,
              "nb_cheese": 21,
              "trace_length": 1000}
    
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    
    # Show statistics
    print(stats)

#################################################################################################################
#################################################################################################################