from flask import Flask, request, render_template
from fileinput import filename
import sqlite3
import csv
import os
# from routing import *

app = Flask(__name__)

sav_routes = [['Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ', '20 Parsons Mead, Abingdon, Oxfordshire', '8 Morgan Vale, Abingdon, Oxfordshire', 'Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ'], ['Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ', 'Taldysai Village, Kazakhstan', '1 Hollow Way, Oxford, OX4 2LZ', 'Ashmolean Museum, Beaumont Street, Oxfordshire', '16 Acacia Gardens, Southmoor, Abingdon OX13 5DE', '25 The Park, Cumnor, Oxford OX2 9QS', 'Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ']]

map_routes = [
    ['Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ', 'Ashmolean Museum, Beaumont Street, Oxfordshire', 'Taldysai Village, Kazakhstan', '1 Hollow Way, Oxford, OX4 2LZ', '16 Acacia Gardens, Southmoor, Abingdon OX13 5DE', '25 The Park, Cumnor, Oxford OX2 9QS', 'Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ'] ,
    ['Abingdon School, Farc:\Users\piggy\OneDrive\Documents\Comp-Sci-NEA\routing.pyingdon Lodge, Abingdon OX14 1BQ', '8 Farriers Mews, Abingdon, Oxfordshire', '8 Morgan Vale, Abingdon, Oxfordshire', '20 Parsons Mead, Abingdon, Oxfordshire', 'Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ']
]

testdepot = "Abingdon School, Faringdon Lodge, Abingdon OX14 1BQ"

def fetch_data():
    # routes = []
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()
    routes = [[] for _ in range(len(cursor.execute("SELECT RouteID FROM routes").fetchall())-1)] # If you use multiplication here it does pointer magic and makes them all the same list
    # print(routes)
    data = []
    # for routeID in range(len(cursor.execute("SELECT RouteID FROM routes").fetchall())-1):
    #     response = cursor.execute("SELECT Address FROM students WHERE RouteID = ? ORDER BY RouteOrder ASC", (routeID,))
    #     route = list(map(lambda x: x[0], response.fetchall()))
    #     response = cursor.execute("SELECT Distance FROM routes WHERE RouteID = ?")
    #     data.append((route, ))
    response = cursor.execute("SELECT RouteID, Address FROM students ORDER BY RouteID, RouteOrder").fetchall()
    # print("response:")
    # print(response)
    for address in response:
        routes[address[0]].append(address[1])
        # print("routes[address[0]]",routes[address[0]])
        # print("routes: ", routes)
    response = cursor.execute("SELECT Distance, Stops FROM routes WHERE RouteID != -1 ORDER BY RouteID").fetchall()
    for info in response:
        data.append(info)
    # print(data)
    for route in routes:
        route.insert(0, testdepot)
        route.append(testdepot)
    return data, routes

def routes_to_embed(routes: list = []):
    embeds = []
    for route in routes:
        for address in route:
            # address: str
            formatted = address.replace(", ", ",").replace(" ", "+")
            route[route.index(address)] = formatted
        embeds.append(f"https://www.google.com/maps/embed/v1/directions?key=AIzaSyDE2qaxHADLeBQO1zLqfDIasLOalcHWHi0&origin={route[0]}&destination={route[-1]}&waypoints={'|'.join(route[1:-1])}")
    return embeds

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    depot = request.form["depot"]
    file = request.files["addresses"]
    file.save(file.filename)
    with open(file.filename) as addresses:
        csvreader = csv.reader(addresses)
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()
        cursor.executemany("INSERT INTO students(StudentID, Name, Address, Year, RouteID) VALUES(?, ?, ?, ?, -1)", list(csvreader))
        connection.commit()
    os.remove(file.filename)
    return render_template('finished.html')

@app.route('/maps/')
@app.route('/maps')
def mapdisplay():
    # connection = sqlite3.connect("student.db")
    # cursor = connection.cursor()
    # cursor.execute
    data, embeds = fetch_data()
    embeds = routes_to_embed(embeds)
    # print(embeds)
    return render_template('mapdisplay.html', maps=embeds, data=data, len=len(data))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)