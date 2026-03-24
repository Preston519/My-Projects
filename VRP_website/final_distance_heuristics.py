# from main import Graph

# testgraph = Graph(nodes=['Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ', '8 Farriers Mews, Abingdon, Oxfordshire', '1 Hollow Way, Oxford, OX4 2LZ', '8 Morgan Vale, Abingdon, Oxfordshire', '20 Parsons Mead, Abingdon, Oxfordshire', '25 The Park, Cumnor, Oxford OX2 9QS', '16 Acacia Gardens, Southmoor, Abingdon OX13 5DE', 'Taldysai Village, Kazakhstan', 'Ashmolean Museum, Beaumont Street, Oxfordshire'])
# testgraph.create_graph()

# All the parameters called graph are supposed to be Graph classes, but I can't do specify because importing Graph would be a circular import

# All works for distance-limited VRP

# Constructive Heuristics

def nearestneighbour(graph, max_capacity = 100000):
    unvisited = graph.nodes
    routes = []
    while len(unvisited) > 0:
        current = sorted(unvisited, key=graph.dist_graph[graph.depot].get)[0]
        route = [current]
        while graph.calc_distance(route) < max_capacity and len(unvisited) > 1:
            unvisited.pop(unvisited.index(current))
            nearest = min(unvisited, key=graph.dist_graph[current].get)
            route.append(nearest)
            current = nearest
        unvisited.pop(unvisited.index(current))
        routes.append(route)
    return routes

def saving(graph, max_distance=100000): # The most well known VRP heuristic!
    routes = list([node] for node in graph.nodes)
    savings = generate_savings(graph)
    while savings:
        current = max(savings, key=savings.get)
        in_route, indexes = is_in_route(current, routes) # Ignore the pair if one or more of the nodes are already interior to a route, because a more optimal saving has already been made
        if is_interior(current[1], routes[indexes[1]]) or is_interior(current[0], routes[indexes[0]]) or graph.calc_distance(routes[indexes[0]]) + graph.calc_distance(routes[indexes[1]]) - savings[current] > max_distance:
            savings.pop(current)
            continue
        if not in_route[0] and not in_route[1]: # If neither node is in an existing route
            routes.pop(routes.index([current[1]]))
            routes[routes.index([current[0]])].append(current[1])
        elif not in_route[0]: # If only one node is in an existing route, for both nodes
            if routes[indexes[1]].index(current[1]) == 0:
                routes[indexes[1]].insert(0, current[0])
            else:
                routes[indexes[1]].append(current[0])
            routes.pop(indexes[0])
        elif not in_route[1]:
            if routes[indexes[0]].index(current[0]) == 0:
                routes[indexes[0]].insert(0, current[1])
            else:
                routes[indexes[0]].append(current[1])
            routes.pop(indexes[1])
        elif not(indexes[0] == indexes[1]): # If both nodes are in two different existing routes
            routes[indexes[0]] = merge(graph, routes[indexes[0]], routes[indexes[1]], current)
            routes.pop(indexes[1])
        savings.pop(current)
    return routes

def merge(graph, route0: list, route1: list, link):
    """Merges two routes together as part of saving method"""
    if route0.index(link[0]) != len(route0)-1:
        route0.reverse()
    if route1.index(link[1]) != len(route1)-1:
        route1.reverse()
    merged_route = route0 + route1
    if graph.calc_distance(merged_route) > graph.calc_distance(list(reversed(merged_route))):
        merged_route.reverse()
    return merged_route

def is_interior(point: tuple, route: list):
    """Returns False if point is at either end of the route. Returns True otherwise"""
    index = route.index(point)
    return not(index == 0 or index == len(route)-1)
        
def is_in_route(pair: tuple, routes: list):
    """Returns if either point in pair are part of existing routes, and provides the index of the route"""
    in_route = [False, False]
    indexes = [None, None]
    for num in range(2):
        for route in routes:
            if pair[num] in route:
                indexes[num] = routes.index(route)
                if len(route) > 1:
                    in_route[num] = True
    return in_route, indexes

def generate_savings(graph):
    """Generates a dict of how much will be saved if two points are merged"""
    savings = dict()
    for nodenum in range(len(graph.nodes)):
        for node2 in graph.nodes[nodenum+1:]:
            savings[(graph.nodes[nodenum], node2)] = graph.dist_graph[graph.nodes[nodenum]][graph.depot] + graph.dist_graph[graph.depot][node2] - graph.dist_graph[graph.nodes[nodenum]][node2]
    return savings


# Improvement Heuristics

def two_opt_swap(route: list, first: int, second: int):
    """Swaps the points at indexes first and second in the route"""
    if first == second:
        return route
    new_route = [None]*len(route)
    new_route[:first+1] = route[:first+1]
    new_route[second:] = route[second:]
    new_route[first+1:second] = reversed(route[first+1:second])
    return new_route

def two_opt(graph, route: list): # Input route should always start and end with Abingdon School
    new_distance = float('inf')
    best_distance = graph.calc_distance(route)
    current_route = route
    for i in range(len(route[1:-2])):
        for j in range(len(route[i+1:-1])):
            new_route = two_opt_swap(current_route, i+1, j+i+2)
            new_distance = graph.calc_distance(new_route)
            if new_distance < best_distance:
                current_route = new_route
                best_distance = new_distance
    return current_route