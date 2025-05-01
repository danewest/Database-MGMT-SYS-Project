"""
SCRIPT FOR CONNECTING TO THE DATABASE
"""

import mysql.connector

# Tries to connect to the DB
# Success: Print a message saying the connection was successful to the terminal
# Fail: Print error message to the terminal
try:
    connection = mysql.connector.connect(
        host="localhost",
        user = "root",
        password = "password",
        database = "cfg")

    print('Connected to MySQL Database')
except mysql.connector.Error as error:
    print('Failed to connect to MySQL database: {}'.format(error))