import mysql.connector

def generate_customer_report(customerName):
    try:
        # Connect to local DB
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="cfg"
        )
        cursor = conn.cursor()

        # SQL script to get the information needed and generate the report
        query = """
        SELECT c.CustomerName, SUM(o1.QuotedPrice * o1.NumOrdered) AS TotalQuotedPrice
        FROM Customer c
        JOIN Orders o ON c.CustomerNum = o.CustomerNum
        JOIN OrderLine o1 ON o.OrderNum = o1.OrderNum
        WHERE c.CustomerName = %s
        GROUP BY c.CustomerName;
        """
        # Execute the query from above
        cursor.execute(query, (customerName,))
        res = cursor.fetchone()

        if res:
            report = {"CustomerName": res[0], "TotalQuotedPrice": float(res[1])}
        else:
            report = {"CustomerName": customerName, "TotalQuotedPrice": 0.0}

        # Returns a string of the report result to be used in the driver GUI
        return report

    # For MySQL errors
    except mysql.connector.Error as e:
        print("Database Error:", e)
        return None

    # Closes the connection when finished
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def generate_representative_report(connection):
    try:
        conn = connection
        cursor = conn.cursor()

        # SQL query for fetching the num of customers and avg balance for a representative
        representative_report_query = """
            SELECT r.FirstName, r.LastName, COUNT(c.CustomerNum) AS NumCustomers, ROUND(AVG(c.Balance), 2) AS AvgBalance
            FROM Rep r
            LEFT JOIN Customer c ON r.RepNum = c.RepNum
            GROUP BY r.RepNum, r.FirstName, r.LastName
            ORDER BY r.LastName, r.FirstName;
        """
        cursor.execute(representative_report_query)
        res = cursor.fetchall()

        report = []
        # loop through all the rows
        for row in res:
            if res:
                report.append({
                    "FirstName": row[0],
                    "LastName": row[1],
                    "NumCustomers": row[2],
                    "AvgBalance": float(row[3]) if row[3] is not None else 0.0
                })
            else:
                report.append({
                    "FirstName": '',
                    "LastName": '',
                    "NumCustomers": 0,
                    "AvgBalance": 0.0
                })

        return report

    except mysql.connector.Error as e:
        print("Database Error", e)
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()