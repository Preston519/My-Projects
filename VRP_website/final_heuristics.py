# from main import Graph

# testgraph = Graph(nodes=['Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ', '8 Farriers Mews, Abingdon, Oxfordshire', '1 Hollow Way, Oxford, OX4 2LZ', '8 Morgan Vale, Abingdon, Oxfordshire', '20 Parsons Mead, Abingdon, Oxfordshire', '25 The Park, Cumnor, Oxford OX2 9QS', '16 Acacia Gardens, Southmoor, Abingdon OX13 5DE', 'Taldysai Village, Kazakhstan', 'Ashmolean Museum, Beaumont Street, Oxfordshire'])
# testgraph.create_graph()

# All the parameters called graph are supposed to be Graph classes, but I can't do specify because importing Graph would be a circular import

# Constructive Heuristics

class Heuristic:
    def __init__(self, graph, constraint: str, maximum: int):
        self._graph = graph
        self._constraint = constraint
        self._maximum = maximum
        self._routes = []

    def get_routes(self):
        return self._routes

class NearestNeighbour(Heuristic):
    def __init__(self, graph, constraint, maximum):
        super().__init__(graph, constraint, maximum)
    
    def execute(self):
        unvisited = self._graph.get_nodes()
        while len(unvisited) > 0:
            current = sorted(unvisited, key=self._graph.dist_edges(self._graph.depot).get)[0]
            route = [current]
            while len(route) < self._maximum and len(unvisited) > 1:
                unvisited.pop(unvisited.index(current))
                nearest = min(unvisited, key=self._graph.dist_edges(current).get)
                route.append(nearest)
                current = nearest
            unvisited.pop(unvisited.index(current))
            self._routes.append(route)


class Savings(Heuristic):
    def __init__(self, graph, constraint, maximum):
        super().__init__(graph, constraint, maximum)
        self._savings = dict()
    
    def execute(self):
        self._routes = list([node] for node in self._graph.get_nodes())
        self.generate_savings()
        while self._savings:
            current = max(self._savings, key=self._savings.get)
            in_route, indexes = self.is_in_route(current) # Ignore the pair if one or more of the nodes are already interior to a route, because a more optimal saving has already been made
            if self.is_interior(current, indexes) or indexes[0] == indexes[1] or self.check_constraint(indexes, current):
                self._savings.pop(current)
                continue
            elif not any(in_route): # If neither node is in an existing route
                self._routes[indexes[0]].append(current[1])
            else: # If one or both nodes are in an existing route
                self._routes[indexes[0]] = self.merge(indexes, current)
            self._routes.pop(indexes[1])
            self._savings.pop(current)
    
    def generate_savings(self):
        """Generates a dict of how much will be saved if two points are merged"""
        for node1 in self._graph.get_nodes():
            for node2 in self._graph.get_nodes():
                if node1 != node2:
                    if self._constraint == "time":
                        self._savings[(node1, node2)] = self._graph.find_time(node1, self._graph.get_depot()) + self._graph.find_time(self._graph.get_depot(), node2) - self._graph.find_time(node1,node2)
                    else:
                        self._savings[(node1, node2)] = self._graph.find_distance(node1, self._graph.get_depot()) + self._graph.find_distance(self._graph.get_depot(), node2) - self._graph.find_distance(node1, node2)

    def is_in_route(self, pair: tuple) -> tuple[list[bool], list[int]]:
        in_route = [False, False]
        indexes = [None, None]
        for num in range(2):
            for route in self._routes:
                if pair[num] in route:
                    indexes[num] = self._routes.index(route)
                    if len(route) > 1:
                        in_route[num] = True
        return in_route, indexes
    
    def is_interior(self, pair: tuple, indexes: list) -> bool:
        """Returns True if one point is interior to a route"""
        for i in range(2):
            if 0 < self._routes[indexes[i]].index(pair[i]) < len(self._routes[indexes[i]])-1:
                return True
        return False
    
    def check_constraint(self, indexes: list, current: tuple) -> bool:
        """Returns True if constraints are breached"""
        if self._constraint == "capacity":
            return len(self._routes[indexes[0]]) + len(self._routes[indexes[1]]) > self._maximum
        elif self._constraint == "time":
            return self._graph.calc_time(self._routes[indexes[0]]) + self._graph.calc_time(self._routes[indexes[1]]) - self._savings[current] > self._maximum*60
        elif self._constraint == "distance":
            return self._graph.calc_distance(self._routes[indexes[0]]) + self._graph.calc_distance(self._routes[indexes[1]]) - self._savings[current] > self._maximum
        else:
            raise Exception("Invalid constraint")
        
    def merge(self, indexes: list, link: tuple) -> list:
        """Merges two routes together as part of saving method"""
        route0 = self._routes[indexes[0]] # Assigning temporary variables to not modify original routes
        route1 = self._routes[indexes[1]]
        if route0.index(link[0]) != len(route0)-1:
            route0.reverse()
        if route1.index(link[1]) != 0:
            route1.reverse()
        merged_route = route0 + route1
        if self._constraint == "time" and self._graph.calc_time(merged_route) > self._graph.calc_time(list(reversed(merged_route))):
            merged_route.reverse()
        elif self._constraint != "time" and self._graph.calc_distance(merged_route) > self._graph.calc_distance(list(reversed(merged_route))):
            merged_route.reverse()
        return merged_route
    
# Improvement Heuristics

class TwoOpt(Heuristic):
    def __init__(self, graph, constraint, maximum, routes):
        super().__init__(graph, constraint, maximum)
        self._routes = routes
    
    def execute(self):
        for num, route in enumerate(self._routes):
            best_distance = self._graph.calc_time(route) if self._constraint == "time" else self._graph.calc_distance(route)
            current_route = route
            for i in range(len(route[:-1])):
                for j in range(len(route[i+1:])):
                    new_route, new_distance = self.swap(num, i, j+i+1)
                    if new_distance < best_distance:
                        current_route = new_route
                        best_distance = new_distance
            self._routes[num] = current_route
    
    def swap(self, listIndex: int, first: int, second: int) -> tuple[list, int]:
        """Swaps the points at indexes first and second in the route"""
        if first == second:
            return self._routes[listIndex]
        new_route = self._routes[listIndex][:first+1] + list(reversed(self._routes[listIndex][first+1:second])) + self._routes[listIndex][second:]
        if self._constraint == "time":
            distance = self._graph.calc_time(new_route)
            reverse_distance = self._graph.calc_time(list(reversed(new_route)))
        else:
            distance = self._graph.calc_distance(new_route)
            reverse_distance = self._graph.calc_distance(list(reversed(new_route)))
        return (new_route, distance) if distance <= reverse_distance else (list(reversed(new_route)), reverse_distance)
    
class Interchange(Heuristic):
    def __init__(self, graph, constraint, maximum, routes):
        super().__init__(graph, constraint, maximum)
        self._routes = routes
    
    def execute(self):
        for num1, route1 in enumerate(self._routes):
            for num2, route2 in enumerate(self._routes):
                if route1 == route2:
                    continue
                new_distance = float('inf')
                if self._constraint == "time":
                    best_distance = self._graph.calc_time(route1) + self._graph.calc_time(route2)
                else:
                    best_distance = self._graph.calc_distance(route1) + self._graph.calc_distance(route2)
                for i in range(len(route1)):
                    for j in range(len(route2)):
                        new_route1, new_route2, new_distance = self.interchange_swap(route1, route2, i, j)
                        if new_distance < best_distance:
                            if self._constraint == "time":
                                if self._graph.calc_time(new_route1) > self._maximum*60 and self._graph.calc_time(new_route2) > self._maximum*60:
                                    continue
                            elif self._graph.calc_distance(new_route1) > self._maximum and self._graph.calc_distance(new_route2) > self._maximum:
                                continue
                            route1 = new_route1
                            route2 = new_route2
                            best_distance = new_distance
                self._routes[num1] = route1
                self._routes[num2] = route2

    def interchange_swap(self, route1: list, route2: list, first: int, second: int) -> list[list]:
        new_routes = [route1[:first+1] + route2[second+1:], route2[:second+1] + route1[first+1:], 0]
        for num in range(2):
            if self._constraint == "time":
                distance = self._graph.calc_time(new_routes[num])
                reverse_distance = self._graph.calc_time(list(reversed(new_routes[num])))
            else:
                distance = self._graph.calc_distance(new_routes[num])
                reverse_distance = self._graph.calc_distance(list(reversed(new_routes[num])))
            if reverse_distance < distance:
                new_routes[num] = list(reversed(new_routes[num]))
                new_routes[2] += reverse_distance
            else:
                new_routes[2] += distance
        return new_routes