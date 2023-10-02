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
# [TODO] Put all your standard imports (numpy, random, os, heapq...) here

# Previously developed functions
from dijkstra import *

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################


#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def graph_to_metagraph(graph, vertices):
    """
    Function to create a complete graph from given graph vertices.

    Args:
    graph (Union[numpy.ndarray, Dict]): Original graph with vertices of interest.
    vertices (List[int]): Vertices used to construct the complete graph.

    Returns:
    Tuple[numpy.ndarray, Dict]: The complete graph and its corresponding routing tables.
    """
    complete_graph = {}  # Dictionary to store the complete graph.
    routing_tables = {}  # Dictionary to store routing tables for each vertex.

    for vertice in vertices:
        # Apply Dijkstra's algorithm to each vertex to find shortest paths.
        distances, routing_tables[vertice] = dijkstra(vertice, graph)

        # Populate the complete graph with distances to other vertices.
        for cheese in vertices:
            if cheese != vertice:
                if vertice not in complete_graph:
                    complete_graph[vertice] = {cheese: distances[cheese]}
                else:
                    complete_graph[vertice][cheese] = distances[cheese]

    return complete_graph, routing_tables

#####################################################################################################################################################

def tsp ( complete_graph: Dict[int, Dict[int, Union[None, int]]],
          source:         int,
          length:         int,
          route:          list[int],
          memory:         threading.local
        ) ->              Tuple[List[int], int]:
    
    """
        Function to solve the TSP using an exhaustive search.
        In:
            * complete_graph: Complete graph of the vertices of interest.
            * source:         Vertex used to start the search.
        Out:
            * best_route:  Best route found in the search.
            * best_length: Length of the best route found.
    """
    memory.best_route = []  # Initialize best route found.
    memory.best_length = 10e9  # Initialize length of best route with a large number.

    def _tsp(graph, vertex, length, route):
        # Base case: if all vertices are visited, update best route and length.
        if len(route) == len(graph):
            if length < memory.best_length:
                memory.best_route = route
                memory.best_length = length
            return
        # Recursive case: explore unvisited neighbors.
        for neighbor in graph[vertex]:
            if neighbor not in route:
                _tsp(graph, neighbor, length + graph[vertex][neighbor], route + [neighbor])

    # Start the recursive TSP search from source.
    _tsp(complete_graph, source, 0, [source])
    return memory.best_route, memory.best_length

#####################################################################################################################################################

def expand_route ( route_in_complete_graph: List[int],
                   routing_tables:          Dict[int, Dict[int, Union[None, int]]],
                 ) ->                       List[int]:
    
    """
        Returns the route in the original graph corresponding to a route in the complete graph.
        In:
            * route_in_complete_graph: List of locations in the complete graph.
            * routing_tables:          Routing tables obtained when building the complete graph.
        Out:
            * route: Route in the original graph corresponding to the given one.
    """
    route = []
    # For each vertex pair in route, find corresponding sub-route in original graph.
    for i in range(len(route_in_complete_graph) - 1):
        route += find_route(routing_tables[route_in_complete_graph[i]], route_in_complete_graph[i], route_in_complete_graph[i + 1])
    return route
        
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

    player_pos = player_locations[name]

    # We create a complete graph of the cheeses and the initial position in our maze
    complete_graph, routing_tables = graph_to_metagraph(maze, [player_pos] + cheese)

    # We apply the tsp to the complete graph to get the shortest route
    best_route, best_length = tsp(complete_graph, player_pos, 0, [], threading.local())

    # We turn this best route in the complete graph in an actual route in the graph
    route = expand_route(best_route, routing_tables)

    # We turn this route into actions and store them in the memory
    memory.actions = locations_to_actions(route, maze_width)
    
    pass
    
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

    # We play the different actions stored in the memory at each turn
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
    
#################################################################################################################
###################################################### GO ! #####################################################
#################################################################################################################

if __name__ == "__main__":
    
    # Map the functions to the character
    players = [{"name": "TSP 1", "preprocessing_function": preprocessing, "turn_function": turn}]
    
    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage": 40.0,
              "nb_cheese": 8,
              "trace_length": 1000,
              "gui_speed":20}
    
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    
    # Show statistics
    print(stats)
    
#################################################################################################################
#################################################################################################################
