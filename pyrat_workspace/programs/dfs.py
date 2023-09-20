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
import random

# Previously developed functions
from tutorial import get_neighbors, locations_to_action 

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def traversal ( source              :   int,
                graph               :   Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                create_structure    :   Callable[[], Any],
                push_to_structure   :   Callable[[Any, Tuple[int, int, int]], None],
                pop_from_structure  :   Callable[[Any], Tuple[int, int, int]]
              ) -> Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
        Traversal function that explores a graph from a given vertex.
        This function is generic and can be used for most graph traversal.
        To adapt it to a specific traversal, you need to provide the adapted functions to create, push and pop elements from the structure.
        In:
            * source:             Vertex from which to start the traversal.
            * graph:              Graph on which to perform the traversal.
            * create_structure:   Function that creates an empty structure to use in the traversal.
            * push_to_structure:  Function that adds an element of type B to the structure of type A.
            * pop_from_structure: Function that returns and removes an element of type B from the structure of type A.
        Out:
            * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
            * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """
    visited_vertices = []
    queue_structure = create_structure()

    routing_table = {source: None}
    distances_to_explored_vertices = {source: 0}

    # Create the FIFO queue using the provided function
    push_to_structure(queue_structure, (source, 0, None))  # push (vertex, distance, parent)

    while queue_structure :

        # Pop the current vertex from the queue
        vertex, distance, parent = pop_from_structure(queue_structure)
        
        # If the vertex has not been visited
        if vertex not in visited_vertices:

            visited_vertices.append(vertex)
            distances_to_explored_vertices[vertex] = distance
            routing_table[vertex] = parent
            
            # Loop over the neighbors of the current vertex
            for neighbor in get_neighbors(vertex, graph) :
                if neighbor not in visited_vertices:
                    push_to_structure(queue_structure, (neighbor, distance + 1, vertex))

    return distances_to_explored_vertices, routing_table


def dfs ( source    : int,
          graph     : Union[numpy.ndarray, Dict[int, Dict[int, int]]]
        ) -> Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
    A dfs is a particular traversal where vertices are explored in the order where they are added to the structure.
    In:
        * source: Vertex from which to start the traversal.
        * graph:  Graph on which to perform the traversal.
    Out:
        * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
        * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """

    # Function to create an empty FIFO, encoded as a list
    def _create_structure() -> List[int] :
        return []
    
    # Function to add an element to the FIFO (elements enter by the end)
    def _push_to_structure(structure: List[int], element: int) -> None:
        structure.append(element)
        return None
    
    # Function to extract an element from the FIFO (elements exit by the beginning)
    def _pop_from_structure(structure: List[int]) -> int:
        return structure.pop(-1)
    
    distances_to_explored_vertices, routing_table = traversal(source, graph, _create_structure, _push_to_structure, _pop_from_structure)
    return distances_to_explored_vertices, routing_table


def find_route(routing_table: Dict[int, Union[None, int]],
               source: int,
               target: int) -> List[int]:
    """
    Function to return a sequence of locations using a provided routing table.
    In:
        * routing_table: Routing table as obtained by the traversal.
        * source:        Vertex from which we start the route (should be the one matching the routing table).
        * target:        Target to reach using the routing table.
    Out:
        * route: Sequence of locations to reach the target from the source, as performed in the traversal.
    """

    route = [target]  # Start with the target

    while target != source:  # While we haven't reached the source
        
        target = routing_table[target]  # Get the parent of the current target
        
        if target is None:  # If we don't find a parent, the route is incomplete
            raise ValueError("No route found from source to target using the provided routing table.")
        
        route.append(target)

    return route[::-1]  # Reverse the route to get from source to target


def locations_to_actions ( locations:  List[int],
                           maze_width: int
                         ) ->          List[str]: 
    """
        Function to transform a list of locations into a list of actions to reach vertex i+1 from vertex i.
        In:
            * locations:  List of locations to visit in order.
            * maze_width: Width of the maze in number of cells.
        Out:
            * actions: Sequence of actions to visit the list of locations.
    """
    
    # We iteratively transforms pairs of locations in the corresponding action
    actions = []
    for i in range(len(locations) - 1):
        
        action = locations_to_action(locations[i], locations[i + 1], maze_width)
        actions.append(action)
    
    return actions

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

    # [TODO] Write your preprocessing code here
    # Use dfs to compute shortest path from player's starting position to every other position
    start_location = player_locations[name]
    distances, routing_table = dfs(start_location, maze)
    
    # Store distances and routing_table in memory to be used in the turn function
    memory.distances = distances
    memory.routing_table = routing_table
    
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

    # Current location of the player
    current_location = player_locations[name]

    # Find the nearest cheese
    nearest_cheese_distance = float('inf')
    nearest_cheese_location = None

    for cheese_location in cheese:

        if memory.distances[cheese_location] < nearest_cheese_distance:
        
            nearest_cheese_distance = memory.distances[cheese_location]
            nearest_cheese_location = cheese_location

    # If no cheese is reachable, return a random move
    if nearest_cheese_location is None:
        
        return random.choice(possible_actions)

    # Use the routing table to find the next move towards the nearest cheese
    path_to_cheese = find_route(memory.routing_table, current_location, nearest_cheese_location)
    actions_to_cheese = locations_to_actions(path_to_cheese, maze_width)
    
    # Take the first action from the list of actions
    return actions_to_cheese[0]

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
    players = [{"name": "DFS", "preprocessing_function": preprocessing, "turn_function": turn, "postprocessing_function": postprocessing}]

    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage": 0.0,
              "nb_cheese": 1}

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################
