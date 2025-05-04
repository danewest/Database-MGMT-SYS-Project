'''
!Adds a Representative!
adding a representative adds to table Rep
with attributes: RepNum CHAR(2) PRIMARY KEY, LastName CHAR(15),
FirstName CHAR(15), Street CHAR(15), City CHAR(15), State CHAR(2),
PostalCode CHAR(5), Commission DECIMAL(7,2), Rate DECIMAL(3,2)
'''

import mysql.connector
from mysql.connector import errorcode, cursor

def is_valid_decimal(value, precision, scale):
    try:
        float_value = float(value)
    except ValueError:
        return False  # not a number

    # split on decimal point
    parts = str(value).split(".")
    digits_before = len(parts[0].lstrip("-"))
    digits_after = len(parts[1]) if len(parts) > 1 else 0
    total_digits = digits_before + digits_after

    return total_digits <= precision and digits_after <= scale

def add_representative(connection, last_name, first_name, street, city, state, postal_code, commission, rate):
    try:
        cursor = connection.cursor()

        # generate a rep_num in sequential order, starting at 10
        cursor.execute("SELECT MAX(RepNum) FROM Rep")
        max_rep_num = cursor.fetchone()[0]
        if max_rep_num is None:
            rep_num: int = 10  # or whatever your starting point is
        else:
            rep_num = int(max_rep_num) + 1

        # validate inputs
        # test last_name, first_name, street, and city: must be a string length 15 or less
        variables = [last_name, first_name, street, city]
        for var in variables:
            if var is not None:
                if not isinstance(var, str) or  len(var) > 15:
                    return "Error: " + var + " must be Max 15 Characters Long"

        # test state: must be string of length 2
        if state not in (None, ""):
            if not isinstance(state, str) or len(state) != 2:
                return "Error: State must be Represented by 2 Characters"

        # test postalcode: must be string of length 5
        if postal_code is not None:
            if not isinstance(postal_code, int) or postal_code <= 9999 or postal_code > 99999:
                return "Error: Postal Code must be a 5 Digit Number"

        # test commission: must be a valid decimal
        if commission is not None:
            if not is_valid_decimal(commission, 7, 2):
                return "Error: Commission must be a Decimal Number"

        # test rate: must be a valid decimal
        if rate is not None:
            if not is_valid_decimal(rate, 3, 2):
                return "Error: Rate must be a Decimal Number"

        # prepare SQL query
        insert_query = """
        INSERT INTO Rep(RepNum, LastName, FirstName, Street, City, State, PostalCode, Commission, Rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # execute query with actual values
        cursor.execute(insert_query, (rep_num, last_name, first_name, street, city, state, postal_code, commission, rate))
        connection.commit()
        return "Representative Added"

    except mysql.connector.Error as error:
        return "Error while connecting to MySQL: {}".format(error)

    finally:
        # close cursor
        if cursor:
            cursor.close()