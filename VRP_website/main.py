import googlemaps
from flask import Flask, request, render_template, redirect, session
import sqlite3
import csv
from os import remove
from final_heuristics import Savings, TwoOpt, Interchange
import bcrypt

app = Flask(__name__)

class Graph:
    def __init__(self, nodes: list, depot: str, time_graph: dict = None, dist_graph: dict = None):
        self.time_graph = time_graph if time_graph else dict()
        self.dist_graph = dist_graph if dist_graph else dict()
        self.depot = depot
        self.nodes = nodes if nodes else []

    def add_dist_edge(self, node1, node2, weight) -> None:
        """Adds an edge on the distance graph, directed from node1 to node2"""
        if node1 not in self.dist_graph:
            self.dist_graph[node1] = {}
        self.dist_graph[node1][node2] = weight

    def add_time_edge(self, node1, node2, weight):
        """Adds an edge on the time graph, directed from node1 to node2"""
        if node1 not in self.time_graph:
            self.time_graph[node1] = {}
        self.time_graph[node1][node2] = weight

    def calc_distance(self, route: list) -> int:
        """Adds up all the distance weights of one route"""
        distance = 0
        for address_index in range(len(route)-1):
            distance += self.dist_graph[route[address_index]][route[address_index+1]]
        distance += self.dist_graph[self.depot][route[0]] + self.dist_graph[route[-1]][self.depot]
        return distance
    
    def calc_time(self, route: list) -> int:
        """Adds up all the time weights of one route"""
        time = 0
        for address_index in range(len(route)-1):
            time += self.time_graph[route[address_index]][route[address_index+1]]
        time += self.time_graph[self.depot][route[0]] + self.time_graph[route[-1]][self.depot]
        return time
    
    def find_distance(self, address1, address2) -> int:
        """Edge from address1 to address2 on dist_graph"""
        return self.dist_graph[address1][address2]
    
    def dist_edges(self, address1) -> dict:
        """Returns a dict of edge weights from address1 to all other nodes"""
        return self.dist_graph[address1]
    
    def find_time(self, address1, address2) -> int:
        """Edge from address1 to address2 on time_graph"""
        return self.time_graph[address1][address2]
    
    def time_edges(self, address1) -> dict:
        """Returns a dict of edge weights from address1 to all other nodes"""
        return self.time_graph[address1]
    
    def create_graph(self) -> None:
        gmaps = googlemaps.Client(key="EXAMPLEKEY")
        self.nodes.append(self.depot)
        
        splitNodes = [self.nodes[i:i+10] for i in range(0, len(self.nodes), 10)]
        for splitChunk1 in splitNodes:
            for splitChunk2 in splitNodes:
                result = gmaps.distance_matrix(splitChunk1, splitChunk2, mode="driving")
                if not all(result["origin_addresses"]):
                    for num, address in enumerate(result["origin_addresses"]):
                        if not address:
                            raise Exception("Address not found: " + splitChunk1[num])
                elif not all(result["destination_addresses"]):
                    for num, address in enumerate(result["destination_addresses"]):
                        if not address:
                            raise Exception("Address not found: " + splitChunk2[num])
                for num1, row in enumerate(result["rows"]):
                    for num2, element, in enumerate(row["elements"]):
                        if splitChunk1[num1] == splitChunk2[num2]:
                            continue
                        elif element["status"] == "ZERO_RESULTS":
                            raise Exception("No route found between" + splitChunk1[num] + "and" + splitChunk2[num])
                        self.add_dist_edge(splitChunk1[num1], splitChunk2[num2], element["distance"]["value"])
                        self.add_time_edge(splitChunk1[num1], splitChunk2[num2], element["duration"]["value"])                
        self.nodes.pop()

    def get_nodes(self) -> list:
        return self.nodes
    
    def get_depot(self) -> str:
        return self.depot
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get("username"):
        return redirect("/input")
    if request.method == 'POST':
        connection = sqlite3.connect("addresses.db")
        cursor = connection.cursor()
        if request.form["method"] == "register":
            if request.form["username"] == "" or request.form["password"] == "":
                return render_template("index.html", error="Empty username or password")
            elif '\"' in request.form["username"]:
                return render_template("index.html", error="Quotation marks are not allowed in usernames")
            elif cursor.execute("SELECT Username FROM login WHERE Username=?", (request.form["username"],)).fetchall():
                connection.close()
                return render_template("index.html", error="This username is already taken")
            username = request.form["username"]
            salt = bcrypt.gensalt()
            cursor.execute("INSERT INTO login VALUES(?, ?)", (username, bcrypt.hashpw(request.form["password"].encode("utf-8"), salt)))
            cursor.execute('CREATE TABLE "{}_routes" (RouteID INTEGER PRIMARY KEY, Distance INTEGER, Time INTEGER, Stops INTEGER)'.format(username))
            cursor.execute('CREATE TABLE "{tag}_addresses" (PersonID INTEGER PRIMARY KEY, Name TEXT, Address TEXT, RouteID INTEGER REFERENCES "{tag}_routes" (RouteID), RouteOrder INTEGER)'.format(tag=username))
            connection.commit()
            connection.close()
        else:
            password = cursor.execute("SELECT Password FROM login WHERE Username=?", (request.form["username"],)).fetchone()
            if password == None or not bcrypt.checkpw(request.form["password"].encode("utf-8"), password[0]):
                return render_template("index.html", error="Incorrect username or password")
        session["username"] = request.form["username"]
        return redirect('/input')
    return render_template("index.html")

@app.route('/input', methods=['GET', 'POST'])
@app.route('/input/', methods=['GET', 'POST'])
def data_input():
    if not session.get("username"):
        return redirect('/')
    if request.method == 'POST':
        username = session["username"]
        depot = request.form["depot"]
        file = request.files["addresses"]
        constraint = request.form["constraint"]
        maximum = request.form["maximum"]
        if not all((depot, file, constraint, maximum)):
            return render_template("input.html", error="Please fill all boxes", username=session["username"])
        elif not maximum.isdigit() or int(maximum) < 0:
            return render_template("input.html", error="Units of measurement must be a positive integer", username=session["username"])
        elif not file.filename.endswith(".csv"):
            return render_template("input.html", error="Submitted file is not of type csv", username=session["username"])
        file.save(file.filename)
        with open(file.filename) as addresses:
            data = list(csv.reader(addresses))
            error = None
            if any(len(row) != 3 for row in data):
                print(list(len(row) for row in data))
                error = "Incorrect amount of columns"
            elif any(not row[0].isdigit() for row in data):
                error = "PersonID must be an integer"
            elif sorted(set(x[0] for x in data)) != sorted(x[0] for x in data):
                error = "PersonID must be unique for every person"
            else:
                connection = sqlite3.connect("addresses.db")
                cursor = connection.cursor()
                cursor.execute('DELETE FROM "{}_routes" WHERE RouteID != -1'.format(username))
                cursor.execute('DELETE FROM "{}_addresses"'.format(username))
                cursor.executemany('INSERT INTO "{}_addresses"(PersonID, Name, Address, RouteID) VALUES(?, ?, ?, -1)'.format(username), data)
                cursor.execute('INSERT INTO "{}_addresses" (PersonID, Name, Address, RouteID) VALUES(-1, "Depot", ?, -1)'.format(username), (depot,))
                connection.commit()
                connection.close()
        remove(file.filename)
        if error: # Needs to be stalled until the file is deleted
            return render_template("input.html", error=error, username=session["username"])
        try:
            processing(list(row[2] for row in data), depot, constraint, int(maximum))
        except Exception as exception:
            return render_template("input.html", error=exception, username=session["username"])
        return render_template('finished.html')
    return render_template('input.html', username=session["username"])

@app.route('/maps')
@app.route('/maps/')
def mapdisplay():
    if not session.get("username"):
        return redirect('/')
    data, routes, depot = fetch_data()
    if not all((data, routes, depot)):
        return render_template("nomaps.html", username=session["username"])
    embeds = routes_to_embed(([x[2] for x in y]for y in routes), depot)
    return render_template('mapdisplay.html', maps=embeds, data=data, len=len(data), routes=routes, username=session["username"])

def processing(nodes: list, depot: str, constraint: str, maximum: int,) -> None:
    """Creates a graph with provided nodes and depot, then applies heuristic based on constraint and maximum. No returns, all in SQL"""
    graph = Graph(nodes=nodes, depot=depot)
    graph.create_graph()
    savings = Savings(graph, constraint, maximum)
    savings.execute()
    two_opt = TwoOpt(graph, constraint, maximum, savings.get_routes())
    two_opt.execute()
    interchange = Interchange(graph, constraint, maximum, two_opt.get_routes())
    connection = sqlite3.connect("addresses.db")
    cursor = connection.cursor()
    username = session["username"]
    for routeID, route in enumerate(interchange.get_routes()):
        cursor.execute('INSERT INTO "{}_routes" VALUES (?, ?, ?, ?)'.format(username), (routeID, graph.calc_distance(route), graph.calc_time(route), len(route)))
        for n, point in enumerate(route):
            cursor.execute('UPDATE "{}_addresses" SET RouteID = ?, RouteOrder = ? WHERE Address = ?'.format(username), (routeID, n+1, point))
    connection.commit() # ALWAYS COMMIT dangit
    connection.close()

def fetch_data() -> tuple[list[list[tuple]], list, str]:
    """Gets display data from SQL. Data: list(list(tuple)), routes: list, depot: str"""
    connection = sqlite3.connect("addresses.db")
    cursor = connection.cursor()
    username = session["username"]
    routeAmt = len(cursor.execute('SELECT RouteID FROM "{}_routes"'.format(username)).fetchall())
    routes = [[] for _ in range(routeAmt)] # If you use multiplication here it does pointer magic and makes them all the same list because mutable data structure
    data = []
    response = cursor.execute('SELECT RouteID, Address, PersonID, Name FROM "{}_addresses" ORDER BY RouteID, RouteOrder'.format(username)).fetchall()
    if not response:
        routes = None
        depot = None
    else:
        depot = response.pop(0)[1]
        for address in response:
            routes[address[0]].append((address[2], address[3], address[1]))
    response = cursor.execute('SELECT Distance, Time, Stops FROM "{}_routes" WHERE RouteID != -1 ORDER BY RouteID'.format(username)).fetchall()
    if not response:
        data = None
    for info in response:
        data.append(info)
    connection.close()
    return data, routes, depot

def routes_to_embed(routes: list[list[str]], depot: str) -> list[str]:
    """Turns a list of routes into a list of embed URLs"""
    embeds = []
    depot = depot.replace(", ", ",").replace(" ", "+").replace("&", "and")
    for route in routes:
        for address in route:
            route[route.index(address)] = address.replace(", ", ",").replace(" ", "+").replace("&", "and")
        embeds.append(f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyDE2qaxHADLeBQO1zLqfDIasLOalcHWHi0&origin={depot}&destination={depot}&waypoints={'|'.join(route)}")
    return embeds

@app.route('/reset')
@app.route('/reset/')
def reset_page():
    if session.get("username"):
        connection = sqlite3.connect("addresses.db")
        cursor = connection.cursor()
        cursor.execute('DELETE FROM "{}_routes" WHERE RouteID != -1'.format(session['username']))
        cursor.execute('DELETE FROM "{}_addresses"'.format(session['username']))
        connection.commit()
        connection.close()
        return redirect("/input")
    return redirect("/")

@app.route('/logout')
@app.route('/logout/')
def logout():
    if session.get("username"):
        session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = "f5a48f39fe9f9545d425ba7d751d2589a6a588f36b334a26b469f1b539d342af"
    app.run(host="127.0.0.1", port=80, debug=True)