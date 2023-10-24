#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This program the competition PyRat File
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

#####################################################################################################################################################
############################################################### CONSTANTS & VARIABLES ###############################################################
#####################################################################################################################################################

def get_neighbors ( vertex: int,
                    graph:  Union[numpy.ndarray, Dict[int, Dict[int, int]]]
                  ) ->      List[int]:

    """
        Fuction to return the list of neighbors of a given vertex.
        Here we propose an implementation for all types handled by the PyRat game.
        The function assumes that the vertex exists in the maze.
        It can be checked using for instance `assert vertex in get_vertices(graph)` but this takes time.
        In:
            * vertex: Vertex for which to compute the neighborhood.
            * graph:  Graph on which to get the neighborhood of the vertex.
        Out:
            * neighbors: List of vertices that are adjacent to the vertex in the graph.
    """
    
    # If "maze_representation" option is set to "dictionary"
    if isinstance(graph, dict):
        neighbors = list(graph[vertex].keys())

    # If "maze_representation" option is set to "matrix"
    elif isinstance(graph, numpy.ndarray):
        neighbors = graph[vertex].nonzero()[0].tolist()
    
    # Unhandled data type
    else:
        raise Exception("Unhandled graph type", type(graph))
    
    # Done
    return neighbors
    
#####################################################################################################################################################

def get_weight ( source: int,
                 target: int,
                 graph:  Union[numpy.ndarray, Dict[int, Dict[int, int]]]
               ) ->      List[int]:

    """
        Fuction to return the weight of the edge in the graph from the source to the target.
        Here we propose an implementation for all types handled by the PyRat game.
        The function assumes that both vertices exists in the maze and the target is a neighbor of the source.
        As above, it can be verified using `assert source in get_vertices(graph)` and `assert target in get_neighbors(source, graph)` but at some cost.
        In:
            * source: Source vertex in the graph.
            * target: Target vertex, assumed to be a neighbor of the source vertex in the graph.
            * graph:  Graph on which to get the weight from the source vertex to the target vertex.
        Out:
            * weight: Weight of the corresponding edge in the graph.
    """
    
    # If "maze_representation" option is set to "dictionary"
    if isinstance(graph, dict):
        weight = graph[source][target]
    
    # If "maze_representation" option is set to "matrix"
    elif isinstance(graph, numpy.ndarray):
        weight = graph[source, target]
    
    # Unhandled data type
    else:
        raise Exception("Unhandled graph type", type(graph))
    
    # Done
    return weight

#####################################################################################################################################################

def locations_to_action ( source:     int,
                          target:     int,
                          maze_width: int
                        ) ->          str: 

    """
        Function to transform two locations into an action to reach target from the source.
        In:
            * source:     Vertex on which the player is.
            * target:     Vertex where the character wants to go.
            * maze_width: Width of the maze in number of cells.
        Out:
            * action: Name of the action to go from the source to the target.
    """

    # Convert indices in row, col pairs
    source_row = source // maze_width
    source_col = source % maze_width
    target_row = target // maze_width
    target_col = target % maze_width
    
    # Check difference to get direction
    difference = (target_row - source_row, target_col - source_col)
    if difference == (0, 0):
        action = "nothing"
    elif difference == (0, -1):
        action = "west"
    elif difference == (0, 1):
        action = "east"
    elif difference == (1, 0):
        action = "south"
    elif difference == (-1, 0):
        action = "north"
    else:
        raise Exception("Impossible move from", source, "to", target)
    return action

#####################################################################################################################################################
#####################################################################################################################################################

def traversal ( source              :   int,
                graph               :   Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                create_structure    :   Callable[[], Any],
                push_to_structure   :   Callable[[Any, Tuple[int, int, int]], None],
                pop_from_structure  :   Callable[[Any], Tuple[int, int, int]],
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
    visited_vertices = set()  # for O(1) lookups
    queue_structure = create_structure()

    routing_table = {}
    distances_to_explored_vertices = {vertex: float('inf') for vertex in graph}
    distances_to_explored_vertices[source] = 0
    
    push_to_structure(queue_structure, (0, source, None))  # push (distance, vertex, parent)

    while queue_structure:

        distance, vertex, parent = pop_from_structure(queue_structure)

        if vertex in visited_vertices:
            continue

        visited_vertices.add(vertex)
        routing_table[vertex] = parent

        for neighbor in get_neighbors(vertex, graph):

            new_distance = distance + graph[vertex][neighbor]

            if new_distance < distances_to_explored_vertices[neighbor]:

                distances_to_explored_vertices[neighbor] = new_distance
                push_to_structure(queue_structure, (new_distance, neighbor, vertex))

    return distances_to_explored_vertices, routing_table

#####################################################################################################################################################

def dijkstra ( source: int,
               graph:  Union[numpy.ndarray, Dict[int, Dict[int, int]]],
             ) ->      Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
        Dijkstra's algorithm is a particular traversal where vertices are explored in an order that is proportional to the distance to the source vertex.
        In:
            * source: Vertex from which to start the traversal.
            * graph:  Graph on which to perform the traversal.
            * weights: A dictionary for hadling witgths between two vertex
        Out:
            * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
            * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """
    
    # Function to create an empty priority queue
    def _create_structure ():
        return []

    # Function to add an element to the priority queue
    def _push_to_structure (structure, element):
        heapq.heappush(structure, element)
    
    # Function to extract an element from the priority queue
    def _pop_from_structure (structure):
        return heapq.heappop(structure)
    
    # Perform the traversal
    distances_to_explored_vertices, routing_table = traversal(source, graph, _create_structure, _push_to_structure, _pop_from_structure)
    return distances_to_explored_vertices, routing_table

#####################################################################################################################################################

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

    # Check if the target exists in the routing table
    if target not in routing_table:
        raise ValueError("The target is not reachable from the source.")
    
    route = [target]
    current_vertex = target
    
    # Using a while loop and appending to the route instead of inserting at the beginning
    while current_vertex != source:
        current_vertex = routing_table[current_vertex]
        route.append(current_vertex)
    
    return route[::-1] 

#####################################################################################################################################################

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
    """
    actions = []
    for i in range(len(locations) - 1):
        action = locations_to_action(locations[i], locations[i + 1], maze_width)
        actions.append(action)
    return actions
    """
    return [locations_to_action(locations[i], locations[i + 1], maze_width) for i in range(len(locations) - 1)]


#####################################################################################################################################################
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
    x1, y1 = vertex1 % maze_width, vertex1 // maze_width
    x2, y2 = vertex2 % maze_width, vertex2 // maze_width
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
    closed_set = set() # The set of nodes already evaluated
    open_set = set([start]) # The set of discovered nodes that are not evaluated yet.

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

                routing_table[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target, maze_width)
                open_set.add(neighbor)
                open_queue.put((f_score[neighbor], neighbor))
    
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
    current = target
    path = [current]

    while current != start:
    
        current = routing_table[current]
        path.insert(0, current)
    
    return path

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def nearby_cheese(current_position, cheeses, max_distance=7):
    """
    Returns the nearest cheese if it's within the max_distance.
    """
    nearby = [cheese for cheese in cheeses if abs(current_position - cheese) <= max_distance]
    
    if nearby:
        return min(nearby, key=lambda cheese: abs(current_position - cheese))
    return None

#####################################################################################################################################################

def cheese_density(maze: Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                   cheese_location: int, 
                   cheeses: List[int], 
                   maze_width: int, 
                   D: int) -> int:
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
    
    distances = []

    for fromage in cheeses:
        if fromage != cheese_location:
            distance = manhattan_distance(cheese_location, fromage, maze_width)
            if distance <= D:
                distances.append(distance)
                
    densite = sum(1 / (distance + 1) for distance in distances)
    return densite

#####################################################################################################################################################

def tournois ( graph: Union[numpy.ndarray, Dict[int, Dict[int, int]]],
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
    
    Out:
        * route : The optimal path from the source to the best target vertex 
        * best_cheese : The optimal target vertex itself.
    """

    # Initialisation des variables pour stocker la distance la plus courte et le fromage optimal
    
    best_score = float('inf')
    best_cheese = None
    route = None

    for cheese in vertices:
        density = cheese_density(graph, cheese, vertices, maze_width, 7)  
        player_path, distance_to_cheese = a_star(source, cheese, graph, manhattan_distance, maze_width)

        # Combine distance and density into a single score
        score = distance_to_cheese + lambda_coefficient * (1 - density)

        if score < best_score:
            best_score = score
            best_cheese = cheese
            route = player_path

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

    route, cheese_goal = tournois (maze, source, cheese, maze_width)
    
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
    
        route_new, cheese_goal_new = tournois (maze, player_locations[name], cheese, maze_width)
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
    players = [{"name": "Greedyx", "preprocessing_function": preprocessing, "turn_function": turn}]
    
    # Customize the game elements
    config = {"maze_width": 31,
              "maze_height": 29,
              "mud_percentage": 20.0,
              "nb_cheese": 41,
              "trace_length": 1000}
    
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    
    # Show statistics
    print(stats)

#################################################################################################################
#################################################################################################################