"""
SCRIPT FOR CONNECTING TO THE DATABASE
"""

import mysql.connector
from mysql.connector import errorcode, cursor
from main.database.scripts.update_customer import update_customer_credit

# Tries to connect to the DB
# Success: Print a message saying the connection was successful to the terminal
# Fail: Print error message to the terminal

# Global connection object
conn = None

# Function to connect to the database
def connect():
    try:
        global conn
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="cfg")

        print('Connected to MySQL Database')
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print('Failed to connect to MySQL database')
        return False

# Closes the connection
def close_connection():
    global conn
    conn.close()