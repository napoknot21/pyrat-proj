#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    Contrary to the "template.py" file, there are 2 players here.
    Here, opponent is "random_3.py".
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports# External imports 
import random

# Previously developed functions
from tutorial import get_neighbors, locations_to_action

# [TODO] Put imports of functions you have developed in previous lessons here
import tsp_1 as opponent

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all developed functions in an easily identifiable section

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
    # To store the already visited cells
    memory.visited_cells = []
    memory.trajectory = []
    
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

    # [TODO] Write your turn code here and do not forget to return a possible action
    #Mark current cell as visited
    if player_locations[name] not in memory.visited_cells:
        memory.visited_cells.append(player_locations[name])

    memory.trajectory.append(player_locations[name])

    # Go to an unvisited neighbor in priority
    neighbors = get_neighbors(player_locations[name], maze)
    unvisited_neighbors = [neighbor for neighbor in neighbors if neighbor not in memory.visited_cells]
    if len(unvisited_neighbors) > 0:
        neighbor = random.choice(unvisited_neighbors)
        memory.visited_cells.append(neighbor)
        
    # If there is no unvisited neighbor, choose one randomly
    else:
        
        if len(memory.trajectory )> 0 :
        
            memory.trajectory.pop()
            neighbor = memory.trajectory[-1]
            memory.trajectory.pop()
        
        else :
        
            neighbor = random.choice(neighbors)

    
    # Retrieve the corresponding action
    action = locations_to_action(player_locations[name], neighbor, maze_width)
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
    players = [{"name": "Template 2", "team": "You", "skin": "rat", "preprocessing_function": preprocessing, "turn_function": turn, "postprocessing_function": postprocessing},
               {"name": "Random 3", "team": "Opponent", "skin": "python", "preprocessing_function": opponent.preprocessing if "preprocessing" in dir(opponent) else None, "turn_function": opponent.turn, "postprocessing_function": opponent.postprocessing if "postprocessing" in dir(opponent) else None}]

    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage": 0.0,
              "nb_cheese": 21}

    # Start the game
    game = PyRat(players, **config)
    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################