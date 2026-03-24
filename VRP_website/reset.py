import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

cursor.execute("UPDATE students SET RouteID = -1, RouteOrder = ?", (None, ))
cursor.execute("DELETE FROM routes WHERE RouteID != -1")
cursor.execute("DELETE FROM students")

connection.commit()