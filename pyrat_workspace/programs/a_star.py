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
from queue import PriorityQueue

# Previously developed functions
from tutorial import get_neighbors, get_weight
from dijkstra import find_route, locations_to_actions

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def manhattan_distance ( vertex1: int,
                         vertex2: int,
                         maze_width: int
                       ) -> float:
    """
        The heuristic function.
        Computes the Manhattan distance between two vertices in a grid.
        
        In:
            * vertex1:   The first vertex.
            * vertex2:   The second vertex.
            * maze_width: Width of the maze in number of cells.
            
        Out:
            * The Manhattan distance between the two vertices.
    """
    # Convert vertex1 to its x and y coordinates
    x1, y1 = vertex1 % maze_width, vertex1 // maze_width
    
    # Convert vertex2 to its x and y coordinates
    x2, y2 = vertex2 % maze_width, vertex2 // maze_width
    
    # Calculate the Manhattan distance
    res = abs(x1 - x2) + abs(y1 - y2)
    
    return res

#####################################################################################################################################################

def a_star ( start: int,
             target: int,
             graph: Union[numpy.ndarray, Dict[int, Dict[int, int]]],
             heuristic: Callable[[int, int], float],
             maze_width : int
           ) -> List[int] :
    """
        A* search algorithm.
        This function returns a path from the start location to the target location in a maze using a heuristic.
        
        In:
            * start:      Starting vertex.
            * target:     Target vertex.
            * graph:      Graph representation of the maze.
            * heuristic:  Heuristic function to estimate the distance from a vertex to the target.
            * maze_width: Width of the maze in number of cells. 
            
        Out:
            * List of vertices representing the path from start to target. If no path is found, returns an empty list.
    """
    # Nodes that have already been analyzed and have a path from the start to them
    closed_set = set() 

    # Nodes that are yet to be analyzed but have a known path from the start node
    open_set = set([start]) 

    # A dictionary that maps each node to its predecessor. This is used to reconstruct the path at the end.
    routing_table = {}

    # For each node, the cost of getting from the start node to that node.
    g_score = {node: float('inf') for node in graph.keys()}
    g_score[start] = 0

    # For each node, the total cost of getting from the start node to the goal by passing by that node.
    f_score = {node: float('inf') for node in graph.keys()}
    f_score[start] = heuristic(start, target, maze_width)

    # Nodes to be evaluated, with f_score as the priority
    open_queue = PriorityQueue()
    open_queue.put((f_score[start], start))

    while not open_queue.empty():
        
        # Get the node in open_set having the lowest f_score value
        _, current = open_queue.get()

        # If the current node is already evaluated, skip it
        if current in closed_set:
            continue

        # If we have reached the goal, reconstruct and return the path
        if current == target:
            return _reconstruct_path(routing_table, start, target), g_score[current]

        open_set.remove(current)
        closed_set.add(current)

        # Evaluate all neighbors of the current node
        for neighbor in get_neighbors(current, graph):
            
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + get_weight(current, neighbor, graph)

            if tentative_g_score < g_score[neighbor]:

                # Mise à jour de la table de routage pour indiquer que le chemin actuel vers 'neighbor' passe par le nœud 'current'.
                routing_table[neighbor] = current

                # Mise à jour du coût du chemin le plus court connu pour se rendre de 'start' à 'neighbor'.
                g_score[neighbor] = tentative_g_score

                # Mise à jour de l'estimation du coût total pour se rendre du nœud de départ au nœud cible
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target, maze_width)

                # Ajout du nœud 'neighbor' à l'ensemble des nœuds à évaluer.
                open_set.add(neighbor)

                # Ajout du nœud 'neighbor' à la file de priorité avec son 'f_score' comme priorité.
                open_queue.put((f_score[neighbor], neighbor))
    
    # If we reach here, there is no path from start to target
    return [], float('inf')

#####################################################################################################################################################

def _reconstruct_path ( routing_table , 
                        start : int,
                        target: int
                      ) -> List[int] :
    """
    Reconstruct the path from start to goal using the came_from dictionary.

    In:
        * routing_table:    A dictionary mapping a node to its predecessor in the path.
        * start:            The starting node.
        * target:           The goal node.
    
    Out:
        * path: A list representing the path from start to goal.
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
    start_location = player_locations[name]

    # A* Path to cheese
    path_to_cheese_a_star, _ = a_star(start_location, cheese[0], maze, manhattan_distance, maze_width)
    actions_to_cheese_a_star = locations_to_actions(path_to_cheese_a_star, maze_width)
    
    # Store the actions to the cheese in memory
    memory.actions_to_cheese_a_star = actions_to_cheese_a_star


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

    if not memory.actions_to_cheese_a_star :
        return random.choice(possible_actions)

    action = memory.actions_to_cheese_a_star.pop(0)
    return action

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Map the functions to the character
    players = [{"name": "A*", "preprocessing_function": preprocessing, "turn_function": turn}]
    
    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage": 40.0,
              "nb_cheese": 1,
              "trace_length": 1000
              }
    
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    
    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################