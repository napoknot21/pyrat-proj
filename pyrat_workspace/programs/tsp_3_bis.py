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
from dijkstra import dijkstra, locations_to_actions

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def graph_to_metagraph ( graph : Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                         vertices: List[int]
                        ) -> Tuple[numpy.ndarray, Dict[int, Union[None, int]]] :
    """
        Function to build a complete graph out of locations of interest in a given graph.
        In:
            * graph:    Graph containing the vertices of interest.
            * vertices: Vertices to use in the complete graph.
        Out:
            * complete_graph: Complete graph of the vertices of interest.
            * routing_tables: Dictionary of routing tables obtained by traversals used to build the complete graph.
    """
    n = len(vertices)

    # Initialize with zeros the new complete graph
    complete_graph = numpy.zeros((n,n), dtype=int)

    # To store the routing tables
    routing_tables = {}

    for i, vertex_1 in enumerate(vertices) :

        # Perform Dijktra's algorithm starting from vertex1 to get 
        distances, routing_table = dijkstra(vertex_1, graph)

        # Store the routing table for vertex_1
        routing_tables[vertex_1] = routing_table

        for j, vertex_2 in enumerate(vertices) :

            if vertex_1 != vertex_2 :

                # Fill the complete graph with the distances from vertex_1 to vertex_2
                complete_graph[i][j] = distances[vertex_2]

    return complete_graph, routing_tables

#####################################################################################################################################################

def dfs_recursive ( source: int,
                    graph:  Union[numpy.ndarray, Dict[int, Dict[int, int]]]
                  ) ->      Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
        This is a recursive implementation of the DFS.
        At each call, we check if we are done with the traversal, and then we explore unexplored neighbors.
        This implementation stops when the spanning tree is done, i.e. when all vertices have been explored once.
        In:
            * source: Vertex from which to start the traversal.
            * graph:  Graph on which to perform the traversal.
        Out:
            * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
            * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """
    
    # We will fill these variables during the traversal
    routing_table = {source: None}
    distances_to_explored_vertices = {source: 0}
    
    # Internal implementation of the recursive DFS
    def _dfs_recursive (current_vertex, parent_vertex, current_length):
        
        # Visit the vertex
        print("Visiting", current_vertex, "at distance", current_length, "from start along the explored path")
        routing_table[current_vertex] = parent_vertex
        distances_to_explored_vertices[current_vertex] = current_length
        
        # We stop when all vertices are visited
        if len(distances_to_explored_vertices) == len(graph) :
            print("Spanning tree done, all vertices have been explored once using DFS")
            return
        
        # If there are still vertices to visit, we explore unexplored neighbors
        for neighbor in graph[current_vertex] :
            if neighbor not in distances_to_explored_vertices :
                _dfs_recursive(neighbor, current_vertex, current_length + graph[current_vertex][neighbor])
    
    # Perform the traversal
    _dfs_recursive(source, None, 0)
    return distances_to_explored_vertices, routing_table

#####################################################################################################################################################

def tsp ( complete_graph: numpy.ndarray,
          source:         int
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
    n = len(complete_graph)
    
    # Initialize variables to store the best route and its length
    best_route = []
    best_length = float('inf')
    
    def backtrack(remaining: set, vertex: int, path: List[int], weight: int) -> None:
        nonlocal best_length, best_route

        if not remaining:
            # If all vertices are visited, check if it forms a shorter route
            if weight < best_length:
                best_length = weight
                best_route = path[:]
        else:
            # Sort neighbors based on the distance from the current vertex
            sorted_neighbors = sorted(remaining, key=lambda x: complete_graph[vertex][x])
            
            for next_vertex in sorted_neighbors:
                new_remaining = remaining - {next_vertex}
                new_weight = weight + complete_graph[vertex][next_vertex]
                
                # Pruning: if path is already longer than known best, skip this path
                if new_weight < best_length:
                    backtrack(new_remaining, next_vertex, path + [next_vertex], new_weight)
    
    # Start the backtracking search from the source vertex
    initial_remaining = set(range(n)) - {source}
    backtrack(initial_remaining, source, [source], 0)
    
    # Add the source vertex to the end of the best route to complete the cycle
    best_route.append(source)
    
    return best_route, best_length

#####################################################################################################################################################

def expand_route (  route_in_complete_graph: List[int], 
                    routing_tables: Dict[int, Dict[int, Union[None, int]]], 
                    cell_names: List[int]
                ) -> List[int]:
    """
    Returns the route in the original graph corresponding to a route in the complete graph.
    
    Args:
        route_in_complete_graph: List of locations in the complete graph.
        routing_tables: Routing tables obtained when building the complete graph.
        cell_names: List of cells in the graph that were used to build the complete graph.

    Returns:
        route: Route in the original graph corresponding to the given one.
    """
    """
    route = []
    
    for i in range(len(route_in_complete_graph) - 1):
        source = route_in_complete_graph[i]
        target = route_in_complete_graph[i + 1]

        # Check if source or target are arrays and print them for debugging
        if isinstance(source, (list, numpy.ndarray)) or isinstance(target, (list, numpy.ndarray)):
            print(f"Source: {source}, Target: {target}")

        # Use the routing table to find the path between source and target in the original graph
        current_vertex = source
        while current_vertex != target:
            next_vertex = routing_tables[current_vertex][target]
            route.append(cell_names[current_vertex])
            current_vertex = next_vertex

    # Add the last cell to the route
    #route.append(cell_names[route_in_complete_graph[-1]])
    
    return route
    """
    route = []

    for sub_route in route_in_complete_graph:
        for i in range(len(sub_route) - 1):
            source = sub_route[i]
            target = sub_route[i + 1]

            current_vertex = source
            while current_vertex != target:
                next_vertex = routing_tables[current_vertex][target]
                route.append(cell_names[current_vertex])
                current_vertex = next_vertex

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
    # Convert maze to a graph representation and select vertices of interest
    current_position = player_locations[name]
    vertices_of_interest = [current_position] + cheese

    # Build the complete graph and routing tables using graph_to_metagraph function
    memory.complete_graph, memory.routing_tables = graph_to_metagraph(maze, vertices_of_interest)
    memory.cell_names = vertices_of_interest

    
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

    if cheese:  # Check if there is still cheese left
    
        source_index = memory.cell_names.index(player_locations[name])
        tsp_cheese = tsp(memory.complete_graph, source_index)
        path_to_cheese = expand_route(tsp_cheese, memory.routing_tables, memory.cell_names)
        actions_to_cheese = locations_to_actions(path_to_cheese, maze_width)
        
        return actions_to_cheese[0] if actions_to_cheese else random.choice(possible_actions)
    
    return choice(possible_actions)

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
              "trace_length": 1000}
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    # Show statistics
    print(stats)

#################################################################################################################
#################################################################################################################
