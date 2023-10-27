# PyRat

## Authors
MARTIN AVILA Charly
LAARECH, Yasmine

## Introduction

Le projet PyRat (Python Rat) a été mené et développé dans le cadre du cours d'Algorithmes et mathématiques discrètes à l'IMT Atlantique.

C'est particulièrement intéressant en raison de son contenu très riche en termes d'algorithmes de recherche et d'estimation.

Le projet a progressé en parallèle avec le cours. Nous avons commencé avec des algorithmes pseudo-aléatoires et nous sommes progressivement passés à des algorithmes plus complexes comme le "greedy".

D'autres notions abordées lors du cours ont également été discutées, comme la recherche adversaire, qui cette fois ne se base pas uniquement sur l'agent (le rat) mais également sur les mouvements de l'adversaire.

## Git

Nous avons choisi d'utiliser le logiciel `git` pour pouvoir travailler ensemble. 

En effet, Git offre de nombreux avantages pour la réalisation de projets à plusieurs personnes, comme la gestion des versions permettant de revenir à une version précédente si le code ne fonctionne plus. 

Le contrôle de version est également essentiel pour suivre l'évolution du code et identifier les auteurs des modifications. 

Et finalement, la facilité de mise à jour du code avec une simple commande (`git pull`) permet à tous les collaborateurs d'avoir la même version.

Notre code est hébergé sur `github`: [https://github.com/napoknot21/pyrat-project.git](https://github.com/napoknot21/pyrat-project.git)

## Le code

Le code source se trouve dans le répertoire `$PYRAT_DIR/pyrat_environment/programs/`.
> Où `$PYRAT_DIR` est le chemin absolu où se trouve notre projet.

### Setup

Nous avons également implémenté un petit script appelé `setup.sh`.

En effet, lors des premières séances, Charly ne pouvait pas installer PyRat à cause de son système d'exploitation (Archlinux). 

Son système d'exploitation ne lui permettait pas d'utiliser `pip` pour installer des bibliothèques Python ; il devait plutôt utiliser son gestionnaire de paquets officiel, `pacman`.

Il a donc opté pour un environnement virtuel (`venv`). L'objectif de ce script était d'automatiser l'installation de PyRat sur n'importe quel système Linux ou Mac.

Ce script a aidé quelques camarades de classe à installer Python de manière plus efficace et rapide, car la majorité d'entre eux ne savaient pas comment utiliser un terminal.

```bash
#!/bin/sh

# Create a virtual environment in a subdirectory named venv
python3 -m venv .

# Activate the virtual environment
source ./bin/activate # This line is useful only for mac systems

# Modify the pyvenv.cfg file
sed -i "s/false/true/g" ./pyvenv.cfg

# Install the PyRat package
pip install ./extras/PyRat

# Run the setup_workspace function from the pyrat module
python -c "import pyrat; pyrat.PyRat.setup_workspace()" 2> /dev/null

```


### Greedy

Parlons maintenant du dernier algorithme implémenté en cours : `greedy`.

Nous avons créé au total 4 versions de cet algorithme. À chaque fois, nous avons amélioré les implémentations pour rendre le code plus efficace.

#### Greedy_1

Comme son nom l'indique, c'est la première version implémentée. Le principe est simple : on utilise une fonction heuristique appelée `give_score` pour calculer les distances du point d'origine à tous les autres sommets (vertices) et ensuite renvoyer les distances (ou scores) d'intérêt, en particulier ceux qui sont passés en paramètre sous le nom `targets`.

```python
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
    scores = [distances[target] for target in targets]
    
    # Return the scores and the routing table.
    return scores, routing_tables
```
> Fonction extraite de `greedy_1.py`
> Cette algorithme se sert de ```dijkstra``` du ficier `dijkstra.py`


L'algorithme `greedy` a pour objectif de calculer un itinéraire à travers le labyrinthe en maximisant le score à chaque étape. Il choisit constamment le sommet cible avec le score le plus élevé et ajuste son itinéraire pour se diriger vers celui-ci. Ce processus se poursuit jusqu'à ce que tous les sommets cibles soient visités.

```python
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
    # Initialize current_vertex to initial_vertex and set the list of unvisited vertices.
    current_vertex = initial_vertex
    unvisited = set(vertices)

    # The route starts with the initial vertex.
    route = [current_vertex]

    # While there are still unvisited vertices, continue the greedy algorithm.
    while unvisited:

        # Use give_score function to get scores for each unvisited vertex from current_vertex.
        scores, routing_tables = give_score(graph, current_vertex, list(unvisited))    
        
        # Find the vertex with the min score
        next_vertex = min(zip(unvisited, scores), key=lambda x: x[1])[0]
        
        # We use the routing_tables to retrieve the route from current_vertex to next_vertex
        route_a2b = find_route(routing_tables, current_vertex, next_vertex)

        # Update current_vertex and remove next_vertex from the set of unvisited vertices.
        current_vertex = route_a2b[-1]
        unvisited.remove(current_vertex)
        
        # Append the route_a2b to the main route, but skip appending the current_vertex as it's already added.
        route += route_a2b[1:]
    
    # Return the complete route.
    return route
```
> Fonction extraite de `greedy_1.py`
> Cette implémentation ne prend pas en cosidération des changements


CComme indiqué ci-dessus, cette implémentation ne prend pas en considération les événements qui pourraient survenir. Par conséquent, elle poursuivra son chemin même si le fromage visé disparaît en plein déplacement.

#### Greedy_2

Comme énoncé précédemment, ce `greedy` commence par une phase de prétraitement où il planifie sa première route vers le fromage le plus proche.

À chaque tour, la souris suit cette route. Si elle atteint un fromage ou si le fromage est collecté par un autre joueur, elle recalculera sa route vers le prochain fromage le plus proche.

Le script utilise l'algorithme de **Dijkstra** pour déterminer la distance minimale entre les fromages, et il choisit toujours le fromage le plus proche comme prochain objectif.

Pour notre fonction `greedy`, nous apporterons quelques changements.

```python
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
```
> Fonction extrate de `greedy_2.py`

De même, puisque nous allons recalculer le chemin à plusieurs reprises, en adaptant à des obstacles ou événements imprévus, nous devrons modifier la fonction `turn`. En effet, nous devrons ajuster notre route initialement calculée lors de la phase de prétraitement !

```python
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

```
> Fonction extraite de `greedy_2.py`

Cet algorithme est dit réactif car il s'adapte aux conditions qui lui sont données. Or, comme mentionné précédemment, nous utilisons Dijkstra dans notre fonction `give_scores` (fonction modifiée pour le `greedy_2`). Cependant, une question se pose : Ne pourrait-on pas faire mieux ? Est-ce que Dijkstra est le seul algorithme utile pour calculer les distances (scores) ?


#### Greedy_3

La problématique que `greedy_3` cherche à résoudre est d'améliorer la complexité de notre algorithme. En effet, Dijkstra est coûteux en temps et en mémoire car il explore tous les chemins possibles, et cette approche n'est pas toujours efficace.

C'est pourquoi nous avons implémenté l'algorithme `A*`! Le principe est simple : à l'aide d'une fonction heuristique, nous réduisons considérablement le nombre de chemins examinés pour atteindre notre destination.

Comme mentionné précédemment, nous avons choisi `manhattan` comme notre fonction heuristique \( h(s) \) .


```python
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
    > fonction extrai du fichier `a_star.py`

    De même dans le ficher
    # Convert vertex1 to its x and y coordinates
    x1, y1 = vertex1 % maze_width, vertex1 // maze_width
    
    # Convert vertex2 to its x and y coordinates
    x2, y2 = vertex2 % maze_width, vertex2 // maze_width
    
    # Calculate the Manhattan distance
    res = abs(x1 - x2) + abs(y1 - y2)
    
    return res
```
> Fonction extraite du fichier `a_star.py`

Comme mentionné précédemment, dans le fichier `a_star.py`, nous avons implémenté l'algorithme `A*` afin de définir la stratégie de mouvement d'une IA dans le jeu PyRat. Cette stratégie permet de traverser un labyrinthe pour collecter du fromage.

```python
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
```
> Fonction extraite de `a_star.py`
> On utilise une fonction `_reconstruct_path` qui la même tâche que `find_route` dans `dijkstra.py`

L'intérêt principal de cet algorithme réside dans la prise en compte de deux fonctions : la fonction heuristique \( h(s) \) (notamment `manhattan_distance`) et la fonction du coût du chemin \( g(s) \). L'idée est de sommer ces deux fonctions pour évaluer le coût total d'un chemin donné. En faisant cela, nous évitons d'investir du temps et de la mémoire dans la recherche de chemins qui ne seraient pas optimaux.

La force de l'algorithme `A*` par rapport à Dijkstra réside dans xctte combinaison de \( h(s) \) et \( g(s) \). 

Tandis que Dijkstra explore systématiquement tous les chemins possibles, `A*` utilise la fonction heuristique pour estimer le coût restant jusqu'à la destination. 

Cette estimation, combinée au coût réel pour atteindre le point courant (c'est-à-dire \( g(s) \)), permet de prioriser certains chemins par rapport à d'autres. Par conséquent, `A*` est souvent plus efficace que Dijkstra car il explore moins de chemins inutiles, grâce à cette capacité d'estimation.

Donc utilisons ceci dans notre fontion `greedy` !

```python
def greedy ( graph: Union[numpy.ndarray, Dict[int, Dict[int, int]]],
             source :   int, 
             vertices : List[int],
             maze_width: int
           ) -> int :
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
    shortest_distance = float('inf')
    best_cheese = None
    route = None

    # Pour chaque fromage dans la liste des vertices
    for cheese in vertices:

        # Calculer le chemin et la distance du point de départ au fromage actuel en utilisant l'algorithme A*
        player_path, distance = a_star(source, cheese, graph, manhattan_distance, maze_width)
        
        # Si la distance calculée est plus courte que la meilleure distance trouvée jusqu'à présent
        if distance < shortest_distance:

            # Mettre à jour la meilleure distance, le meilleur fromage, et le chemin optimal
            shortest_distance = distance
            best_cheese = cheese
            route = player_path

    # Retourner le chemin optimal et le fromage optimal
    return route, best_cheese

```
> Fonction principale de ```greedy_3.py```

Avec cette implémentation et le côté réactif de l'algorithme implémenté dans les versions précédentes, tout semble être suffisant !

Cependant, ce n'est pas vraiment le cas. En effet, malgré les optimisations actuelles, notre algorithme vise toujours le fromage le plus proche de la souris. Or, cette décision n'est pas toujours la meilleure en termes de stratégie.

#### Greedy 4

Avec l'implémentation précédente, qui est efficace en termes de prétraitement, il se peut que notre souris se dirige vers un fromage certes proche d'elle, mais isolé (c'est-à-dire qu'il n'y a pas d'autres fromages à proximité). Stratégiquement parlant, il serait plus judicieux de viser des zones où il y a une concentration de fromages.

C'est pourquoi nous introduisons la notion de `densité`, qui est définie comme le nombre de fromages dans une zone donnée se trouvant dans un rayon de distance \(D\).

Pour cela, nous allons implémenter la fonction `cheese_density`.

```python
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
```
> Fonction extraite de `greedy_4.py`
> On utilise `manhattan_distance` pour calculer les distances aux autres fromages

La fonction renvoie donc la densité d'un fromage, c'est-à-dire la proximité des autres fromages par rapport à lui. Ainsi, le fromage qui possède la plus grande densité sera celui qui nous intéressera le plus à récupérer.

Nous avons intégré cette logique dans notre algorithme `greedy`.

```python
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
```
> Fonction extratie de `greedy_4.py`

Le coefficient de lambda est crucial pour équilibrer l'importance de la distance par rapport à la densité du fromage. Si la valeur de lambda est faible, cela signifie que la densité du fromage a moins d'importance par rapport à la distance. 

Inversement, une valeur de lambda élevée donnera plus d'importance à la densité du fromage par rapport à la distance. En ajustant ce paramètre, nous pouvons affiner la stratégie de notre IA pour lui faire privilégier soit la proximité, soit les zones à haute densité de fromage.
