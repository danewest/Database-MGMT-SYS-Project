import mysql.connector
from mysql.connector import errorcode, cursor

# Updates the current credit limit
# Input: customer name and new credit limit
def update_customer_credit(connection, name, new_limit):
    cursor = connection.cursor()
    update_query = (
        'UPDATE Customer '
        'SET CreditLimit = %s '
        'WHERE CustomerName = %s '
    )

    update_data = (new_limit, name)

    cursor.execute(update_query, update_data)

    connection.commit()
    cursor.close()