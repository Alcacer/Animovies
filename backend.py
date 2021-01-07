import sqlite3


def connect():
    connection = sqlite3.connect("DB\\Animovies.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Animovies (ID INTEGER Primary Key, Name TEXT, Category TEXT)")
    connection.commit()
    connection.close()


def view(category):
    connection = sqlite3.connect("DB\\Animovies.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Animovies WHERE Category = ?", (category,))
    output = cursor.fetchall()
    connection.close()
    return output


def view_all():
    connection = sqlite3.connect("DB\\Animovies.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Animovies")
    output = cursor.fetchall()
    connection.close()
    return output


def search(name=""):
    connection = sqlite3.connect("DB\\Animovies.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Animovies WHERE Name = ?", (name,))
    output = cursor.fetchall()
    connection.close()
    return output


def insert(name, category):
    connection = sqlite3.connect("DB\\Animovies.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Animovies VALUES (NULL,?,?)", (name, category))
    connection.commit()
    connection.close()


def delete(name):
    connection = sqlite3.connect("DB\\Animovies.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Animovies WHERE Name = ?", (name,))
    connection.commit()
    connection.close()


connect()
